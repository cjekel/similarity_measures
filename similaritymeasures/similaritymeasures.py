from __future__ import division
import numpy as np
from scipy.spatial import distance
# MIT License
#
# Copyright (c) 2018,2019 Charles Jekel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def poly_area(x, y):
    r"""
    A function that computes the polygonal area via the shoelace formula.

    This function allows you to take the area of any polygon that is not self
    intersecting. This is also known as Gauss's area formula. See
    https://en.wikipedia.org/wiki/Shoelace_formula

    Parameters
    ----------
    x : ndarray (1-D)
        the x locations of a polygon
    y : ndarray (1-D)
        the y locations of the polygon

    Returns
    -------
    area : float
        the calculated polygonal area

    Notes
    -----
    The x and y locations need to be ordered such that the first vertex
    of the polynomial correspounds to x[0] and y[0], the second vertex
    x[1] and y[1] and so forth


    Thanks to Mahdi for this one line code
    https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    """
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))


def is_simple_quad(ab, bc, cd, da):
    r"""
    Returns True if a quadrilateral is simple

    This function performs cross products at the vertices of a quadrilateral.
    It is possible to use the results to decide whether a quadrilateral is
    simple or complex. This function returns True if the quadrilateral is
    simple, and False if the quadrilateral is complex. A complex quadrilateral
    is a self-intersecting quadrilateral.

    Parameters
    ----------
    ab : array_like
        [x, y] location of the first vertex
    bc : array_like
        [x, y] location of the second vertex
    cd : array_like
        [x, y] location of the third vertex
    da : array_like
        [x, y] location of the fourth vertex

    Returns
    -------
    simple : bool
        True if quadrilateral is simple, False if complex
    """
    #   Compute all four cross products
    temp0 = np.cross(ab, bc)
    temp1 = np.cross(bc, cd)
    temp2 = np.cross(cd, da)
    temp3 = np.cross(da, ab)
    cross = np.array([temp0, temp1, temp2, temp3])
    #   See that majority of cross products is non-positive or non-negative
    #   They don't necessarily need to lie in the same 'Z' direction
    if sum(cross > 0) < sum(cross < 0):
        crossTF = cross <= 0
    else:
        crossTF = cross >= 0
    return sum(crossTF) > 2


def makeQuad(x, y):
    r"""
    Calculate the area from the x and y locations of a quadrilateral

    This function first constructs a simple quadrilateral from the x and y
    locations of the vertices of the quadrilateral. The function then
    calculates the shoelace area of the simple quadrilateral.

    Parameters
    ----------
    x : array_like
        the x locations of a quadrilateral
    y : array_like
        the y locations of a quadrilateral

    Returns
    -------
    area : float
        Area of quadrilateral via shoelace formula

    Notes
    -----
    This function rearranges the vertices of a quadrilateral until the
    quadrilateral is "Simple" (meaning non-complex). Once a simple
    quadrilateral is found, the area of the quadrilateral is calculated
    using the shoelace formula.
    """

    # check to see if the provide point order is valid
    # I need to get the values of the cross products of ABxBC, BCxCD, CDxDA,
    # DAxAB, thus I need to create the following arrays AB, BC, CD, DA

    AB = [x[1]-x[0], y[1]-y[0]]
    BC = [x[2]-x[1], y[2]-y[1]]
    CD = [x[3]-x[2], y[3]-y[2]]
    DA = [x[0]-x[3], y[0]-y[3]]

    isQuad = is_simple_quad(AB, BC, CD, DA)

    if isQuad is False:
        # attempt to rearrange the first two points
        x[1], x[0] = x[0], x[1]
        y[1], y[0] = y[0], y[1]
        AB = [x[1]-x[0], y[1]-y[0]]
        BC = [x[2]-x[1], y[2]-y[1]]
        CD = [x[3]-x[2], y[3]-y[2]]
        DA = [x[0]-x[3], y[0]-y[3]]

        isQuad = is_simple_quad(AB, BC, CD, DA)

        if isQuad is False:
            # place the second and first points back where they were, and
            # swap the second and third points
            x[2], x[0], x[1] = x[0], x[1], x[2]
            y[2], y[0], y[1] = y[0], y[1], y[2]
            AB = [x[1]-x[0], y[1]-y[0]]
            BC = [x[2]-x[1], y[2]-y[1]]
            CD = [x[3]-x[2], y[3]-y[2]]
            DA = [x[0]-x[3], y[0]-y[3]]

            isQuad = is_simple_quad(AB, BC, CD, DA)

    # calculate the area via shoelace formula
    area = poly_area(x, y)
    return area


