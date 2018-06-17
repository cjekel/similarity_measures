import numpy as np
import re
#   read the variables
beta = []
with open('VariableDefs','r') as out:
    #for line in islice(out, 9):
    #    pass
    for line in out:
        a = re.split('=|;', line)
        beta.append(float(a[1]))

#   define a function to compute x and y values given betas
def getXY(betas):
    x1 = np.linspace(0,1.0,num=100)
    xEnd = np.log((1.0 + (2.0*np.exp(1.0)) - np.exp(1.0))/2.0)
    x2 = np.linspace(1.0,xEnd, num=50)
    
    y1 = np.exp(betas[0]*x1) + betas[1]
    y2 = 2.0*np.exp(betas[2]*x2) -2.0*np.exp(betas[3]) + np.exp(1.0) -1.0
    x = np.concatenate((x1,x2))
    y = np.concatenate((y1,y2))
    return x,y

xi2, eta2 = getXY(beta)

##   load the test data
#xi1, eta1 = asc.readTestData('test2.txt')   
#
##   load the history data
#xi2, eta2 = asc.readHistoryData('history.2')

xi1, eta1 = np.load('true.npy')
#xi2, eta2 = np.load('noise.npy')

testData = np.zeros([len(xi1), 2])
historyData = np.zeros([len(xi2), 2])
testData[:,0] = xi1
testData[:,1] = eta1
historyData[:, 0] = xi2
historyData[:, 1] = eta2

import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()
    
# Set up our R namespaces
R = rpy2.robjects.r
DTW = importr('dtw')

# Calculate the alignment vector and corresponding distance
alignment = R.dtw(testData, historyData, keep=True)
area = alignment.rx('distance')[0][0]

np.savetxt('area.txt', np.sum(area)[None], fmt='%.10f')
print("N o r m a l")
