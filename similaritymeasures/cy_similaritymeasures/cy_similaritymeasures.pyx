import numpy as np
from scipy.spatial import distance

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