# Using pywinauto to access silhouette command.

from pycatia import catia
from pywinauto.application import Application

caa = catia()
documents = caa.documents
document = caa.active_document
part = document.part
hbs = part.hybrid_bodies
hb = hbs.item("Geometrical Set.1")

# Set hb as working object.
part.in_work_object = hb

# Define selection and clear.
selection = document.selection
selection.clear()

# Select inputs before starting command.
selection.add(part.main_body)
selection.add(part.origin_elements.plane_yz)

# Start command
caa.start_command("Silhouette")

app = Application().connect(title="Silhouette Definition", timeout=20) # Wait max 20s for the dialog to appear.
window = app.dialog
internal = window.Internal
internal.uncheck_by_click() # Uncheck internal option.
inner = window.Inner
inner.uncheck_by_click() # Uncheck inner option.
ok = window.OK
ok.click()