def get_arc_length(dataset):
    r"""
    Obtain arc length distances between every point in 2-D space

    Obtains the total arc length of a curve in 2-D space (a curve of x and y)
    as well as the arc lengths between each two consecutive data points of the
    curve.

    Parameters
    ----------
    dataset : ndarray (2-D)
        The dataset of the curve in 2-D space.

    Returns
    -------
    arcLength : float
        The sum of all consecutive arc lengths
    arcLengths : array_like
        A list of the arc lengths between data points

    Notes
    -----
    Your x locations of data points should be dataset[:, 0], and the y
    locations of the data points should be dataset[:, 1]
    """
    #   split the dataset into two discrete datasets, each of length m-1
    m = len(dataset)
    a = dataset[0:m-1, :]
    b = dataset[1:m, :]
    #   use scipy.spatial to compute the euclidean distance
    dataDistance = distance.cdist(a, b, 'euclidean')
    #   this returns a matrix of the euclidean distance between all points
    #   the arc length is simply the sum of the diagonal of this matrix
    arcLengths = np.diagonal(dataDistance)
    arcLength = sum(arcLengths)
    return arcLength, arcLengths


def area_between_two_curves(exp_data, num_data):
    r"""
    Calculates the area between two curves.

    This calculates the area according to the algorithm in [1]_. Each curve is
    constructed from discretized data points in 2-D space, e.g. each curve
    consists of x and y data points.

    Parameters
    ----------
    exp_data : ndarray (2-D)
        Curve from your experimental data.
    num_data : ndarray (2-D)
        Curve from your numerical data.

    Returns
    -------
    area : float
        The area between exp_data and num_data curves.

    References
    ----------
    .. [1] Jekel, C. F., Venter, G., Venter, M. P., Stander, N., & Haftka, R.
        T. (2018). Similarity measures for identifying material parameters from
        hysteresis loops using inverse analysis. International Journal of
        Material Forming. https://doi.org/10.1007/s12289-018-1421-8

    Notes
    -----
    Your x locations of data points should be exp_data[:, 0], and the y
    locations of the data points should be exp_data[:, 1]. Same for num_data.
    """
    # Calculate the area between two curves using quadrilaterals
    # Consider the test data to be data from an experimental test as exp_data
    # Consider the computer simulation (results from numerical model) to be
    # num_data
    #
    # Example on formatting the test and history data:
    # Curve1 = [xi1, eta1]
    # Curve2 = [xi2, eta2]
    # exp_data = np.zeros([len(xi1), 2])
    # num_data = np.zeros([len(xi2), 2])
    # exp_data[:,0] = xi1
    # exp_data[:,1] = eta1
    # num_data[:, 0] = xi2
    # num_data[:, 1] = eta2
    #
    # then you can calculate the area as
    # area = area_between_two_curves(exp_data, num_data)

    n_exp = len(exp_data)
    n_num = len(num_data)

    # the length of exp_data must be larger than the length of num_data
    if n_exp < n_num:
        temp = num_data.copy()
        num_data = exp_data.copy()
        exp_data = temp.copy()
        n_exp = len(exp_data)
        n_num = len(num_data)

    # get the arc length data of the curves
    # arcexp_data, _ = get_arc_length(exp_data)
    _, arcsnum_data = get_arc_length(num_data)

    # let's find the largest gap between point the num_data, and then
    # linearally interpolate between these points such that the num_data
    # becomes the same length as the exp_data
    for i in range(0, n_exp-n_num):
        a = num_data[0:n_num-1, 0]
        b = num_data[1:n_num, 0]
        nIndex = np.argmax(arcsnum_data)
        newX = (b[nIndex] + a[nIndex])/2.0
        #   the interpolation model messes up if x2 < x1 so we do a quick check
        if a[nIndex] < b[nIndex]:
            newY = np.interp(newX, [a[nIndex], b[nIndex]],
                             [num_data[nIndex, 1], num_data[nIndex+1, 1]])
        else:
            newY = np.interp(newX, [b[nIndex], a[nIndex]],
                             [num_data[nIndex+1, 1], num_data[nIndex, 1]])
        num_data = np.insert(num_data, nIndex+1, newX, axis=0)
        num_data[nIndex+1, 1] = newY

        _, arcsnum_data = get_arc_length(num_data)
        n_num = len(num_data)

    # Calculate the quadrilateral area, by looping through all of the quads
    area = []
    for i in range(1, n_exp):
        tempX = [exp_data[i-1, 0], exp_data[i, 0], num_data[i, 0],
                 num_data[i-1, 0]]
        tempY = [exp_data[i-1, 1], exp_data[i, 1], num_data[i, 1],
                 num_data[i-1, 1]]
        area.append(makeQuad(tempX, tempY))
    return np.sum(area)


