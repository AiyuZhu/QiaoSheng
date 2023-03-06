import ifcopenshell
import os
import time
import subprocess
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
from physics_attr import calculate_mass, calculate_inertia, rotationMatrixToEulerAngles, calculate_volume


class IfcToSdf(object):
    def __init__(self, input_ifc_model_path, folder_name, output_sdf_path, ifc_converter_path=None):
        # create folders as gazebo requirements
        self.input_ifc_path = input_ifc_model_path
        self.folder_name = folder_name
        self.output_sdf_path = output_sdf_path + '\\{}'.format(self.folder_name)
        self.launch_path = self.output_sdf_path + '\\launch'
        self.models_path = self.output_sdf_path + '\\models'
        self.worlds_path = self.output_sdf_path + '\\worlds'
        if ifc_converter_path is None:
            self.ifc_converter_path = '..\\ifc_to_sdf\\IfcConvert.exe'  # TODO add function to match multi os
        else:
            self.ifc_converter_path = ifc_converter_path
        if not os.path.exists(self.output_sdf_path):
            os.mkdir(self.output_sdf_path)
        if not os.path.exists(self.launch_path):
            os.mkdir(self.launch_path)
        if not os.path.exists(self.models_path):
            os.mkdir(self.models_path)
        if not os.path.exists(self.worlds_path):
            os.mkdir(self.worlds_path)

        # read ifc by ifcopenshell
        self.ifc_file = ifcopenshell.open(self.input_ifc_path)

        # element_list
        self.elements_list = []

        # project name
        self.project_name = self.ifc_file.by_type('IfcProject')[0].Name

    def create_ros_launch(self):

        launch_path = self.launch_path + '\\{}.launch'.format(str(self.project_name + '_launch'))
        launch_file = """<launch>
                      <include file="$(find gazebo_ros)/launch/empty_world.launch">
                        <arg name="world_name" value="$(find {})/worlds/{}.world"/> 
                        <arg name="paused" value="false"/>
                        <arg name="use_sim_time" value="true"/>
                        <arg name="gui" value="true"/>
                        <arg name="recording" value="false"/>
                        <arg name="debug" value="false"/>
                      </include>
                    </launch>
                    """.format(self.folder_name, self.project_name)
        with open(launch_path, 'w', encoding='utf-8') as f:
            f.write(str(launch_file))

    def create_models(self, static="False"):
        for _ in self.ifc_file.by_type("IfcBuildingElement"):
            if _.is_a() != "IfcBuildingElementProxy":
                element_name = _.GlobalId
                matrix = ifcopenshell.util.placement.get_local_placement(_.ObjectPlacement)
                element_position = list(matrix[:, 3][:3]) + list(rotationMatrixToEulerAngles(matrix))
                self.elements_list.append([element_name, element_position])
                element_folder_path = self.models_path + '\\{}'.format(element_name)
                # create single element sdf format folder
                if not os.path.exists(element_folder_path):
                    os.mkdir(element_folder_path)
                # create meshes folder, save .dae here

                element_meshes = element_folder_path + '\\meshes'
                if not os.path.exists(element_meshes):
                    os.mkdir(element_meshes)
                    # create .ifc for single element
                element_path = element_meshes + '\\{}.ifc'.format(element_name)
                new_model = ifcopenshell.file()
                for container in self.ifc_file.by_type("IfcRelContainedInSpatialStructure"):
                    for ele in container[4]:
                        if ele.id() == _.id():
                            new_model.add(container)
                for i in self.ifc_file.by_type("IfcRelAggregates"):
                    new_model.add(i)
                new_model.add(_)
                new_model.write(element_path)
                _model = ifcopenshell.open(element_path)
                for element in _model.by_type("IfcBuildingElement"):
                    if element.GlobalId != _.GlobalId:
                        _model.remove(element)
                    elif element.GlobalId == _.GlobalId:
                        element.ObjectPlacement.RelativePlacement.Location.Coordinates = (0., 0., 0.)
                for product in _model.by_type("IfcProduct"):
                    if product.is_a() == "IfcGrid":
                        _model.remove(product)
                _model.write(element_path)

                # use ifcConvert to convert ifc to collada
                collada_path = element_meshes + '\\{}.dae'.format(element_name)
                convert_path = '{} {} {} {}'.format(self.ifc_converter_path, '--building-local-placement', element_path,
                                                    collada_path)
                # os.popen(convert_path)
                # time.sleep(1)
                return_code = 1
                while return_code == 1:
                    return_code = subprocess.Popen(convert_path, shell=False).wait()

                # create model.config
                model_config_path = element_folder_path + '\\model.config'
                model_config = """<?xml version = "1.0"?>
                                <model>
                                <name>{0}</name>
                                <version>1.0</version>
                                <sdf version='1.5'>model.sdf</sdf>
                                
                                <author>
                                    <name>PandaZay</name>
                                    <email>a.zhu@tue.nl</email>
                                </author>
                                
                                <description>
                                    {1}
                                </description>
                                </model>
                                """.format(element_name, _.is_a())
                with open(model_config_path, 'w', encoding='utf-8') as f:
                    f.write(str(model_config))

                # create model.sdf
                model_sdf_path = element_folder_path + '\\model.sdf'
                model_meshes = 'model://' + element_name + '//meshes//{}'.format(element_name + '.dae')

                # get vol and calc mass, inertia
                # quan = ifcopenshell.util.element.get_psets(_, qtos_only=True)
                # vol = next(iter(quan.values()))['NetVolume']
                vol = calculate_volume(collada_path)
                inertia = calculate_inertia(collada_path, calculate_mass(vol, 'steel'))  # add get material

                model_sdf = """<?xml version="1.0" ?>
                                <sdf version = '1.5'>
                                <model name = "{0}">
                                    <static>{1}</static>
                                    <self_collide>True</self_collide>
                                    <enable_wind>True</enable_wind>
                                    <pose>0 0 0 0 0 0</pose>
                                
                                    <link name = '{2}'>
                                        <inertial>
                                          <mass>{3}</mass>
                                          <pose>{11} {12} {13} 0 0 0</pose>
                                          <inertia>
                                            <ixx>{4}</ixx>
                                            <ixy>{5}</ixy>
                                            <ixz>{6}</ixz>
                                            <iyy>{7}</iyy>
                                            <iyz>{8}</iyz>
                                            <izz>{9}</izz>
                                          </inertia>
                                        </inertial>
                                
                                        <collision name='collision'>
                                            <geometry>
                                                <mesh>
                                                    <uri>{10}</uri>
                                                </mesh>
                                            </geometry>
                                        </collision>
                                
                                        <visual name='visual'>
                                            <geometry>
                                                <mesh>
                                                    <uri>{10}</uri>
                                                </mesh>
                                            </geometry>
                                        </visual>
                                    </link>
                                </model>
                                </sdf>
                                """.format(element_name, static, _.is_a(), inertia[0], inertia[1], inertia[2],
                                           inertia[3],
                                           inertia[4], inertia[5], inertia[6], model_meshes, inertia[7], inertia[8],
                                           inertia[9])

                with open(model_sdf_path, 'w', encoding='utf-8') as f:
                    f.write(str(model_sdf))

    def create_worlds(self):
        world_path = self.worlds_path + '\\{}.world'.format(self.project_name)
        world_file = """<?xml version="1.0" ?>
                        <sdf version="1.5">
                          <world name="{0}">
                            <physics type="ode">
                            ...
                            </physics>  
                            
                            <include>
                                <uri>model://sun</uri>
                            </include>

                            <include>
                                <uri>model://plane</uri>
                            </include>
                        """.format(self.project_name)
        with open(world_path, 'w', encoding='utf-8') as f:
            f.write(str(world_file))
        with open(world_path, 'a', encoding='utf-8') as f:
            for in_element in self.elements_list:
                include_element = """
                                    <include>
                                        <uri>model://{0}</uri>
                                        <pose>{1} {2} {3} 0 0 0</pose>
                                    </include>
                                    """.format(in_element[0], in_element[1][0], in_element[1][1], in_element[1][2])
                f.write(str(include_element))
        with open(world_path, 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write(' </world>')
            f.write('\n')
            f.write('</sdf>')


if __name__ == "__main__":
    # BIM model's path
    path_bim = '..\\..\\Case_for_RC\\BIM_model\\IFC_model\\unit_without_beam_in_b_room.ifc'
    # the path where you want to set the sdf folder
    path_sdf = 'C:\\Users\\31613\\Desktop'
    its = IfcToSdf(path_bim, 'bim_model', path_sdf)
    its.create_ros_launch()
    its.create_models()
    its.create_worlds()
