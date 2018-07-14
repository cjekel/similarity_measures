import numpy as np
import matplotlib.pyplot as plt
import similarity_measures
reload(similarity_measures)

x1 = np.linspace(0.0, 1.0, 100)
y1 = np.ones(100)*2
x2 = np.linspace(0.0, 1.0, 50)
y2 = np.ones(50)

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

area = similarity_measures.area_between_two_curves(curve1, curve2)
cl = similarity_measures.curve_length_measure(curve1, curve2)