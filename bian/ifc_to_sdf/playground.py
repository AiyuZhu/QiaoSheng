import ifcopenshell

# load model
model = ifcopenshell.open("..\\..\\Case_for_RC\\BIM_model\\IFC_model\\unit_without_beam_in_room.ifc")

# get all building elements in ifc
# for element in model.by_type("IfcBuildingElement"):
#     print(element)

footing = model.by_type("IfcFooting")[0]
print(model.traverse(footing))

# split ifc element
# new_model = ifcopenshell.file()
# new_model.add(footing)
# new_model.write("C:\\Users\\Aiyu\\Desktop\\footing.ifc")


