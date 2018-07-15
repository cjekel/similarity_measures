import numpy as np
import matplotlib.pyplot as plt
import similaritymeasures
reload(similaritymeasures)

x1 = np.linspace(0.0, 1.0, 100)
y1 = np.ones(100)*2
x2 = np.linspace(0.0, 1.0, 50)
y2 = np.ones(50)

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

area1 = similaritymeasures.area_between_two_curves(curve1, curve2)
cl1 = similaritymeasures.curve_length_measure(curve1, curve2)
df1 = similaritymeasures.frechet_dist(curve1, curve2)
pcm1 = similaritymeasures.pcm(curve1, curve2)

x1 = np.linspace(0.0, 1.0, 100)
y1 = x1
x2 = np.linspace(0.0, 1.0, 50)
y2 = x2+1.0

plt.figure()
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.show()
curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

area2 = similaritymeasures.area_between_two_curves(curve1, curve2)
cl2 = similaritymeasures.curve_length_measure(curve1, curve2)
df2 = similaritymeasures.frechet_dist(curve1, curve2)
pcm2 = similaritymeasures.pcm(curve1, curve2)