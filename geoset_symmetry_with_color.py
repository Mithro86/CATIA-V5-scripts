import os
import sys

from pycatia.enumeration.enumeration_types import cat_vis_property_status

sys.path.insert(0, os.path.abspath("..\\pycatia"))
from pycatia import catia

caa = catia()

document = caa.active_document
product = document.product
part = document.part
hybrid_bodies = part.hybrid_bodies
selection = document.selection
vis_properties = selection.vis_properties
hsf = part.hybrid_shape_factory


selection.clear()
selection_set = selection.select_element2(
    ("HybridBody",), "Select geometrical set...", False
)

if selection_set == "Normal":
    selected_set_name = selection.item2(1).value.name
else:
    sys.exit()

selection.search("CATPrtSearch.Surface,sel")

# hybrid_body = hybrid_bodies.get_item_by_name(selected_set_name)
# shapes = hybrid_body.hybrid_shapes

new_set = hybrid_bodies.add()
new_set.name = f"Symmetry_of_{selected_set_name}"

zx_plane = part.origin_elements.plane_zx

obj_list = []

for i in range(selection.count2):
    item = selection.item2(i + 1).value
    obj_list.append(item)

selection.clear()

for obj in obj_list:
    # add to selection
    selection.add(obj)

    # check if obj hidden
    vis_state = vis_properties.get_show()

    # skip if true
    if vis_state[1] == 1:
        selection.clear()
        continue
    else:
        # get color of obj
        real_color = vis_properties.get_real_color()
        s, r, g, b = real_color

        # hide obj
        # vis_properties.set_show(1)

        # symmetry of obj
        reference = part.create_reference_from_object(obj)
        sym_obj = hsf.add_new_symmetry(reference, zx_plane)
        new_set.append_hybrid_shape(sym_obj)

        part.update()

        # set color of symmetry
        selection.clear()
        selection.add(sym_obj)
        vis_properties.set_real_color(r, g, b, 1)

        # set name
        sym_obj.name = f"Symmetry_of_{obj.name}"

        selection.clear()
