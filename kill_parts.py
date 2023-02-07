import os

from pycatia import catia

source_directory = "C:/Temp/TCIC_V5_tmp/catuii/"

for root, dirs, files in os.walk(source_directory):

	for file in files:

		# only get CATParts.
		if os.path.splitext(file)[1] == ".CATPart":
			# create filename with path.
			file_name = os.path.join(source_directory, file)

			caa = catia()
			documents = caa.documents
			ref_doc = documents.open(file_name)
			document = caa.active_document
			part = document.part
			bodies = part.bodies
			hybrid_bodies = part.hybrid_bodies
			parameters = part.parameters
			relations = part.relations
			axis_systems = part.axis_systems

			selection = document.selection
			vis_properties = selection.vis_properties

			color_list = []
			body_list = []
			body_count = 0

			bodies_copy = bodies

			# filter out empty or hidden bodies. if not get color and append to list.
			for body in bodies:
				if body.shapes.count<1:
					body.name = "Skip"
				else:
					selection.clear()
					selection.add(body)
					vis_value = vis_properties.get_show()
					real_color = vis_properties.get_real_color()
					selection.clear()

					if vis_value[1] ==1:    
						body.name = "Skip"
					else:
						color_list.append(real_color)
						body_count+=1

			# if there is something to copy, else go ahead with next file.
			if body_count>0:
				selection.clear()

				for body in bodies:
					if body.name == "Skip":
						continue
					else:
						selection.add(body)
						
				selection.copy()

				selection.paste_special("CATPrtResultWithOutLink")
				
				vis_properties.set_real_color(120, 205, 220, 0)
				
				selection.clear()

				part.update()

				body_main = bodies.add()
				body_main.name = "PartBody_Isolated"
				part.main_body = body_main

				
				for body in bodies:
					selection.clear()
					selection.add(body)
					real_color = vis_properties.get_real_color()

					if (real_color[1]!=120) and (real_color[2]!=205) and (real_color[3]!=220):
						
						if body.name=="PartBody_Isolated":
							continue
						else:
							body.name = "Delete"
					else:
						continue
				
					
				selection.clear()

				for body in bodies:
					if body.name == "Delete":
						selection.add(body)
					else:
						continue
					
				#for relation in relations:
				#	selection.add(relation)

				#for parameter in parameters:
				#	selection.add(parameter)

				for axis_system in axis_systems:
					selection.add(axis_system)

				for hybrid_body in hybrid_bodies:
					selection.add(hybrid_body)

				if selection.count > 0:
					selection.delete()

				body_main.name = "PartBody"

				i=0
                # loop trough bodies and set color.
				for body in bodies:
					if body.name=="PartBody":
						continue
					else:
						selection.add(body)
						vis_properties.set_real_color(color_list[i][1], color_list[i][2], color_list[i][3], 0)
						selection.clear()
						i+=1
				part.update()
				document.save()
				document.close()

			else:
				document.close()

for root, dirs, files in os.walk(source_directory):

    for file in files:

        # only get dat files.
        if os.path.splitext(file)[1] == ".dat":
            # create filename with path.
            file_name = os.path.join(source_directory, file)
            os.remove(file_name)
print("Killing finished!")
