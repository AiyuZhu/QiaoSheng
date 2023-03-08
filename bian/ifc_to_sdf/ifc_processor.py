import subprocess
import os
import time

import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.api.geometry.edit_object_placement


def ifc_to_mesh(ifc_converter_path, element_path, collada_path, method='subprocess'):
    convert_path = '{} {} {} {}'.format(ifc_converter_path, '--use-world-coords', element_path,
                                        collada_path)
    if method == 'os':
        os.popen(convert_path)
        time.sleep(2)
    elif method == 'subprocess':
        return_code = 1
        while return_code == 1:
            return_code = subprocess.Popen(convert_path, shell=False).wait()

def split_ifc(ifc_file, element, element_path):
    new_model = ifcopenshell.file()
    for i in ifc_file.traverse(element):
        new_model.add(i)
    unit = ifc_file.by_type('IfcUnitAssignment')[0]
    new_model.add(unit)
    new_model.write(element_path)
    _model = ifcopenshell.open(element_path)
    target_element = _model.by_id(element.GlobalId)
    set_origin_placement(target_element, _model)
    _model.write(element_path)


def set_origin_placement(element, _model):
    element.ObjectPlacement.RelativePlacement.Location.Coordinates = (0., 0., 0.)
    placement_matrix = ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)
    n = 0
    while n < 3:
        placement_matrix[n][3] = 0
        n += 1
    ifcopenshell.api.run("geometry.edit_object_placement", _model, product=element, matrix=placement_matrix,
                         should_cascade=False)
