# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
numpy.where()函数是三元表达式x if condition else y的矢量化版本，相当于是一个if的三元表达式
"""
import numpy as np
from numpy.random import randn

x = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
y = np.array([2.1, 2.2, 2.3, 2., 2.5])
condition = np.array([True, False, True, True, False])
# result=[(x if condition else y) for x,y,condition in zip(xarr, yarr, condition]
result = np.where(condition, x, y)  # x if condition else y
print(result)  # [ 1.1  2.2  1.3  1.4  2.5]

arr = randn(4, 4)
print(arr)
# [[-0.18681492 -1.10580148  1.4275585   0.46533781]
#  [ 0.06259091 -0.39561885  2.45960192 -0.52976775]
#  [ 0.99848384 -1.15861484  0.86806706  0.95393949]
#  [-1.9073702   0.57153059  0.60846256  0.79204997]]
print(np.where(arr > 0, 2, -2))
# [[-2 -2  2  2]
#  [ 2 -2  2 -2]
#  [ 2 -2  2  2]
#  [-2  2  2  2]]
print(np.where(arr > 0, 0, arr))
# [[-0.18681492 -1.10580148  0.          0.        ]
#  [ 0.         -0.39561885  0.         -0.52976775]
#  [ 0.         -1.15861484  0.          0.        ]
#  [-1.9073702   0.          0.          0.        ]]

