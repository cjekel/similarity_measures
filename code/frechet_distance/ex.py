import numpy as np
import frechet
import cfrechet
# import c_frechet
from time import time
def my_fun(betas):
    x1 = np.linspace(0,1.0,num=100)
    xEnd = np.log((1.0 + (2.0*np.exp(1.0)) - np.exp(1.0))/2.0)
    x2 = np.linspace(1.0,xEnd, num=50)

    y1 = np.exp(betas[0]*x1) + betas[1]
    y2 = 2.0*np.exp(betas[2]*x2) -2.0*np.exp(betas[3]) + np.exp(1.0) -1.0
    x = np.concatenate((x1,x2))
    y = np.concatenate((y1,y2))
    return x, y

# load the test data
xi1, eta1 = np.load('true.npy')
# calculate the new response
x0 = np.random.random(4)
xi2, eta2 = my_fun(x0)

test_data= np.zeros([len(xi1), 2])
new_response = np.zeros([len(xi2), 2])
test_data[:,0] = xi1
test_data[:,1] = eta1
new_response[:, 0] = xi2
new_response[:, 1] = eta2

t0 = time()
fd = frechet.frechetDist(test_data, new_response)
t1 = time()

print('Run time', t1-t0, 'seconds')

t0 = time()
fd = cfrechet.frechetDist(test_data, new_response)
t1 = time()

print('Run time', t1-t0, 'seconds')

# t0 = time()
# fd = c_frechet.frechet(test_data, new_response)
# t1 = time()

# print('Run time', t1-t0, 'seconds')