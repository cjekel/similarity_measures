import numpy as np
from similaritymeasures import frechet_dist
from cy_similaritymeasures import frechet_dist as cy_frechet_dist

#generating data in a way similar to the tests
x1 = np.linspace(0.0, 1.0, 100)
y1 = np.ones(100)*2
x2 = np.linspace(0.0, 1.0, 50)
y2 = np.ones(50)

np.random.seed(1212121)
curve_a_rand = np.random.random((100, 2))
curve_b_rand = np.random.random((90, 2))

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

res = frechet_dist(curve1, curve2)

cy_res = cy_frechet_dist(curve1, curve2)

print(res)
print(cy_res)
print(res == cy_res)