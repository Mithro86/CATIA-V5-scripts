from pycatia import catia
import scipy.optimize as optimize

caa = catia()
documents = caa.documents
document = caa.active_document
part = document.part
parameters = part.parameters

free_parameter = parameters.item("Length.1")
optimized_parameter = parameters.item("Volume.1")

target_value = 2.5e-07

def objective_function(x):
    free_parameter.value = x
    part.update_object(optimized_parameter)

    return abs(target_value - optimized_parameter.value)

result = optimize.minimize_scalar(objective_function, bounds=(3, 15), method='bounded')

print(result)
