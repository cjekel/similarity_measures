import numpy as np
import matplotlib.pyplot as plt
import math
import time
from scipy.interpolate import interp1d

#   Close figures
plt.close('all')


#   Set up my two curves
x1 = np.linspace(0, 100, num = 100)
x2 = np.linspace(-10, 150, num = 100)

y1 = np.sqrt(x1)
y2 = (0.0005*(x2**2)) + (0.005*x2)

#plt.figure()
#plt.plot(x1, y1,'-k', label='x1y1')
#plt.plot(x2, y2,'-r', label='x2y2')
#plt.legend(loc=2)
#plt.grid(True)
#plt.show()

#   Define a function to normailze a curve's data points
def normalizeCurve(x,y):
    minX = min(x)
    maxX = max(x)
    minY = min(y)
    maxY = max(y)

    xi = (x - minX) / (maxX - minX)
    eta = (y - minY) / (maxY - minY)
    return xi, eta
#   Define a function to normailze the curve data points
def normalizeTwoCurves(x,y,w,z):
    minX = min(x)
    maxX = max(x)
    minY = min(y)
    maxY = max(y)

    xi = (x - minX) / (maxX - minX)
    eta = (y - minY) / (maxY - minY)
    xiP = (w - minX) / (maxX - minX)
    etaP = (z - minY) / (maxY - minY)
    return xi, eta, xiP, etaP 
    
#   normalize the curves
#xi1, eta1 = normalizeCurves(x1,y1)
#xi2, eta2 = normalizeCurves(x2,y2)
xi1, eta1, xi2, eta2 = normalizeTwoCurves(x1, y1, x2, y2)


#plt.figure()
#plt.plot(xi1, eta1, '-k',label=r'$\xi$1$\eta$1')
#plt.plot(xi2, eta2, '-r',label=r'$\xi$2$\eta$2')
###   draw potential areas
##for i in range(1, 2):
##    plt.plot([xi1[i-1], xi2[i-1], xi2[i], xi1[i], xi1[i-1]], [eta1[i-1], eta2[i-1], eta2[i], eta1[i], eta1[i-1]], '-ob')
##    
#plt.legend(loc=2)
#plt.grid(True)
#plt.show()

#   Define a function to compute the segment lengeth of a curve
def segmentLength(xi, eta):
    s = []
    for i in range(1,len(xi)):
        s.append(np.sqrt(((xi[i] - xi[i-1])**2) + ((eta[i] - eta[i-1])**2)))
    #   calc the total length
    t = sum(s)
    return s, t
    
#   Define a function to compute the segment lengeths from a single point
def segmentLengths(xi, eta, x, y):
    s = []
    for i in range(0,len(xi)):
        s.append(np.sqrt(((xi[i] - x)**2) + ((eta[i] - y)**2)))
    #   calc the total length
    t = sum(s)
    return s, t

#   Define a function to compute the distance between two points
def twoPointLength(xi, eta):
    s = np.sqrt(((xi[1] - xi[0])**2) + ((eta[1] - eta[0])**2))
    return s
    
s1, t1 = segmentLength(xi1, eta1)
s2, t2 = segmentLength(xi2, eta2)

#   Check to see 1 is larger than 2, if so 2 becomes 1 
if t1 > t2:
    [xi1old, eta1old] = [xi1, eta1]
    [xi2old, eta2old] = [xi2, eta2]
    [s1old, s2old] = [s1, s2]
    [t1old, t2old] = [t1, t2]
    [xi1, eta1] = [xi2old, eta2old]
    [xi2, eta2] = [xi1old, eta1old]
    [s1, s2] = [s2old, s1old]
    [t1, t2] = [t2old, t1old]
    print 'One was larger than two. Reassigned so that 1 is now 2'
    


