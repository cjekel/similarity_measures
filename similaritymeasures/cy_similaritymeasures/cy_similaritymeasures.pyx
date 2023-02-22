import numpy as np
from scipy.spatial import distance

cdef double c_max(double a, double b):
    if a > b:
        return a
    return b

cdef double c_min(double a, double b):
    if a < b:
        return a
    return b

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
    cdef int i, j
    cdef int n = len(exp_data)
    cdef int m = len(num_data)
    c = distance.cdist(exp_data, num_data, metric='minkowski', p=p)
    #ca = np.ones((n, m))
    #ca = np.multiply(ca, -1)
    #ca[0, 0] = c[0, 0]
    #for i in range(1, n):
    #    ca[i, 0] = max(ca[i-1, 0], c[i, 0])
    #for j in range(1, m):
    #    ca[0, j] = max(ca[0, j-1], c[0, j])
    for i in range(1, n):
        for j in range(1, m):
            c[i, j] = c_max(
                c_min(c_min(c[i-1, j], c[i, j-1]) , c[i-1, j-1]),
                c[i, j])
    return c[n-1, m-1]

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
    cdef int i, j
    cdef int n = len(exp_data)
    cdef int m = len(num_data)
    c = distance.cdist(exp_data, num_data, metric=metric, **kwargs)

    d = np.zeros(c.shape)
    d[0, 0] = c[0, 0]
    #n, m = c.shape
    for i in range(1, n):
        d[i, 0] = d[i-1, 0] + c[i, 0]
    for j in range(1, m):
        d[0, j] = d[0, j-1] + c[0, j]
    for i in range(1, n):
        for j in range(1, m):
            d[i, j] = c[i, j] + c_min(c_min(d[i-1, j], d[i, j-1]), d[i-1, j-1])
    return d[-1, -1], d