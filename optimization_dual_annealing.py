# Optimize free parameter to reach target value of optimized paramter.

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
    free_parameter.value = x[0]
    part.update_object(optimized_parameter)

    return abs(target_value - optimized_parameter.value)

bounds = [(3, 15)]

result = optimize.dual_annealing(objective_function, bounds, seed=0, maxiter=100)

print(result)
