import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
from ifcopenshell.api import run
# load model
model = ifcopenshell.open("..\\..\\Case_for_RC\\BIM_model\\IFC_model\\unit_without_beam_in_room.ifc")

# get all building elements in ifc
# for element in model.by_type("IfcBuildingElement"):
#     print(element)

# print(model.traverse(footing))
# print(model.get_inverse(footing))


contained = model.by_type("IFCRELCONTAINEDINSPATIALSTRUCTURE")[0]
footing = model.by_type("IfcFooting")[0]

# split ifc element
# new_model = ifcopenshell.file()
# # container = ifcopenshell.util.element.get_container(footing)
# # run("spatial.assign_container", new_model, relating_structure=container, product=footing)
# new_model.add(contained)
# # new_model.add(footing)
# relation = model.by_type("IfcRelaggregates")
# for i in relation:
#     new_model.add(i)
# # get all building elements in ifc
# new_model.write("C:\\Users\\Aiyu\\Desktop\\footing2.ifc")
#
# model = ifcopenshell.open("C:\\Users\\Aiyu\\Desktop\\footing2.ifc")
# for element in model.by_type("IfcBuildingElement"):
#     if element.GlobalId != footing.GlobalId:
#         model.remove(element)
# model.remove(model.by_type("IfcGrid")[0])
# model.write("C:\\Users\\Aiyu\\Desktop\\footing2.ifc")
# calculate weight
print(footing.get_info())
matrix = ifcopenshell.util.placement.get_local_placement(footing.ObjectPlacement)
print(matrix[:,3][:3])
