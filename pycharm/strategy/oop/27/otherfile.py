# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
p700
"""

import manynames

X = 66
print(X)  # 66
print(manynames.X)  # 11
manynames.f()  # 11
manynames.g()  # 22
print(manynames.C.X)  # 33
I=manynames.C()
print(I.X)  # 33
I.m()
print(I.X)  # 55