#   Define a function which linearlly interpolates between existing points to
#   find new points of which the partial computational method can be applied to
#   with a preset offset
def linInter(x, y, numberOfPoints, desiredSegments, offset):
    f = interp1d(x, y)
    #   Find the first point from the offset
    #   i need to find two possible points of which the offset may exhist
    newX = []
    newY = []
    #   Calculate the length between the first two points, and find the first two points
    for i in range(1,len(x)):
        length= twoPointLength([x[0], x[i]], [y[0], y[i]])
        print length
        if length > offset:
            print length, offset
            print "I've found an acceptable point to search for an interpolation"
            tempX, tempY = linInterpolateTwoPlusOne(x[0], x[i-1], x[i], y[0], y[i-1], y[i], offset, f)
            newX.append(tempX)
            newY.append(tempY)
            
            #   save the position in the loop
            tempI = i
            break
    count = tempI
    print newX
    for i in desiredSegments:
        length2 = twoPointLength([newX[-1], x[count]], [newY[-1], y[count]])
        length1 = twoPointLength([newX[-1], x[count-1]], [newY[-1], y[count-1]])
        if length2 > desiredSegments[len(newX)-1] or length1 > desiredSegments[len(newX)-1]:
            print length2, desiredSegments[len(newX)-1]
            print "I've found an acceptable point to search for an interpolation"
            tempX, tempY = linInterpolateTwoPlusOne(newX[-1], x[count-1], x[count], newY[-1], y[count-1], y[count], desiredSegments[len(newX)-1], f)
            if tempX != 'not' and tempY != 'possible':
                newX.append(tempX)
                newY.append(tempY)
                
            count+=1
        else:
            count+=1
    return newX, newY

#    Define a function to solve for the correct linear interpolation point 
#    provided the start point, and the two points to interpolate between, and
#    the desired lenght
def linInterpolateTwoPlusOne(x0, x1, x2, y0, y1, y2, desiredLength, interpolation):
    #   Check to see if x0,y0 is the same as x1,y1
    if x0 == x1 and y0 == y1:
        length = twoPointLength([x1, x2],[y1, y2])
        x = ((x2-x1)/length)*desiredLength
        y = ((y2-y1)/length)*desiredLength
        #   conver x and y back to original reference
        x = x + x1
        y = y + y1
        length = twoPointLength([x1, x], [y1, y])

        if np.isclose(desiredLength, length) == False:
            print "****** warning ******"
            print "the desired length doesn't equal the new segment length"
        else:
            return x, y


    else:
#        #   Calculate the slope between the two points
#        if (x2 - x1) == 0:
#            print 'Attempting to create black hole'
#            return 'not', 'possible'
#
#        else:
#            m = (y2 - y1) / (x2 - x1)
#        #   solve for the desired A, B, and C
#        A = 1 + (m**2)
#        B = (-2*x0) - (2*m*m*x1) + (2**y1*m) - (2*y0*m)
#        C = -1 * ((desiredLength**2) - (x0**2) - (y0**2) - (m*m*x1*x1) + (2*y1*m*x1) - (y1*y1) - (2*y0*m*x1) + (2*y0*y1))
#        roots = np.roots([A,B,C])
#        #   Determine what roots are in the acceptable range
#        print roots, x1, x2
#        
#        if x1 < roots[0] < x2:
#            x = roots[0]
#            #   Solve for Y
#            #y = ((x-x1)*m) + y1
#            y = interpolation(x)
#            length = twoPointLength([x0, x], [y0, y])
#            if np.isclose(desiredLength, length) == False:
#                print "****** warning ******"
#                print "the desired length doesn't equal the new segment length"
#                return x, y
#
#            else:
#                return x, y
#        elif x1 < roots[1] < x2:
#            x = roots[1]
#            #   Solve for Y
#            #y = ((x-x1)*m) + y1
#            #print y
#            y = interpolation(x)
#            length = twoPointLength([x0, x], [y0, y])
#            print length, desiredLength
#            if np.isclose(desiredLength, length) == False:
#                print "****** warning ******"
#                print "the desired length doesn't equal the new segment length"
#                return x, y
#
#            else:
#                return x, y
#        else:
#            print 'WTF'
#            return 'not', 'possible'
        #   Guess 1000 x values
        tempX = np.linspace(x1, x2, num=1000)
        #   Evalute the 100 y values
        tempY = interpolation(tempX)
        #   Calculate all of the segment lengths
        tempS, tempT = segmentLengths(tempX, tempY, x0, y0)
        #   Find the segment length that is the best match
        tempSegments = abs(tempS - desiredLength)
        print min(tempSegments)
        index = np.argmin(abs(tempS - desiredLength))
        return tempX[index], tempY[index]
    #    
    #print 'wtf...  let us see what happens'
    #py0 = roots[0]*m*(x2-x1)
    #py1 = roots[1]*m*(x2-x1)
    #
    #print 'possible points:'
    #print roots[0], py0
    #print roots[1], py1
    #

