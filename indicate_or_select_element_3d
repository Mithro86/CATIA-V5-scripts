"""
    Example - indicate_or_select_element_3d - xxx:
    
    Creates plane parallel to screen in viewpoint origin. 
    Loops indicate_or_select_element_3d until mouse is clicked, while checking that sight direction is not changed. 
    Creates projection point on surface at clicked position or if point or vertex is selected, a point in that position.

	Requirements: CATIA runnig. A Part with a geometrical set named "Geometrical Set.1" with a surface "Extract.1" inside.

"""

##########################################################
# insert syspath to project folder so examples can be run.
# for development purposes.
import os
import sys

sys.path.insert(0, os.path.abspath('..\\pycatia'))
##########################################################


from pycatia import catia

caa = catia()
document = caa.active_document
part = document.part
hsf = part.hybrid_shape_factory
hbs = part.hybrid_bodies
hb = hbs.item("Geometrical Set.1")
hs = hb.hybrid_shapes

def sight_coords():
    #get viewer object
    active_window = caa.active_window
    active_viewer = active_window.active_viewer
    
    #get viewpoint object
    view_point_3D = active_viewer.create_viewer_3d().viewpoint_3d

    sight = view_point_3D.get_sight_direction()
    
    return sight

def scr_pln():
    #get viewer object
    active_window = caa.active_window
    active_viewer = active_window.active_viewer
    
    #get viewpoint object
    view_point_3D = active_viewer.create_viewer_3d().viewpoint_3d

    #get viewpoint coords
    viewpoint_coords = view_point_3D.get_origin()

    #create viewpoint
    origin_point = hsf.add_new_point_coord(viewpoint_coords[0], viewpoint_coords[1], viewpoint_coords[2])

    #create reference to viewpoint
    origin_point_ref = part.create_reference_from_object(origin_point)

    #get sight direction coords
    sight_dir_coords = sight_coords()

    #create sight direction
    sight_dir = hsf.add_new_direction_by_coord(sight_dir_coords[0], sight_dir_coords[1], sight_dir_coords[2])

    #create sight direction line
    sight_dir_line = hsf.add_new_line_pt_dir(origin_point_ref, sight_dir, 0, 20, False)

    #create reference to sight direction line
    sight_dir_line_ref = part.create_reference_from_object(sight_dir_line)

    #reate sight direction plane
    scr_pln = hsf.add_new_plane_normal(sight_dir_line_ref, origin_point_ref)
    hb.append_hybrid_shape(scr_pln)

    #update
    part.update_object(scr_pln)
    
    return scr_pln


#get plane parallel to screen
scr_pln_res = scr_pln()

#create reference to sigh direction plane
scr_pln_ref = part.create_reference_from_object(scr_pln_res)

#define selection
selection = document.selection
selection.clear()

#define indicate or select element 3D
status = "MouseMove"
#set whats allowed to select
input_type = ("Point", "Vertex")

selection.clear()

status = selection.indicate_or_select_element_3d(scr_pln_res, "Select a point or click to locate the point", input_type, False, False, True)

#get in value for sight direction coords
in_coords = sight_coords()
in_coordx = in_coords[0]

#do loop while checking if viewer direction is modified
while (status[0] == "MouseMove"):
    
    out_coords = sight_coords()
    out_coordx = out_coords[0]

    if in_coordx == out_coordx:
        status = selection.indicate_or_select_element_3d(scr_pln_res, "Select a point or click to locate the point", input_type, False, False, True)
    else:
        hsf.delete_object_for_datum(scr_pln_ref)
        scr_pln_res = scr_pln()
        scr_pln_ref = part.create_reference_from_object(scr_pln_res)
        status = selection.indicate_or_select_element_3d(scr_pln_res, "Select a point or click to locate the point", input_type, False, False, True)
        in_coords = sight_coords()
        in_coordx = in_coords[0]
    
    if not status[0] == "MouseMove":
        break

#if bailing
if status[0] == "Cancel" or status[0] == "Undo" or status[0] == "Redo":
	hsf.delete_object_for_datum(scr_pln_ref)

#if selecting existing point or vertex
elif status[1]:
	existing_point = selection.item2(1)

	coords = existing_point.get_coordinates()

	vertex_point = hsf.add_new_point_coord(coords[0], coords[1], coords[2])
	    
	hb.append_hybrid_shape(vertex_point)

	selection.clear()

	part.update_object(vertex_point)

	vertex_point_ref = part.create_reference_from_object(vertex_point)

	vertex_point_datum = hsf.add_new_point_datum(vertex_point_ref)

	hb.append_hybrid_shape(vertex_point_datum)

	part.update_object(vertex_point_datum)

	hsf.delete_object_for_datum(vertex_point_ref)
	hsf.delete_object_for_datum(scr_pln_ref)

else:    
	try:
		#create screen point  
		scr_point = hsf.add_new_point_coord(status[3][0], status[3][1], status[3][2])
		hb.append_hybrid_shape(scr_point)

		#update
		part.update_object(scr_point)

		#create reference to screen point       
		scr_point_ref = part.create_reference_from_object(scr_point)

		#project on surface      

		# path to surface
		project_surface = hs.item("Extract.1")

		#create reference to surface
		project_surface_ref = part.create_reference_from_object(project_surface)
		
		projected_point = hsf.add_new_project(scr_point_ref, project_surface_ref)
		projected_point_ref = part.create_reference_from_object(projected_point)

	    #get sight direction coords
		sight_dir_coords = sight_coords()

	    #create sight direction
		sight_dir = hsf.add_new_direction_by_coord(sight_dir_coords[0], sight_dir_coords[1], sight_dir_coords[2])
	    
	    #need to import projection?
		projected_point.normal = False
		projected_point.direction = sight_dir

		hb.append_hybrid_shape(projected_point)

		part.update_object(projected_point)

		projected_point_datum = hsf.add_new_point_datum(projected_point_ref)

		hb.append_hybrid_shape(projected_point_datum)

		part.update_object(projected_point_datum)

		# Delete history
		hsf.delete_object_for_datum(projected_point_ref)
		hsf.delete_object_for_datum(scr_point_ref)
		hsf.delete_object_for_datum(scr_pln_ref)
	except:
		hsf.delete_object_for_datum(projected_point_ref)
		hsf.delete_object_for_datum(scr_point_ref)
		hsf.delete_object_for_datum(scr_pln_ref)

		buttons = 0
		result = caa.message_box("Aim better ;)", buttons=buttons, title="You missed.")
