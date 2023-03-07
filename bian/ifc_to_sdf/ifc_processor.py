import subprocess
import os
import time

import ifcopenshell


def ifc_to_mesh(ifc_converter_path, element_path, collada_path, method='subprocess'):
    convert_path = '{} {} {}'.format(ifc_converter_path, element_path,
                                        collada_path)
    if method == 'os':
        os.popen(convert_path)
        time.sleep(5)
    elif method == 'subprocess':
        return_code = 1
        while return_code == 1:
            return_code = subprocess.Popen(convert_path, shell=False).wait()


def split_ifc(ifc_file, element, element_path):
    new_model = ifcopenshell.file()
    for container in ifc_file.by_type("IfcRelContainedInSpatialStructure"):
        for ele in container[4]:
            if ele.id() == element.id():
                new_model.add(container)
    for i in ifc_file.by_type("IfcRelAggregates"):
        new_model.add(i)
    new_model.add(element)
    new_model.write(element_path)
    _model = ifcopenshell.open(element_path)
    for elements in _model.by_type("IfcBuildingElement"):
        if element.GlobalId != elements.GlobalId:
            _model.remove(elements)
        elif element.GlobalId == elements.GlobalId:
            element.ObjectPlacement.RelativePlacement.Location.Coordinates = (0., 0., 0.)
    for product in _model.by_type("IfcProduct"):
        if product.is_a() == "IfcGrid" or product.is_a() == "IfcSite":
            _model.remove(product)
    _model.write(element_path)
