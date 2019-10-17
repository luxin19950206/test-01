# -*- coding: utf-8 -*-
from pandas import DataFrame
"""
DataFrame.rename(index=None, columns=None, **kwargs)
Alter axes input function or functions. Function / dict values must be unique (1-to-1). Labels not contained in a
dict / Series will be left as-is. Extra labels listed don’t throw an error. Alternatively, change Series.name with
a scalar value (Series only).

index, columns : scalar, list-like, dict-like or function, optional
    Scalar or list-like will alter the Series.name attribute, and raise on DataFrame or Panel. dict-like or functions
    are transformations to apply to that axis’ values

copy : boolean, default True
    Also copy underlying data

inplace : boolean, default False
    Whether to return a new DataFrame. If True then value of copy is ignored.
"""

# example
sf = {'a': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'b': [2000, 2001, 2002, 2001, 2002],
      'c': [1.5, 1.7, 1.6, 2.4, 2.9]}
df = DataFrame(sf)
df.rename(columns={'a': '叉叉', 'b': '涨幅'}, inplace=True)