#newX, newY = linInter(xi2, eta2, len(xi1), s1, 0.002)
#newS, newT = segmentLength(newX, newY)
#
#for i, j in enumerate(newS):
#    print j, s1[i]
#    
#plt.figure()
#plt.plot(xi1, eta1, '-k',label=r'$\xi$1$\eta$1')
#plt.plot(xi2, eta2, '-r',label=r'$\xi$2$\eta$2')
#plt.plot(newX, newY, 'ok')
#plt.legend(loc=2)
#plt.grid(True)
#plt.show()

#   define a function to find the first point based on a offset
def firstPoint(x, y, offset):
    #   Calculate the length between the first two points, and find the first two points
    for i in range(1,len(x)):
        length= twoPointLength([x[0], x[i]], [y[0], y[i]])
        if length > offset:
            xNew = ((x[i]-x[0])/length)*offset
            yNew = ((y[i]-y[0])/length)*offset
            #   conver x and y back to original reference
            xNew = xNew + x[0]
            yNew = yNew + y[0]
            length = twoPointLength([x[0], xNew], [y[0], yNew])

            if np.isclose(offset, length) == False:
                print "****** warning ******"
                print "the desired length doesn't equal the new segment length"
            else:
                return xNew, yNew
#   define interpolation function to find the correct points within a tolerance
def Inter(x, y, numberOfPoints, desiredSegments, tol, firstPoints):
    f = interp1d(x, y)
    #   I need the first starting point
    newX = [firstPoints[0]]
    newY = [firstPoints[1]]
    for i,j in enumerate(desiredSegments):
        #   Guess 10000 x values
        if newX[-1]+j > max(x):
            tempX = np.linspace(newX[-1], max(x), num=10000)
        else:
            tempX = np.linspace(newX[-1], newX[-1]+j, num=10000)
        ##   Delete any values that are beyond the interplolation range
        #delIndex = []
        #for k,l in enumerate(tempX):
        #    if l > max(x):
        #        delIndex.append(k)
        #        print 'Im deleting stuff'
        #np.delete(delIndex,tempX)
                
        #   Evalute the 10000 y values
        tempY = f(tempX)
        #   Calculate all of the segment lengths
        tempS, tempT = segmentLengths(tempX, tempY, newX[i], newY[i])
        #   Find the segment length that is the best match
        tempSegments = abs(tempS - j)            
        minZ = min(tempSegments)
        if minZ < tol:
            minZ = min(tempSegments)
            index = np.argmin(abs(tempS -j))
            if tempX[index]+(0.5*tempX[index]) > max(x):
                tempX = np.linspace(tempX[index]-(0.5*tempX[index]), max(x), num=10000)
            else: 
                tempX = np.linspace(tempX[index]-(0.5*tempX[index]), tempX[index]+(0.5*tempX[index]), num=10000)
            #delIndex = []
            #for i,j in enumerate(tempX):
            #    if j > max(x):
            #        delIndex.append(i)
            #np.delete(delIndex,tempX)
            tempY = f(tempX)
            tempS, tempT = segmentLengths(tempX, tempY, newX[i], newY[i])
            tempSegments = abs(tempS - j) 


        
        #print min(tempSegments) 

        index = np.argmin(abs(tempS -j))
        newX.append(tempX[index])
        newY.append(tempY[index])
    return newX, newY


for i in range(0,3):
    firstX, firstY = firstPoint(xi2, eta2, (float(i)/2)*(t2-t1))

    start_time = time.time()
    newX, newY = Inter(xi2, eta2, len(xi1), s1, 1e-8, [firstX, firstY])
    print("--- %s seconds ---" % (time.time() - start_time))
    
    newS, newT = segmentLength(newX, newY)
    
    #for i, j in enumerate(newS):
    #    print j, s1[i]
        
    plt.figure()
    plt.plot(xi1, eta1, '-ok',label=r'$\xi$1$\eta$1')
    plt.plot(xi2, eta2, '-r',label=r'$\xi$2$\eta$2')
    plt.plot(newX, newY, 'or')
    
    #   Calculate area
    area = []
    for ip, jp in enumerate(s1):
        d0 = twoPointLength([newX[ip], xi1[ip]], [newY[ip], eta1[ip]])
        d1 = twoPointLength([newX[ip+1], xi1[ip+1]], [newY[ip+1], eta1[ip+1]])
        area.append((d0+d1)*0.5*jp)
        
        #   plot the area box
        plt.plot([newX[ip], xi1[ip], xi1[ip+1], newX[ip+1], newX[ip]], [newY[ip], eta1[ip], eta1[ip+1], newY[ip+1], newY[ip]], '-b')
        plt.title('The PCM error is ' + str(sum(area)))
    print len(area)
    plt.legend(loc=2)
    plt.grid(True)
    plt.show()    

