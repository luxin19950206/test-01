"""
DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
Sort by the values along either axis
在dataframe中按照某一个轴进行排序，同时这个轴要是非index

by : string name or list of names which refer to the axis items
axis : index, columns to direct sorting
ascending : bool or list of bool
    Sort ascending vs. descending. Specify list for multiple sort orders. If this is a list of bools,
    must match the length of the by
    ascending中0代表false，1代表true
inplace : bool
    if True, perform operation in-place
kind : {quicksort, mergesort, heapsort}
    Choice of sorting algorithm. See also ndarray.np.sort for more information. mergesort is the only stable algorithm.
    For DataFrames, this option is only applied when sorting on a single column or label.
na_position : {‘first’, ‘last’}
    first puts NaNs at the beginning, last puts NaNs at the end
"""

from pandas import DataFrame, Series

sf = {'a': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'b': [2000, 2001, 2002, 2001, 2002],
      'c': [1.5, 1.7, 1.6, 2.4, 2.9]}
df = DataFrame(sf)

print(df.sort_values(by='c'))
"""
        a     b    c
0    Ohio  2000  1.5
2    Ohio  2002  1.6
1    Ohio  2001  1.7
3  Nevada  2001  2.4
4  Nevada  2002  2.9
"""
# ascending=True意味着升序（默认），从小到大排列
print(df.sort_values(by='c', ascending=False))
"""
        a     b    c
4  Nevada  2002  2.9
3  Nevada  2001  2.4
1    Ohio  2001  1.7
2    Ohio  2002  1.6
0    Ohio  2000  1.5
"""
print(df.sort_values(by='c', ascending=0))
# ascending中0代表false，1代表true
"""
        a     b    c
4  Nevada  2002  2.9
3  Nevada  2001  2.4
1    Ohio  2001  1.7
2    Ohio  2002  1.6
0    Ohio  2000  1.5
"""
# ascending=False意味着降序，从大到小排列
print(df.sort_index(axis=1, ascending=False))
"""
     c     b       a
0  1.5  2000    Ohio
1  1.7  2001    Ohio
2  1.6  2002    Ohio
3  2.4  2001  Nevada
4  2.9  2002  Nevada
"""
# 在python中a<b<c<...
