# Extract edges for surface.

from pycatia import catia

caa = catia()
documents = caa.documents
document = caa.active_document
part = document.part
hbs = part.hybrid_bodies
hb = hbs.item("Geometrical Set.1")
hs = hb.hybrid_shapes

hsf = part.hybrid_shape_factory

surface = hs.item("Extract.1")

selection = document.selection

selection.clear()
selection.add(surface)

selection.search("Topology.Edge;sel")

hb = hbs.item("Geometrical Set.2")

stop = selection.count + 1

for i in range(1, stop):
    edge = selection.item(i).value
    extract = hsf.add_new_extract(edge)
    hb.append_hybrid_shape(extract)

part.update()
