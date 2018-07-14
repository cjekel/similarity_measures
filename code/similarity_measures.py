import numpy as np
from scipy.spatial import distance


def poly_area(x, y):
    """
    A function that computes the polynomial area via the shoelace formula

    Input:
    x (1D array) - the x locations of a polynomial
    y (1D array) - the y locations of the polynomail

    Note:
    The x and y locations need to be ordered such that the first vertex
    of the polynomial correspounds to x[0] and y[0], the second vertex
    x[1] and y[1] and so forth

    Returns:
    (float) - Area of the polynomial via the shoelace formula
    """
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))


def is_simple_quad(ab, bc, cd, da):
    """
    A function that performs all of the cross products of a quadrilateral

    Input (the verticies of the quadrilateral):
    ab (list) - [x, y] location of the first vertex
    bc (list) - [x, y] location of the second vertex
    cd (list) - [x, y] location of the third vertex
    da (list) - [x, y] location of the fourth vertex

    Returns (boolean):
    True if quadrilateral is simple
    False if quadrilateral is complex
    """
    #   Compute all four cross products
    temp0 = np.cross(ab, bc)
    temp1 = np.cross(bc, cd)
    temp2 = np.cross(cd, da)
    temp3 = np.cross(da, ab)
    cross = np.array([temp0, temp1, temp2, temp3])
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


def makeQuad(x, y):
    """
    A function that constructs a simple quadrilateral from the x and y
    locations of the verticies of the quadrilateral. The function then
    calculates the shoelace area of the simple quadrilateral.

    Input:
    x (1D array) - the x locations of a quadrilateral
    y (1D array) - the y locations of a quadrilateral

    Note:
    This function rearranges the verticies of a quadrilateral until the
    quadrilateral is "Simple" (meaning non-complex). Once a simple
    quadrilateral is found, the area of the quadrilateral is calculated
    using the shoelace formula.

    Output:
    (float) - Area of quadrilateral via shoelace formula
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
    """
    Obtain the total arc length of a curve in 2D space (a curve of x and y) as
    well as the arc lengths between each two consecutive data points of the
    curve

    Input:
    dataset (2D array) - The dataset of the curve in 2D space. Your x
    locations of data points should be dataset[:, 0], and the y locations of
    the data points should be dataset[:, 1]

    Useage:
    arcLength, arcLengths = get_arc_length(dataset)

    Returns:
    arcLength (float) - the total arc length distance of your dataset (curve
    in 2D space)
    arcLengths (1D array) - a 1D array of the arc length between every two
    consecutive data points
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
    """
    Calculates the area between two curves according to the algorithm in [1].
    Each curve is constructed from discretizied data points in 2D space, e.g.
    each curve has x and y data point.

    Input:
    exp_data (2D array) - Curve from your experimental data. Your x
    locations of data points should be exp_data[:, 0], and the y locations of
    the data points should be exp_data[:, 1]

    num_data (2D array) - Curve from your numerical data. Your x
    locations of data points should be num_data[:, 0], and the y locations of
    the data points should be num_data[:, 1]

    Returns:
    area (float) - The area between your exp_data curve and the num_data curve

    References:
    [1] Jekel, C.F., Venter, G., Venter, M.P. et al. Int J Mater Form (2018).
    https://doi.org/10.1007/s12289-018-1421-8
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


def get_length(x, y):
    """
    computes the arc length of a xy curve, the cumulative arc length of an xy,
    and the total xy arc length of a xy curve. The euclidean distance is used
    to determine the arc length

    Input:
    x (1D array) - the x locations of a curve
    y (1D array) - the y locations of a curve

    Useage:
    le, le_total, le_cum = get_length(x, y)

    Returns:
    le (1D array) - the euclidean distance between every two points
    le_total (float) - the total arc length distance of a curve
    le_cum (1D array) - the cumulative sum of euclidean distances between
    every two points
    """
    n = len(x)
    xmax = np.max(np.abs(x))
    ymax = np.max(np.abs(y))
    
    # if your max x or y value is zero... you'll get np.inf
    # as your curve length based measure
    if xmax == 0:
        xmax = 1e-15
    if ymax == 0:
        ymax = 1e-15

    le = np.zeros(n)
    le[0] = 0.0
    l_sum = np.zeros(n)
    l_sum[0] = 0.0
    for i in range(0, n-1):
        le[i+1] = np.sqrt((((x[i+1]-x[i])/xmax)**2)+(((y[i+1]-y[i])/ymax)**2))
        l_sum[i+1] = l_sum[i]+le[i+1]
    return le, np.sum(le), l_sum


def curve_length_measure(exp_data, num_data):
    """
    Compute the curve length based similarity measure between two curves
    according to [2]. This implementation follows the OF2 form, which is a
    self normalizing form based on the average value.

    Input:
    exp_data (2D array) - Curve from your experimental data. Your x
    locations of data points should be exp_data[:, 0], and the y locations of
    the data points should be exp_data[:, 1]

    num_data (2D array) - Curve from your numerical data or computer
    simulation. Your x locations of data points should be num_data[:, 0], and
    the y locations of the data points should be num_data[:, 1]

    Returns:
    r (float) - curve length based similarity measure using OF2 from [2]

    References:
    [2] A Andrade-Campos, R De-Carvalho, and R A F Valente. Novel criteria for
    determination of material model parameters. International Journal of
    Mechanical Sciences, 54(1):294-305, 2012. ISSN 0020-7403. DOI
    https://doi.org/10.1016/j.ijmecsci.2011.11.010 URL:
    http://www.sciencedirect.com/science/article/pii/S0020740311002451
    """
    x_e = exp_data[:, 0]
    y_e = exp_data[:, 1]
    x_c = num_data[:, 0]
    y_c = num_data[:, 1]

    _, le_nj, le_sum = get_length(x_e, y_e)
    _, lc_nj, lc_sum = get_length(x_c, y_c)
    print(le_nj, le_nj)
    print(lc_nj, lc_nj)

    xmean = np.mean(x_e)
    ymean = np.mean(y_e)

    n = len(x_e)

    r_sq = np.zeros(n)
    for i in range(0, n):
        lieq = le_sum[i]*(lc_nj/le_nj)
        xtemp = np.interp(lieq, lc_sum, x_c)
        ytemp = np.interp(lieq, lc_sum, y_c)

        r_sq[i] = np.log(1.0 + (np.abs(xtemp-x_e[i])/xmean))**2 + \
            np.log(1.0 + (np.abs(ytemp-y_e[i])/ymean))**2
    return np.sqrt(np.sum(r_sq))

# https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
# https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