def get_length(x, y, norm_seg_length=True):
    r"""
    Compute arc lengths of an x y curve.

    Computes the arc length of a xy curve, the cumulative arc length of an xy,
    and the total xy arc length of a xy curve. The euclidean distance is used
    to determine the arc length.

    Parameters
    ----------
    x : array_like
        the x locations of a curve
    y : array_like
        the y locations of a curve
    norm_seg_length : boolean
        Whether to divide the segment length of each curve by the maximum.

    Returns
    -------
    le : ndarray (1-D)
        the euclidean distance between every two points
    le_total : float
        the total arc length distance of a curve
    le_cum : ndarray (1-D)
        the cumulative sum of euclidean distances between every two points

    Examples
    --------
    >>> le, le_total, le_cum = get_length(x, y)

    """
    n = len(x)

    if norm_seg_length:
        xmax = np.max(np.abs(x))
        ymax = np.max(np.abs(y))

        # if your max x or y value is zero... you'll get np.inf
        # as your curve length based measure
        if xmax == 0:
            xmax = 1e-15
        if ymax == 0:
            ymax = 1e-15
    else:
        ymax = 1.0
        xmax = 1.0

    le = np.zeros(n)
    le[0] = 0.0
    l_sum = np.zeros(n)
    l_sum[0] = 0.0
    for i in range(0, n-1):
        le[i+1] = np.sqrt((((x[i+1]-x[i])/xmax)**2)+(((y[i+1]-y[i])/ymax)**2))
        l_sum[i+1] = l_sum[i]+le[i+1]
    return le, np.sum(le), l_sum


def curve_length_measure(exp_data, num_data):
    r"""
    Compute the curve length based distance between two curves.

    This computes the curve length similarity measure according to [1]_. This
    implementation follows the OF2 form, which is a self normalizing form
    based on the average value.

    Parameters
    ----------
    exp_data : ndarray (2-D)
        Curve from your experimental data.
    num_data : ndarray (2-D)
        Curve from your numerical data.

    Returns
    -------
    r : float
        curve length based similarity distance

    Notes
    -----
    This uses the OF2 method from [1]_.

    References
    ----------
    .. [1] A Andrade-Campos, R De-Carvalho, and R A F Valente. Novel criteria
        for determination of material model parameters. International Journal
        of Mechanical Sciences, 54(1):294-305, 2012. ISSN 0020-7403. DOI
        https://doi.org/10.1016/j.ijmecsci.2011.11.010 URL:
        http://www.sciencedirect.com/science/article/pii/S0020740311002451

    Examples
    --------
    >>> # Generate random experimental data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> exp_data = np.zeros((100, 2))
    >>> exp_data[:, 0] = x
    >>> exp_data[:, 1] = y
    >>> # Generate random numerical data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> num_data = np.zeros((100, 2))
    >>> num_data[:, 0] = x
    >>> num_data[:, 1] = y
    >>> r = curve_length_measure(exp_data, num_data)

    """
    x_e = exp_data[:, 0]
    y_e = exp_data[:, 1]
    x_c = num_data[:, 0]
    y_c = num_data[:, 1]

    _, le_nj, le_sum = get_length(x_e, y_e)
    _, lc_nj, lc_sum = get_length(x_c, y_c)

    xmean = np.mean(x_e)
    ymean = np.mean(y_e)

    n = len(x_e)

    r_sq = np.zeros(n)
    for i in range(0, n):
        lieq = le_sum[i]*(lc_nj/le_nj)
        xtemp = np.interp(lieq, lc_sum, x_c)
        ytemp = np.interp(lieq, lc_sum, y_c)

        r_sq[i] = np.log(1.0 + (np.abs((xtemp-x_e[i])/xmean)))**2 + \
            np.log(1.0 + (np.abs((ytemp-y_e[i])/ymean)))**2
    return np.sqrt(np.sum(r_sq))


