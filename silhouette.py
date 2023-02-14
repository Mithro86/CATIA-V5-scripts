# Create part silhouette with start_command and pywinauto

from pycatia import catia
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError
from time import sleep

caa = catia()
document = caa.active_document

selection = document.selection

part = document.part
hsf = part.hybrid_shape_factory
hbs = part.hybrid_bodies

# Define geoset and set as in work object
hb = hbs.item("Geometrical Set.1")
part.in_work_object = hb

# Add inputs for silhouette to selection
selection.clear()
selection.add(part.main_body)
selection.add(part.origin_elements.plane_yz)

# Start silhouette command
caa.start_command("Silhouette")

# Control silhouette command with pywinauto
app = Application().connect(title="Silhouette Definition", timeout=30)
window = app.dialog
window.move_window(x=8000) # Move window out of view
internal_option = window.Internal
internal_option.uncheck_by_click()
inner_option = window.Inner
inner_option.uncheck_by_click()
ok_button = window.OK
ok_button.click()

# Get silhouette object and create reference
silhouette = hb.hybrid_shapes.item(hb.hybrid_shapes.count)
reference = part.create_reference_from_object(silhouette)

# Check if object is updated or wait until true
check_done = part.is_up_to_date(silhouette)

while not check_done:
	sleep(1)
	check_done = part.is_up_to_date(silhouette)

# Close "Multi-Result  Management" and/or "Warnings" window
try:
	app = Application().connect(title="Multi-Result  Management", timeout=0.5)
	window = app.Dialog
	window.close()
except (ElementNotFoundError, TimeoutError):
	pass

try:
	app = Application().connect(title="Warnings", timeout=0.5)
	window = app.Dialog
	window.close()
except (ElementNotFoundError, TimeoutError):
	pass

# Create datums and append to geoset
multi_result_datums = hsf.add_new_datums(reference)

for multi_result_datum in multi_result_datums:
	hb.append_hybrid_shape(multi_result_datum)

# Delete silhouette operation
hsf.delete_object_for_datum(reference)

part.update()
