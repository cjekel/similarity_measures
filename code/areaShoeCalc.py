import numpy as np
from itertools import islice
#import matplotlib.pyplot as plt
from scipy.spatial import distance

#   library for computing the area between the two datasets

#    Define a function to compute the polynomial area via the shoelace formula   
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
#    Define a fucntion that performs all of the cross producs of a quadralteral
#   and returns true if the quadraleral is a simple quadralteral ie non-complex
#   given the vectors of the quadralateral
def isSimpleQuad(ab, bc, cd, da):
    #   Compute all four cross products
    temp0 = np.cross( ab, bc)
    temp1 = np.cross( bc, cd)
    temp2 = np.cross( cd, da)
    temp3 = np.cross( da, ab)
    cross = np.array([ temp0, temp1, temp2, temp3])
    #   See that cross products are greater than or equal to zero
    crossTF = cross >= 0
    #   if the cross products are majority false, re compute the cross rpoducts
    #   Because they don't necesarrily need to lie in the same 'Z' direction
    if sum(crossTF) <= 1:
        crossTF = cross <= 0
    if sum(crossTF) > 2:
        return True
    else:
        return False
  
#   Define a funtion to arrange four points into a non-convex quadralateral
def makeQuad( x, y):
    #   check to see if the provide point order is valid
    #   I need to get the values of the cross products of ABxBC, BCxCD, CDxDA, 
    #   DAxAB, thus I need to create the following arrays AB, BC, CD, DA

    AB = [ x[1]-x[0], y[1]-y[0] ]
    BC = [ x[2]-x[1], y[2]-y[1] ]
    CD = [ x[3]-x[2], y[3]-y[2] ]
    DA = [ x[0]-x[3], y[0]-y[3] ]

    isQuad = isSimpleQuad(AB, BC, CD, DA)
    
    if isQuad == False:
        #   attempt to rearange the first two points
        x[1], x[0] = x[0], x[1]
        y[1], y[0] = y[0], y[1]
        AB = [ x[1]-x[0], y[1]-y[0] ]
        BC = [ x[2]-x[1], y[2]-y[1] ]
        CD = [ x[3]-x[2], y[3]-y[2] ]
        DA = [ x[0]-x[3], y[0]-y[3] ]
        
        isQuad = isSimpleQuad(AB, BC, CD, DA)
        
        if isQuad == False:
            #   place the second and first points back where they were, and swap
            #   the second and third points
            x[2], x[0], x[1] = x[0], x[1], x[2]
            y[2], y[0], y[1] = y[0], y[1], y[2]
            AB = [ x[1]-x[0], y[1]-y[0] ]
            BC = [ x[2]-x[1], y[2]-y[1] ]
            CD = [ x[3]-x[2], y[3]-y[2] ]
            DA = [ x[0]-x[3], y[0]-y[3] ]
            
            isQuad = isSimpleQuad(AB, BC, CD, DA)
    #plotX = [ x[0], x[1], x[2], x[3], x[0]]
    #plotY = [ y[0], y[1], y[2], y[3], y[0]]
    #plt.plot( plotX, plotY, '--b',label=r'$\xi$1$\eta$1')

    area = PolyArea( x, y)

    return area

def readTestData(fileName):
    x = []
    y = []
    with open(fileName,'r') as out:
        #for line in islice(out, 9):
        #    pass
        for line in out:
            a = line.split(',')
            #while '' in a: a.remove('')    
            X = float(a[0])
            Y = float(a[1]) 
            x.append(X)
            y.append(Y)
    return np.array(x), np.array(y)

def readHistoryData(fileName):
    x = []
    y = []
    with open(fileName,'r') as out:
        for line in islice(out, 6):
            pass
        for line in out:
            a = line.split(' ')
            if len(a) > 1:
                while '' in a: a.remove('')    
                X = float(a[0])
                Y = float(a[1])
                x.append(X)
                y.append(Y)
    return np.array(x), np.array(y)






#   get the arc length of a dataset where dataSet is of the form
#   dataSet = np.array([[x11, x21, ..., xn1],
#                [x12, x22, ..., xn2],
#                ...
#                [x1m, x2m, ..., xnm]])
#   essentially this will return the arc length of a dataset
def getArcLength(dataSet):
    #   split the dataset into two discrete datasets, each of length m-1
    m = len(dataSet)
    a = dataSet[0:m-1, :]
    b = dataSet[1:m, :]
    #   use scipy.spatial to compute the euculidean distance
    dataDistance = distance.cdist(a,b, 'euclidean')
    #   this returns a matrix of the euclidiean distance betweena all points
    #   the arc lenght is simply the sum of the diagonal of this matrix
    arcLengths = np.diagonal(dataDistance)
    arcLength = sum(arcLengths)
    return arcLength, arcLengths