def frechet_dist(exp_data, num_data, p=2):
    r"""
    Compute the discrete Frechet distance

    Compute the Discrete Frechet Distance between two N-D curves according to
    [1]_. The Frechet distance has been defined as the walking dog problem.
    From Wikipedia: "In mathematics, the Frechet distance is a measure of
    similarity between curves that takes into account the location and
    ordering of the points along the curves. It is named after Maurice Frechet.
    https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance

    Parameters
    ----------
    exp_data : array_like
        Curve from your experimental data. exp_data is of (M, N) shape, where
        M is the number of data points, and N is the number of dimmensions
    num_data : array_like
        Curve from your numerical data. num_data is of (P, N) shape, where P
        is the number of data points, and N is the number of dimmensions
    p : float, 1 <= p <= infinity
        Which Minkowski p-norm to use. Default is p=2 (Eculidean).
        The manhattan distance is p=1.

    Returns
    -------
    df : float
        discrete Frechet distance

    References
    ----------
    .. [1] Thomas Eiter and Heikki Mannila. Computing discrete Frechet
        distance. Technical report, 1994.
        http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.90.937&rep=rep1&type=pdf

    Notes
    -----
    Your x locations of data points should be exp_data[:, 0], and the y
    locations of the data points should be exp_data[:, 1]. Same for num_data.

    Thanks to Arbel Amir for the issue, and Sen ZHANG for the iterative code
    https://github.com/cjekel/similarity_measures/issues/6

    Examples
    --------
    >>> # Generate random experimental data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> exp_data = np.zeros((100, 2))
    >>> exp_data[:, 0] = x
    >>> exp_data[:, 1] = y
    >>> # Generate random numerical data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> num_data = np.zeros((100, 2))
    >>> num_data[:, 0] = x
    >>> num_data[:, 1] = y
    >>> df = frechet_dist(exp_data, num_data)

    """
    n = len(exp_data)
    m = len(num_data)
    c = distance.cdist(exp_data, num_data, metric='minkowski', p=p)
    ca = np.ones((n, m))
    ca = np.multiply(ca, -1)
    ca[0, 0] = c[0, 0]
    for i in range(1, n):
        ca[i, 0] = max(ca[i-1, 0], c[i, 0])
    for j in range(1, m):
        ca[0, j] = max(ca[0, j-1], c[0, j])
    for i in range(1, n):
        for j in range(1, m):
            ca[i, j] = max(min(ca[i-1, j], ca[i, j-1], ca[i-1, j-1]),
                           c[i, j])
    return ca[n-1, m-1]


def normalizeTwoCurves(x, y, w, z):
    """
    Normalize two curves for PCM method.

    This normalizes the two curves for PCM method following [1]_.

    Parameters
    ----------
    x : array_like (1-D)
        x locations for first curve
    y : array_like (1-D)
        y locations for first curve
    w : array_like (1-D)
        x locations for second curve curve
    z : array_like (1-D)
        y locations for second curve

    Returns
    -------
    xi : array_like
        normalized x locations for first curve
    eta : array_like
        normalized y locations for first curve
    xiP : array_like
        normalized x locations for second curve
    etaP : array_like
        normalized y locations for second curve

    References
    ----------
    .. [1] Katharina Witowski and Nielen Stander. "Parameter Identification of
        Hysteretic Models Using Partial Curve Mapping", 12th AIAA Aviation
        Technology, Integration, and Operations (ATIO) Conference and 14th
        AIAA/ISSMO Multidisciplinary Analysis and Optimization Conference,
        Aviation Technology, Integration, and Operations (ATIO) Conferences.
        doi: doi:10.2514/6.2012-5580.

    Examples
    --------
    >>> xi, eta, xiP, etaP = normalizeTwoCurves(x,y,w,z)

    """
    minX = np.min(x)
    maxX = np.max(x)
    minY = np.min(y)
    maxY = np.max(y)

    xi = (x - minX) / (maxX - minX)
    eta = (y - minY) / (maxY - minY)
    xiP = (w - minX) / (maxX - minX)
    etaP = (z - minY) / (maxY - minY)
    return xi, eta, xiP, etaP


