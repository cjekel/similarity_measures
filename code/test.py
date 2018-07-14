import numpy as np
import matplotlib.pyplot as plt
import similarity_measures
reload(similarity_measures)

x1 = np.linspace(0.0, 1.0, 100)
y1 = np.zeros(100)
x2 = np.linspace(0.0, 1.0, 50)
y2 = np.ones(50)

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

area = similarity_measures.area_between_two_curves(curve1, curve2)