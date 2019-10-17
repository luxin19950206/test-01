# -*- coding: utf-8 -*-
"""
pandas.merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False,
             sort=False, suffixes=('_x', '_y'), copy=True, indicator=False)
Merge DataFrame objects by performing a database-style join operation by columns or indexes.
If joining columns on columns, the DataFrame indexes will be ignored. Otherwise if joining indexes on indexes or
indexes on a column or columns, the index will be passed on.
根据一个或者多个键将不同的DataFrame中的行链接起来

left:DataFrame
right:DataFrame
how : {‘left’, ‘right’, ‘outer’, ‘inner’}, default ‘inner’ how指的是合并的方式
    left: use only keys from left frame (SQL: left outer join) 以left为准
    right: use only keys from right frame (SQL: right outer join) 以right为准
    outer: use union of keys from both frames (SQL: full outer join) 求取的是键的并集，全部
    inner: use intersection of keys from both frames (SQL: inner join) 结果中的键是交集，共有部分
on : label or list
    Field names to join on. Must be found in both DataFrames. If on is None and not
    merging on indexes, then it merges on the intersection of the columns by default.
    on指的是用于链接的列索引名称，必须存在于左右两个DataFrame中，必须存在于左右两个DataFrame中，必须存在于左右两个DataFrame中
    如果没有指定，则以两个DataFrame的列名交集作为链接键
left_on : label or list, or array-like
    Field names to join on in left DataFrame. Can be a vector or list of vectors of the
    length of the DataFrame to use a particular vector as the join key instead of columns.
right_on : label or list, or array-like
    Field names to join on in right DataFrame or vector/list of vectors per left_on docs
sort : boolean, default False
    Sort the join keys lexicographically in the result DataFrame
    sort＝True时会按照键进行排序
suffixes : 2-length sequence (tuple, list, ...)
    Suffix to apply to overlapping column names in the left and right side, respectively
    若两边有相同的列名的时候，可以这些列的后面加上注释
    eg：suffixes=['_股票', '_指数']
indicator=True,默认为False
    增加_merge列，表明这一行数据来自哪个表，会显示数据来自于right、left还是both
"""

import pandas as pd
from pandas import DataFrame, Series

# 多对一的合并，df1中多种类key，df2中key的每个值则只对应一行
df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
"""
   data1 key
0      0   b
1      1   b
2      2   a
3      3   c
4      4   a
5      5   a
6      6   b
"""
df2 = DataFrame({'key': ['a', 'b', 'd'],
                 'data2': range(3)})
"""
   data2 key
0      0   a
1      1   b
2      2   d
"""
df3 = DataFrame({'lkeys': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
"""
   data1 lkeys
0      0     b
1      1     b
2      2     a
3      3     c
4      4     a
5      5     a
6      6     b
"""
df4 = DataFrame({'rkeys': ['a', 'b', 'd'],
                 'data2': range(3)})
"""
   data2 rkeys
0      0     a
1      1     b
2      2     d
"""
print(pd.merge(left=df1, right=df2, on='key', how='inner'))
# 根据key将两个DataFrame的行链接起来,取交集
"""
   data1 key  data2
0      0   b      1
1      1   b      1
2      6   b      1
3      2   a      0
4      4   a      0
5      5   a      0
"""
print(pd.merge(left=df1, right=df2, on='key', how='left'))
# 两个df都有key时，将left中的key作为链接键进行合并，如果right中没有的计为Nan
"""
   data1 key  data2
0      0   b    1.0
1      1   b    1.0
2      2   a    0.0
3      3   c    NaN
4      4   a    0.0
5      5   a    0.0
6      6   b    1.0 这里的key是left中的key
"""
print(pd.merge(left=df1, right=df2, on='key', how='right'))
# 两个df都有key的将right中的key作为链接键进行合并，如果left中没有的计为Nan
"""
   data1 key  data2
0    0.0   b      1
1    1.0   b      1
2    6.0   b      1
3    2.0   a      0
4    4.0   a      0
5    5.0   a      0
6    NaN   d      2
right中的key只有abd三个数，而一个b在left中对应着三个数，所以整合后b扩大为3个
"""
print(pd.merge(left=df1, right=df2, on='key', how='outer'))
# 根据key将两个DataFrame的行链接起来,取并集
"""
   data1 key  data2
0    0.0   b    1.0
1    1.0   b    1.0
2    6.0   b    1.0
3    2.0   a    0.0
4    4.0   a    0.0
5    5.0   a    0.0
6    3.0   c    NaN
7    NaN   d    2.0
"""
print(pd.merge(left=df3, right=df4, left_on='lkeys', right_on='rkeys', how='inner'))
"""
   data1 lkeys  data2 rkeys
0      0     b      1     b
1      1     b      1     b
2      6     b      1     b
3      2     a      0     a
4      4     a      0     a
5      5     a      0     a
"""
print(pd.merge(left=df3, right=df4, left_on='lkeys', right_on='rkeys', how='outer'))
"""
   data1 lkeys  data2 rkeys
0    0.0     b    1.0     b
1    1.0     b    1.0     b
2    6.0     b    1.0     b
3    2.0     a    0.0     a
4    4.0     a    0.0     a
5    5.0     a    0.0     a
6    3.0     c    NaN   NaN
7    NaN   NaN    2.0     d
"""
print(pd.merge(left=df3, right=df4, left_on='lkeys', right_on='rkeys', how='left'))
"""
   data1 lkeys  data2 rkeys
0      0     b    1.0     b
1      1     b    1.0     b
2      2     a    0.0     a
3      3     c    NaN   NaN
4      4     a    0.0     a
5      5     a    0.0     a
6      6     b    1.0     b
"""

# 多对多合并，这里需要考虑到笛卡尔积，例如下方由于df1中有3a，3b，df2中有2a，1b，这样就得到6a，3b
df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})  # 其中有3a，3b，1c
"""
   data1 key
0      0   b
1      1   b
2      2   a
3      3   c
4      4   a
5      5   a
6      6   b
"""
df2 = DataFrame({'key': ['a', 'a', 'b', 'd'],
                 'data2': range(4)})  # 其中有2a，1b，1d
"""
   data2 key
0      0   a
1      1   a
2      2   b
3      3   d
"""

print(pd.merge(df1, df2, on='key'))
"""
   data1 key  data2
0      0   b      2
1      1   b      2
2      6   b      2
3      2   a      0
4      2   a      1
5      4   a      0
6      4   a      1
7      5   a      0
8      5   a      1
6a，3b
"""

print(pd.merge(df1, df2, on='key', how='outer'))
"""
    data1 key  data2
0     0.0   b    2.0
1     1.0   b    2.0
2     6.0   b    2.0
3     2.0   a    0.0
4     2.0   a    1.0
5     4.0   a    0.0
6     4.0   a    1.0
7     5.0   a    0.0
8     5.0   a    1.0
9     3.0   c    NaN
10    NaN   d    3.0
6a，3b，1c，1d
"""

print(pd.merge(df1, df2, on='key', how='left'))
"""
   data1 key  data2
0      0   b    2.0
1      1   b    2.0
2      2   a    0.0
3      2   a    1.0
4      3   c    NaN
5      4   a    0.0
6      4   a    1.0
7      5   a    0.0
8      5   a    1.0
9      6   b    2.0
6a，3b，1c
"""