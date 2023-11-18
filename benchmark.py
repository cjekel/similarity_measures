# https://github.com/nucccc/benchmark_similarity_measures/blob/main/run_benchmark.py
import similaritymeasures
import torch
import json
import timeit
import numpy as np

benchmark_result : dict[str:dict[str:any]] = dict()

x1 = np.linspace(0.0, 1.0, 500)
y1 = np.ones(500)*2
x2 = np.linspace(0.0, 1.0, 250)
y2 = np.ones(250)

np.random.seed(1212121)
curve_a_rand = np.random.random((100, 2))
curve_b_rand = np.random.random((90, 2))

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

curve1t = torch.from_numpy(curve1)
curve2t = torch.from_numpy(curve2)

r1 = 10
r2 = 100
theta = np.linspace(0.0, 2.0*np.pi, 500)
x1 = np.cos(theta)*r1
x2 = np.cos(theta)*r2
y1 = np.sin(theta)*r1
y2 = np.sin(theta)*r2
curve5 = np.array((x1, y1)).T
curve6 = np.array((x2, y2)).T
curve5t = torch.from_numpy(curve5)
curve6t = torch.from_numpy(curve6)


def run_dtw_c1_c2():
    return similaritymeasures.dtw(curve1, curve2)

def run_dtw_c5_c6():
    return similaritymeasures.dtw(curve5, curve6)

def run_dtw_c1_c2t():
    return similaritymeasures.dtwtorch(curve1t, curve2t)

def run_dtw_c5_c6t():
    return similaritymeasures.dtwtorch(curve5t, curve6t)

bnchmks = {
    'dtw_c1_c2':run_dtw_c1_c2,
    'dtw_c5_c6':run_dtw_c5_c6,
    'dtw_c1_c2t':run_dtw_c1_c2t,
    'dtw_c5_c6t':run_dtw_c5_c6t,
}

n_repeats = 50
n_runs = 20

for name, func in bnchmks.items():

    times_list = timeit.repeat(func, repeat = n_repeats, number = n_runs)

    total = sum(times_list)
    avg = total / len(times_list)

    func_result = {
        'times_list':times_list,
        'total':total,
        'avg':avg
    }

    benchmark_result[name] = func_result

result_encoded = json.dumps(benchmark_result)
print(result_encoded)
with open('benchmark.json', 'w') as f:
    json.dump(result_encoded, f)
# with open('benchmark_no_jit.json', 'w') as f:
#     json.dump(result_encoded, f)
