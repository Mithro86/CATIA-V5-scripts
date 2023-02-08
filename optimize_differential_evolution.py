# https://docs.scipy.org/doc/scipy/reference/optimize.html

from pycatia import catia
import scipy.optimize as optimize

caa = catia()
documents = caa.documents
document = caa.active_document
part = document.part
parameters = part.parameters

p1 = parameters.item("Length.1")
p2 = parameters.item("Length.2")
p3 = parameters.item("Length.3")
optimized_parameter = parameters.item("Volume.1")

target_value = 1e-006

def objective_function(x):
    a, b, c = x

    p1.value = a
    p2.value = b
    p3.value = c

    part.update_object(optimized_parameter)

    return abs(target_value - optimized_parameter.value)

bounds = [[9, 11], [9, 11], [9, 11]]

result = optimize.differential_evolution(objective_function, bounds, maxiter=100, atol=0.01)

print(result)
