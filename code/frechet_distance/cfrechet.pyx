import numpy as np
# Thanks to MaxBareiss
# https://gist.github.com/MaxBareiss/ba2f9441d9455b56fbc9
# Euclidean distance.
cdef euc_dist(pt1, pt2):
    return ((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))**0.5

cdef _c(ca, i,j,P, Q):
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


def frechetDist(P, Q):
    # Computes the discrete frechet distance between two polygonal lines
    # Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
    # P and Q are arrays of 2-element arrays (points)
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca, -1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)
