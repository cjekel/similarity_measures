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
xi1, eta1 = np.load('true.npy')


def get_length(x,y):
    n = len(x)
    xmax = np.max(np.abs(x))
    ymax = np.max(np.abs(y))
    l = np.zeros(n)
    l[0]= 0.0
    l_sum = np.zeros(n)
    l_sum[0] = 0.0
    for i in range(0,n-1):
        l[i+1] = np.sqrt((((x[i+1]-x[i])/xmax)**2)+(((y[i+1]-y[i])/ymax)**2))
        l_sum[i+1] = l_sum[i]+l[i+1]
    return l, np.sum(l), l_sum
def get_r(x_e, y_e, x_c, y_c):
    le, le_nj, le_sum = get_length(x_e,y_e)
    lc, lc_nj, lc_sum = get_length(x_c,y_c)
    xmean = np.mean(x_e)
    ymean = np.mean(y_e)
    n = len(x_e)
    r_sq = np.zeros(n)
    for i in range(0,n):
        lieq = le_sum[i]*(lc_nj/le_nj)
        xtemp = np.interp(lieq, lc_sum, x_c)
        ytemp = np.interp(lieq, lc_sum, y_c)

        r_sq[i] = np.log(1.0 + (np.abs(xtemp-x_e[i])/xmean))**2 + \
            np.log(1.0 + (np.abs(ytemp-y_e[i])/ymean))**2
    return np.sqrt(np.sum(r_sq))
r = get_r(xi1, eta1, xi2, eta2)
np.savetxt('area.txt', r[None], fmt='%.10f')
print("N o r m a l")