def pcm(exp_data, num_data, norm_seg_length=False):
    """
    Compute the Partial Curve Mapping area.

    Computes the Partial Cuve Mapping (PCM) similarity measure as proposed by
    [1]_.

    Parameters
    ----------
    exp_data : ndarray (2-D)
        Curve from your experimental data.
    num_data : ndarray (2-D)
        Curve from your numerical data.
    norm_seg_length : boolean
        Whether to divide the segment length of each curve by the maximum. The
        default value is false, which more closely follows the algorithm
        proposed in [1]_. Versions prior to 0.6.0 used `norm_seg_length=True`.

    Returns
    -------
    p : float
        pcm area measure

    Notes
    -----
    Your x locations of data points should be exp_data[:, 0], and the y
    locations of the data points should be exp_data[:, 1]. Same for num_data.

    PCM distance was changed in version 0.6.0. To get the same results from
    previous versions, set `norm_seg_length=True`.

    References
    ----------
    .. [1] Katharina Witowski and Nielen Stander. "Parameter Identification of
        Hysteretic Models Using Partial Curve Mapping", 12th AIAA Aviation
        Technology, Integration, and Operations (ATIO) Conference and 14th
        AIAA/ISSMO Multidisciplinary Analysis and Optimization Conference,
        Aviation Technology, Integration, and Operations (ATIO) Conferences.
        doi: doi:10.2514/6.2012-5580.

    Examples
    --------
    >>> # Generate random experimental data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> exp_data = np.zeros((100, 2))
    >>> exp_data[:, 0] = x
    >>> exp_data[:, 1] = y
    >>> # Generate random numerical data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> num_data = np.zeros((100, 2))
    >>> num_data[:, 0] = x
    >>> num_data[:, 1] = y
    >>> p = pcm(exp_data, num_data)
    """
    # normalize the curves to the experimental data
    xi1, eta1, xi2, eta2 = normalizeTwoCurves(exp_data[:, 0], exp_data[:, 1],
                                              num_data[:, 0], num_data[:, 1])
    # compute the arc lengths of each curve
    le, le_nj, le_sum = get_length(xi1, eta1, norm_seg_length)
    lc, lc_nj, lc_sum = get_length(xi2, eta2, norm_seg_length)
    # scale each segment to the total polygon length
    le = le / le_nj
    le_sum = le_sum / le_nj
    lc = lc / lc_nj
    lc_sum = lc_sum / lc_nj
    # right now exp_data is curve a, and num_data is curve b
    # make sure a is shorter than a', if not swap the defintion
    if lc_nj > le_nj:
        # compute the arc lengths of each curve
        le, le_nj, le_sum = get_length(xi2, eta2, norm_seg_length)
        lc, lc_nj, lc_sum = get_length(xi1, eta1, norm_seg_length)
        # scale each segment to the total polygon length
        le = le / le_nj
        le_sum = le_sum / le_nj
        lc = lc / lc_nj
        lc_sum = lc_sum / lc_nj
        # swap xi1, eta1 with xi2, eta2
        xi1OLD = xi1.copy()
        eta1OLD = eta1.copy()
        xi1 = xi2.copy()
        eta1 = eta2.copy()
        xi2 = xi1OLD.copy()
        eta2 = eta1OLD.copy()

    n_sum = len(le_sum)

    min_offset = 0.0
    max_offset = le_nj - lc_nj

    # make sure the curves aren't the same length
    # if they are the same length, don't loop 200 times
    if min_offset == max_offset:
        offsets = [min_offset]
        pcm_dists = np.zeros(1)
    else:
        offsets = np.linspace(min_offset, max_offset, 200)
        pcm_dists = np.zeros(200)

    for i, offset in enumerate(offsets):
        # create linear interpolation model for num_data based on arc length
        # evaluate linear interpolation model based on xi and eta of exp data
        xitemp = np.interp(le_sum+offset, lc_sum, xi2)
        etatemp = np.interp(le_sum+offset, lc_sum, eta2)

        d = np.sqrt((eta1-etatemp)**2 + (xi1-xitemp)**2)
        d1 = d[:-1]

        d2 = d[1:n_sum]

        v = 0.5*(d1+d2)*le_sum[1:n_sum]
        pcm_dists[i] = np.sum(v)
    return np.min(pcm_dists)


