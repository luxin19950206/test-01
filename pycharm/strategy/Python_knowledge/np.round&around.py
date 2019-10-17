# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
np.round(a, decimals=0, out=None)
    Evenly round to the given number of decimals.求约数、四舍五入
a : array_like
    Input data.
decimals : int, optional 约数的小数
    Number of decimal places to round to (default: 0). If decimals is negative, it specifies
    the number of positions to the left of the decimal point.

"""
import numpy as np

np.round(a, decimals=0, out=None)
# >>> np.around([0.37, 1.64])
# array([ 0.,  2.])
# >>> np.around([0.37, 1.64], decimals=1)
# array([ 0.4,  1.6])
# >>> np.around([.5, 1.5, 2.5, 3.5, 4.5]) # rounds to nearest even value
# array([ 0.,  2.,  2.,  4.,  4.])
# >>> np.around([1,2,3,11], decimals=1) # ndarray of ints is returned
# array([ 1,  2,  3, 11])
# >>> np.around([1,2,3,11], decimals=-1)
# array([ 0,  0,  0, 10])