def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0][0] * corners[j][0][1]
        area -= corners[j][0][0] * corners[i][0][1]
    area = abs(area) / 2.0
    return area

#   I need to build the correct list
#   I need to reverse the order of xi1, eta1
xi1R   = xi1[::-1]
eta1R = eta1[::-1]

#   combine the rereversed arrays to the end of xi2, and eta2
xi2R = np.insert(xi1R, 0, xi2)
eta2R = np.insert(eta1R, 0, eta2)

start_time = time.time()
area = PolygonArea(np.transpose([[xi2R], [eta2R]]))
print("--- %s seconds ---" % (time.time() - start_time))

plt.figure()
#for i,j in enumerate(xi2R):
#    plt.plot(xi2R[i], eta2R[i], 'ok')
    #plt.show()
plt.plot(xi2R, eta2R, '-ok')
plt.legend(loc=2)
plt.grid(True)
plt.title('Polygon shoelace formula area is ' + str(area))
plt.show()


def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
start_time = time.time()
area1 = PolyArea(xi2R, eta2R)
print("--- %s seconds ---" % (time.time() - start_time))

#===============================================================================
#   Attempt this problem with quadralertal area

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
    
    #plotX = [ x[0], x[1], x[2], x[3], x[0]]
    #plotY = [ y[0], y[1], y[2], y[3], y[0]]
    #plt.figure()
    #plt.plot( plotX, plotY, 'o-k',label=r'$\xi$1$\eta$1')

    
    if isQuad == False:
        #   attempt to rearange the first two points
        x[1], x[0] = x[0], x[1]
        y[1], y[0] = y[0], y[1]
        AB = [ x[1]-x[0], y[1]-y[0] ]
        BC = [ x[2]-x[1], y[2]-y[1] ]
        CD = [ x[3]-x[2], y[3]-y[2] ]
        DA = [ x[0]-x[3], y[0]-y[3] ]
        
        isQuad = isSimpleQuad(AB, BC, CD, DA)
        
        #plotX = [ x[0], x[1], x[2], x[3], x[0]]
        #plotY = [ y[0], y[1], y[2], y[3], y[0]]
        #plt.plot( plotX, plotY, '-r',label=r'$\xi$1$\eta$1')
        
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
            #plt.plot( plotX, plotY, '-b',label=r'$\xi$1$\eta$1')
        
    #plt.grid(True)
    #plt.show()
    
    plotX = [ x[0], x[1], x[2], x[3], x[0]]
    plotY = [ y[0], y[1], y[2], y[3], y[0]]
    plt.plot( plotX, plotY, '-b')
    
    area = PolyArea( x, y)

    return area

plt.figure()
plt.plot(xi1, eta1, 'ok')
plt.plot(xi2, eta2, 'ok')
area = []
start_time = time.time()

for i in range(1, len(xi1)):
    tempX = [xi1[i-1], xi1[i], xi2[i], xi2[i-1]]
    tempY = [eta1[i-1], eta1[i], eta2[i], eta2[i-1]]
    area.append(makeQuad( tempX, tempY))
plt.title('The quadralteral area as the summation of shoelaces ' + str(sum(area)))
print("--- %s seconds ---" % (time.time() - start_time))
  
plt.grid(True)
plt.show()


#   Code for Frechet Distance from https://gist.github.com/MaxBareiss/ba2f9441d9455b56fbc9
# Euclidean distance.
def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))

def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

""" Computes the discrete frechet distance between two polygonal lines
Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
P and Q are arrays of 2-element arrays (points)
"""
def frechetDist(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)
start_time = time.time()

FD = frechetDist([xi1, eta1], [xi2, eta2])
print 'The Frechet distance is ', FD
print("--- %s seconds ---" % (time.time() - start_time))