def dtw(exp_data, num_data, metric='euclidean', **kwargs):
    r"""
    Compute the Dynamic Time Warping distance.

    This computes a generic Dynamic Time Warping (DTW) distance and follows
    the algorithm from [1]_. This can use all distance metrics that are
    available in scipy.spatial.distance.cdist.

    Parameters
    ----------
    exp_data : array_like
        Curve from your experimental data. exp_data is of (M, N) shape, where
        M is the number of data points, and N is the number of dimmensions
    num_data : array_like
        Curve from your numerical data. num_data is of (P, N) shape, where P
        is the number of data points, and N is the number of dimmensions
    metric : str or callable, optional
        The distance metric to use. Default='euclidean'. Refer to the
        documentation for scipy.spatial.distance.cdist. Some examples:
        'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'kulsinski',
        'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao',
        'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean',
        'wminkowski', 'yule'.
    **kwargs : dict, optional
        Extra arguments to `metric`: refer to each metric documentation in
        scipy.spatial.distance.
        Some examples:

        p : scalar
            The p-norm to apply for Minkowski, weighted and unweighted.
            Default: 2.

        w : ndarray
            The weight vector for metrics that support weights (e.g.,
            Minkowski).

        V : ndarray
            The variance vector for standardized Euclidean.
            Default: var(vstack([XA, XB]), axis=0, ddof=1)

        VI : ndarray
            The inverse of the covariance matrix for Mahalanobis.
            Default: inv(cov(vstack([XA, XB].T))).T

        out : ndarray
            The output array
            If not None, the distance matrix Y is stored in this array.

    Returns
    -------
    r : float
        DTW distance.
    d : ndarray (2-D)
        Cumulative distance matrix

    Notes
    -----
    The DTW distance is d[-1, -1].

    This has O(M, P) computational cost.

    The latest scipy.spatial.distance.cdist information can be found at
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html

    Your x locations of data points should be exp_data[:, 0], and the y
    locations of the data points should be exp_data[:, 1]. Same for num_data.

    This uses the euclidean distance for now. In the future it should be
    possible to support other metrics.

    DTW is a non-metric distance, which means DTW doesn't hold the triangle
    inequality.
    https://en.wikipedia.org/wiki/Triangle_inequality

    References
    ----------
    .. [1] Senin, P., 2008. Dynamic time warping algorithm review. Information
        and Computer Science Department University of Hawaii at Manoa Honolulu,
        USA, 855, pp.1-23.
        http://seninp.github.io/assets/pubs/senin_dtw_litreview_2008.pdf

    Examples
    --------
    >>> # Generate random experimental data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> exp_data = np.zeros((100, 2))
    >>> exp_data[:, 0] = x
    >>> exp_data[:, 1] = y
    >>> # Generate random numerical data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> num_data = np.zeros((100, 2))
    >>> num_data[:, 0] = x
    >>> num_data[:, 1] = y
    >>> r, d = dtw(exp_data, num_data)

    The euclidean distance is used by default. You can use metric and **kwargs
    to specify different types of distance metrics. The following example uses
    the city block or Manhattan distance between points.

    >>> r, d = dtw(exp_data, num_data, metric='cityblock')

    """
    c = distance.cdist(exp_data, num_data, metric=metric, **kwargs)

    d = np.zeros(c.shape)
    d[0, 0] = c[0, 0]
    n, m = c.shape
    for i in range(1, n):
        d[i, 0] = d[i-1, 0] + c[i, 0]
    for j in range(1, m):
        d[0, j] = d[0, j-1] + c[0, j]
    for i in range(1, n):
        for j in range(1, m):
            d[i, j] = c[i, j] + min((d[i-1, j], d[i, j-1], d[i-1, j-1]))
    return d[-1, -1], d


