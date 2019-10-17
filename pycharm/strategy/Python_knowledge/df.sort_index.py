"""
DataFrame.sort_index(axis=0, by=None, ascending=True, inplace=False, kind='quicksort')
    Sort DataFrame either by labels (along either axis) or by the values in a column

by : object
    Column name(s) in frame. Accepts a column name or a list or tuple for a nested sort.
"""

from pandas import DataFrame, Series
import warnings

warnings.filterwarnings("ignore")

sf = {'a': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'b': [2000, 2001, 2002, 2001, 2002],
      'c': [1.5, 1.7, 1.6, 2.4, 2.9]}
df = DataFrame(sf)
print(df.sort_index(by='b', ascending=False))
print(df.sort_index(by='c'))
print(df.sort_index())