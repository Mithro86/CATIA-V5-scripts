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
            product = document.product

            ref_part_number = product.part_number
            ref_revision = product.revision
            ref_definition = product.definition
            ref_nomenclature = product.nomenclature

            copy_b_checker = document.selection
            vis_properties = copy_b_checker.vis_properties

            color_list =[]
            body_count = 0
            
            # filter out empty or hidden bodies. if not get color and append to list.
            for body in bodies:
                if body.shapes.count<1:
                    body.name = "skip"
                else:
                    copy_b_checker.clear()
                    copy_b_checker.add(body)
                    vis_value = vis_properties.get_show()
                    real_color = vis_properties.get_real_color()
                    copy_b_checker.clear()

                    if vis_value[1] ==1:    
                        body.name = "skip"
                    else:
                        color_list.append(real_color)
                        body_count+=1
                        
            # if there is something to copy, else go ahead with next file.
            if body_count>0:
                copy_b = document.selection
                copy_b.clear()

                for body in bodies:
                    if body.name=="skip":
                        continue
                    else:
                        copy_b.add(body)

                copy_b.copy()
                copy_b.clear()          

                # create new part and paste as result.
                tar_doc = documents.add("Part")
                document = caa.active_document
                copy_b = document.selection
                part = document.part

                product = document.product

                product.part_number = ref_part_number
                product.revision = ref_revision
                product.definition = ref_definition
                product.nomenclature = ref_nomenclature

                copy_b.add(part.main_body)
                copy_b.paste_special("CATPrtResultWithOutLink")
                copy_b.clear()

                part.update()
                
                bodies = part.bodies

                copy_color = document.selection
                vis_properties = copy_color.vis_properties
                copy_color.clear()

                i=0
                # loop trough bodies and set color.
                for body in bodies:
                    if body.name=="PartBody":
                        continue
                    else:
                        copy_color.add(body)
                        vis_properties.set_real_color(color_list[i][1], color_list[i][2], color_list[i][3], 1)
                        copy_color.clear()
                        i+=1
                # close reference catpart and overwrite with new catpart.
                ref_doc.close()
                document.save_as(file_name, overwrite= True)
                tar_doc.close()
            else:
                ref_doc.close()

for root, dirs, files in os.walk(source_directory):

    for file in files:

        # only get dat files.
        if os.path.splitext(file)[1] == ".dat":
            # create filename with path.
            file_name = os.path.join(source_directory, file)
            os.remove(file_name)
print("*********** DONE ***********")