#   define a function to discritze data into smaller portions for aera sum
#   where factors is the scale factor of the number of increase data points
#   if factor = 10, then this creates 9 times the number of data points, 
#   plus the original data points
#   len(new) = 9*(len(old)-1) + len(old)
def discretizeData(data, factor):
    newLength = ((factor-1)*(len(data)-1))+len(data)
    newData = np.zeros([int(newLength), 2])
    xData = []
    yData = []
    for i,j in enumerate(data[0:len(data)-1,:]):
        #   create a linear interpolation model between the 
        newX = np.arange(j[0], data[i+1,0], (data[i+1,0]-j[0])/factor)
        #   the interpolation model messes up if x2 < x1 so we do a quick check
        if j[0] < data[i+1,0]:
            newY = np.interp(newX, [j[0], data[i+1,0]], [j[1], data[i+1,1]])
        else:
            newY = np.interp(newX, [data[i+1,0], j[0]], [data[i+1,1], j[1]])
        for k in range(0,len(newX)):
            xData.append(newX[k])
            yData.append(newY[k])
    xData.append(data[-1,0])
    yData.append(data[-1,1])
    newData[:,0] = xData
    newData[:,1] = yData
    return newData
    
def calcAreaOfTwoDatasets(testData, historyData):
    #   Calculate the area between two datasets using very small quadralaterals
    #   Consider the test data to be data from an experimental test
    #   Consider the history data to be the result from the numerical model
    #   the len(testData) > len(historyData)
    #
    #   Example on formatting the test and history data: 
    ##   load the test data
    #xi1, eta1 = readTestData('test6.txt')   
    #
    ##   load the history data
    #xi2, eta2 = readHistoryData('history.5')
    #
    #testData = np.zeros([len(xi1), 2])
    #historyData = np.zeros([len(xi2), 2])
    #testData[:,0] = xi1
    #testData[:,1] = eta1
    #historyData[:, 0] = xi2
    #historyData[:, 1] = eta2
    arcTestData, arcsTestData = getArcLength(testData)
    arcHistoryData, arcsHistoryData = getArcLength(historyData)
    
    #   let's find the largerst gap between point  in the history data, and then
    #   linearlly interpolate between these points such that the thistory data 
    #   becomes the same length as the test data
    for i in range(0,len(testData)-len(historyData)):
        a = historyData[0:len(historyData)-1,0]
        b = historyData[1:len(historyData),0]
        c = np.abs(a-b)
        nIndex = np.argmax(c)
        newX = (b[nIndex] + a[nIndex])/2.0
        #   the interpolation model messes up if x2 < x1 so we do a quick check
        if a[nIndex] < b[nIndex]:
            newY = np.interp(newX, [a[nIndex], b[nIndex]], [historyData[nIndex,1], historyData[nIndex+1,1]])
        else:
            newY = np.interp(newX, [b[nIndex], a[nIndex]] , [historyData[nIndex+1,1], historyData[nIndex,1]])
        historyData = np.insert(historyData,nIndex+1,999.9,axis=0)
        historyData[nIndex+1,0] = newX
        historyData[nIndex+1,1] = newY
    
    #   I want my evaulation points of both curves to be equallys spaced along the 
    #    arc length of each curve. This means that if I want to evalute 155 times
    #   (len(testData)) then the proportional space of each data point should be 
    #   arc length / 155
    
    sTestData = arcTestData/ len(testData)
    sHistoryData = arcHistoryData / len(testData)
            
    #testDataDisc = discretizeData(testData, 10.0)
    ##   compute a history factor such that the rescaled history data has the same
    #histF = ((len(testDataDisc) - len(historyData)) / (len(historyData) -  1.0))+1.0
    #   number of points as 
    #historyDataDisc = discretizeData(historyData, 10.0)
    testDataDisc = testData.copy()
    historyDataDisc = historyData.copy()
        
    ##   plot the new datapoints
    #
    #plt.figure()
    #plt.plot(testData[:,0],testData[:,1], '-xk')
    #plt.plot(testDataDisc[:,0], testDataDisc[:,1], '-ok')
    #plt.plot(historyData[:, 0],historyData[:, 1], '-xr')
    #plt.plot(historyDataDisc[:,0], historyDataDisc[:,1], '-or')

    
    
    #   Calculate the quadralateral area, by looping through all of the quads
    area = []
    for i in range(1, len(testDataDisc)):
        tempX = [testDataDisc[i-1,0], testDataDisc[i,0], historyDataDisc[i,0], historyDataDisc[i-1,0]]
        tempY = [testDataDisc[i-1,1], testDataDisc[i,1], historyDataDisc[i,1], historyDataDisc[i-1,1]]
        area.append(makeQuad( tempX, tempY))

    #plt.show()
    return area


