import os
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
import materials
import ifcopenshell.api.geometry.edit_object_placement as iep
import math

#
# from physics_attr import rotationMatrixToEulerAngles
#
# # load model
model = ifcopenshell.open("C:\\Users\\Aiyu\\Desktop\\Barn.ifc")
print(model)
beam = model.by_id('14Q2LABuj0ouJ970CxJHwC')
print(beam)
new_model = ifcopenshell.file()
for i in model.traverse(beam):
    new_model.add(i)
for i in model.get_inverse(beam):
    new_model.add(i)
new_model.write("C:\\Users\\Aiyu\\Desktop\\beam_test.ifc")
# beam.ObjectPlacement.RelativePlacement.Location.Coordinates = (0., 0., 0.)
# # placement_matrix = ifcopenshell.util.placement.get_local_placement(beam.ObjectPlacement)
# m = ifcopenshell.util.placement.get_local_placement(beam.ObjectPlacement)
# print(m)
# n = 0
# while n < 3:
#     placement_matrix[n][3] = 0
#     n+=1
# ifcopenshell.api.run("geometry.edit_object_placement", model, product=beam, matrix=placement_matrix, should_cascade=False)
# m = ifcopenshell.util.placement.get_local_placement(beam.ObjectPlacement)
# print(m)
# model.write("C:\\Users\\Aiyu\\Desktop\\Barn_revit.ifc")

# matrix = [[1, 0, 0, 0],
#           [0, 1, 0, 0],
#           [0, 0, 1, 0],
#           [0, 0, 0, 1]]
# iep.Usecase(beam).convert_matrix_to_si(matrix)
# print(project.Name)
# curtain_wall = model.by_type('IfcPlate')[0]
# # if curtain_wall.is_a() != 'IfcBuildingElementProxy' and curtain_wall.is_a() != 'IfcCurtainWall':
# #     print('ssssssss')
# # else:
# #     print('ddddddddddddddddddddddd')
# roof = model.by_guid('3LhSTesrr2xxw9MQ7ULln6')
# print(model.traverse(roof))
# # get all building elements in ifc
# for element in model.by_type("IfcBuildingElement"):
#     print(element)
#
# # print(model.traverse(footing))
# # print(model.get_inverse(footing))
#
# footing = model.by_type("IfcFooting")[2]
# contained = model.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE")[0]
# for container in model.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE"):
#     print(container[4])
#     print(type(container[4]))
#     for ele in container[4]:
#         if ele.id() == footing.id():
#             print(ele, 'gooooooo')
#
# footing = model.by_type("IfcColumn")[0]
# footing.ObjectPlacement.RelativePlacement.Location.Coordinates = (0., 0., 0.)
# new_model = ifcopenshell.file()
# print(model.traverse(footing))
# for i in model.traverse(footing):
#     new_model.add(i)
# new_model.write("C:\\Users\\Aiyu\\Desktop\\Roof.ifc")
# print('footing placement',footing.ObjectPlacement)
# # split ifc element
# new_model = ifcopenshell.file()
# container = ifcopenshell.util.element.get_container(footing)
# # print(container)
# # run("spatial.assign_container", new_model, relating_structure=container, product=footing)
# new_model.add(contained)
# # new_model.add(footing)
# relation = model.by_type("IfcRelaggregates")
# # for i in relation:
# #     new_model.add(i)
# # get all building elements in ifc
# new_model.write("C:\\Users\\31613\\Desktop\\footing.ifc")
#
# model = ifcopenshell.open("C:\\Users\\31613\\Desktop\\footing.ifc")
# for element in model.by_type("IfcBuildingElement"):
#     if element.GlobalId != footing.GlobalId:
#         model.remove(element)
# model.remove(model.by_type("IfcGrid")[0])
# model.write("C:\\Users\\31613\\Desktop\\footing.ifc")
# # calculate weight
# # print(footing.get_info())
# matrix = ifcopenshell.util.placement.get_local_placement(footing.ObjectPlacement)
# print(matrix)
# print(list(rotationMatrixToEulerAngles(matrix)))
# print(list(matrix[:, 3][:3]) + list(rotationMatrixToEulerAngles(matrix)))
#
# # use ifcconvert to convert ifc to collada
# collada_path = element_meshes + '\\{}.dae'.format(element_name)


# element_path = 'C:\\Users\\Aiyu\\Desktop\\1v_ZCRjlL9pudQA7oZBgU5.ifc'  # should input by user
# collada_path = 'C:\\Users\\Aiyu\\Desktop\\1v_ZCRjlL9pudQA7oZBgU5.dae'  # should input by user
# ifc_converter_path = '..\\ifc_to_sdf\\IfcConvert.exe'
# convert_path = '{} {} {}'.format(ifc_converter_path, element_path, collada_path)
# print("os", os.popen(convert_path))


#
# # Get all properties and quantities of the wall, including inherited type properties
# psets = ifcopenshell.util.element.get_psets(footing)
# print(psets)
#
# # Get only properties and not quantities
# print(ifcopenshell.util.element.get_psets(footing, psets_only=True))
#
# # Get only quantities and not properties
# quan = ifcopenshell.util.element.get_psets(footing, qtos_only=True)
# vol = next(iter(quan.values()))['NetVolume']
# print(vol)
# den = materials.carbon_steel.density
# print(den)
# weight = vol * den
# print(weight)
# # for i in quan.values():
# #     print(i['NetVolume'])
# # project = model.by_type('IFCPROJECT')[0]
# # print(project.Name)
#
#

import numpy as np

import ifcopenshell.geom
import ifcopenshell.util.placement
import ifcopenshell

# Load the Barn Model and extract one of the "faulty" elements
# model = ifcopenshell.open('C:\\Users\\31613\\Desktop\\Barn.ifc')
# item = model.by_guid('0v68eVm656WgN4ZiDn3nVZ')
# print(item)