def dtw_path(d):
    r"""
    Calculates the optimal DTW path from a given DTW cumulative distance
    matrix.

    This function returns the optimal DTW path using the back propagation
    algorithm that is defined in [1]_. This path details the index from each
    curve that is being compared.

    Parameters
    ----------
    d : ndarray (2-D)
        Cumulative distance matrix.

    Returns
    -------
    path : ndarray (2-D)
        The optimal DTW path.

    Notes
    -----
    Note that path[:, 0] represents the indices from exp_data, while
    path[:, 1] represents the indices from the num_data.

    References
    ----------
    .. [1] Senin, P., 2008. Dynamic time warping algorithm review. Information
        and Computer Science Department University of Hawaii at Manoa Honolulu,
        USA, 855, pp.1-23.
        http://seninp.github.io/assets/pubs/senin_dtw_litreview_2008.pdf

    Examples
    --------
    First calculate the DTW cumulative distance matrix.

    >>> # Generate random experimental data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> exp_data = np.zeros((100, 2))
    >>> exp_data[:, 0] = x
    >>> exp_data[:, 1] = y
    >>> # Generate random numerical data
    >>> x = np.random.random(100)
    >>> y = np.random.random(100)
    >>> num_data = np.zeros((100, 2))
    >>> num_data[:, 0] = x
    >>> num_data[:, 1] = y
    >>> r, d = dtw(exp_data, num_data)

    Now you can calculate the optimal DTW path

    >>> path = dtw_path(d)

    You can visualize the path on the cumulative distance matrix using the
    following code.

    >>> import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> plt.imshow(d.T, origin='lower')
    >>> plt.plot(path[:, 0], path[:, 1], '-k')
    >>> plt.colorbar()
    >>> plt.show()

    """
    path = []
    i, j = d.shape
    i = i - 1
    j = j - 1
    # back propagation starts from the last point,
    # and ends at d[0, 0]
    path.append((i, j))
    while i > 0 or j > 0:
        if i == 0:
            j = j - 1
        elif j == 0:
            i = i - 1
        else:
            temp_step = min([d[i-1, j], d[i, j-1], d[i-1, j-1]])
            if d[i-1, j] == temp_step:
                i = i - 1
            elif d[i, j-1] == temp_step:
                j = j - 1
            else:
                i = i - 1
                j = j - 1
        path.append((i, j))
    path = np.array(path)
    # reverse the order of path, such that it starts with [0, 0]
    return path[::-1]


def mae(exp_data, num_data):
    """
    Compute the Mean Absolute Error (MAE).

    This computes the mean of absolute values of distances between two curves.
    Each curve must have the same number of data points and the same dimension.

    Parameters
    ----------
    exp_data : array_like
        Curve from your experimental data. exp_data is of (M, N) shape, where
        M is the number of data points, and N is the number of dimensions
    num_data : array_like
        Curve from your numerical data. num_data is of (M, N) shape, where M
        is the number of data points, and N is the number of dimensions

    Returns
    -------
    r : float
        MAE.
    """
    c = np.abs(exp_data - num_data)
    return np.mean(c)


def mse(exp_data, num_data):
    """
    Compute the Mean Squared Error (MAE).

    This computes the mean of sqaured distances between two curves.
    Each curve must have the same number of data points and the same dimension.

    Parameters
    ----------
    exp_data : array_like
        Curve from your experimental data. exp_data is of (M, N) shape, where
        M is the number of data points, and N is the number of dimensions
    num_data : array_like
        Curve from your numerical data. num_data is of (M, N) shape, where M
        is the number of data points, and N is the number of dimensions

    Returns
    -------
    r : float
        MSE.
    """
    c = np.square(exp_data - num_data)
    return np.mean(c)
