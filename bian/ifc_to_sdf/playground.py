import os
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
from ifcopenshell.api import run
import materials

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
new_model = ifcopenshell.file()
# container = ifcopenshell.util.element.get_container(footing)
# run("spatial.assign_container", new_model, relating_structure=container, product=footing)
new_model.add(contained)
# new_model.add(footing)
relation = model.by_type("IfcRelaggregates")
for i in relation:
    new_model.add(i)
# get all building elements in ifc
new_model.write("C:\\Users\\31613\\Desktop\\footing.ifc")

model = ifcopenshell.open("C:\\Users\\31613\\Desktop\\footing.ifc")
for element in model.by_type("IfcBuildingElement"):
    if element.GlobalId != footing.GlobalId:
        model.remove(element)
model.remove(model.by_type("IfcGrid")[0])
model.write("C:\\Users\\31613\\Desktop\\footing.ifc")
# calculate weight
# print(footing.get_info())
# matrix = ifcopenshell.util.placement.get_local_placement(footing.ObjectPlacement)
# print(matrix[:,3][:3])

# use ifcconvert to convert ifc to collada
# collada_path = element_meshes + '\\{}.dae'.format(element_name)
element_path = 'C:\\Users\\31613\\Desktop\\footing.ifc' # should input by user
collada_path = 'C:\\Users\\31613\\Desktop\\footing.dae' # should input by user
ifc_converter_path = '..\\ifc_to_sdf\\IfcConvert.exe'
convert_path = '{} {} {}'.format(ifc_converter_path, element_path, collada_path)
os.popen(convert_path)

# Get all properties and quantities of the wall, including inherited type properties
psets = ifcopenshell.util.element.get_psets(footing)
print(psets)

# Get only properties and not quantities
print(ifcopenshell.util.element.get_psets(footing, psets_only=True))

# Get only quantities and not properties
quan = ifcopenshell.util.element.get_psets(footing, qtos_only=True)
vol = next(iter(quan.values()))['NetVolume']
print(vol)
den = materials.carbon_steel.density
print(den)
weight = vol * den
print(weight)
# for i in quan.values():
#     print(i['NetVolume'])