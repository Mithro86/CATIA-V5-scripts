import math

t = input("Enter part thickness: ")
t = float(t)

ratio = input("Enter material ratio: ")
ratio = float(ratio)

y = t*ratio

x = y/2
f = math.degrees(math.atan(t/x))
b = (90-f)*2
r = x/math.sin(math.radians(b))
print(f"Maxium sphere diameter is: {round(r*2, 2)}")