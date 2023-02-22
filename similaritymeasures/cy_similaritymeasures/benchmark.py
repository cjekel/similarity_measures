'''
just a quick benchmaerking script to showcase cythonized vs
non cythonized performances
'''

import timeit
import numpy as np
from similaritymeasures import frechet_dist, dtw
from cy_similaritymeasures import frechet_dist as cy_frechet_dist
from cy_similaritymeasures import dtw as cy_dtw

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

def run_frechet():
    return frechet_dist(curve1, curve2)

def run_cy_frechet():
    return cy_frechet_dist(curve1, curve2)

n_repeats = 5
n_runs = 200

t1 = timeit.repeat(run_frechet, repeat = n_repeats, number = n_runs)

t2 = timeit.repeat(run_cy_frechet, repeat = n_repeats, number = n_runs)
print(t1)
print(t2)

avg = sum(t1) / len(t1)
cy_avg = sum(t2) / len(t2)
improv_pct = (avg - cy_avg) / avg * 100
print('average execution time for non cythonized version: %f' % avg)
print('average execution time for cythonized version: %f' % cy_avg)
print('improvement: %d %%' % improv_pct)

#then i would benchmark dtw

res, _ = dtw(curve1, curve2)

cy_res, _ = cy_dtw(curve1, curve2)

print(res)
print(cy_res)
print(res == cy_res)

def run_dtw():
    return dtw(curve1, curve2)

def run_cy_dtw():
    return cy_dtw(curve1, curve2)

t1 = timeit.repeat(run_dtw, repeat = n_repeats, number = n_runs)

t2 = timeit.repeat(run_cy_dtw, repeat = n_repeats, number = n_runs)
print(t1)
print(t2)

avg = sum(t1) / len(t1)
cy_avg = sum(t2) / len(t2)
improv_pct = (avg - cy_avg) / avg * 100
print('average execution time for non cythonized version: %f' % avg)
print('average execution time for cythonized version: %f' % cy_avg)
print('improvement: %d %%' % improv_pct)