# -*- coding: utf-8 -*-
"""
def set_index(self, keys, drop=True, append=False, inplace=False, verify_integrity=False):
Set the DataFrame index (row labels) using one or more existingcolumns. By default yields a new object.
将其中一个或多个列转化为行索引，并返回一个新对象
keys : column label or list of column labels / arrays
drop : boolean, default True 默认为True, 表示转换后会删除已经变成行索引的列
    Delete columns to be used as the new index
append : boolean, default False
    Whether to append columns to existing index
inplace : boolean, default False
    Modify the DataFrame in place (do not create a new object)
verify_integrity : boolean, default False
    Check the new index for duplicates. Otherwise defer the check untilnecessary. Setting to False will improve the
    performance of this method
"""

"""
def reset_index(self, level=None, drop=False, inplace=False, col_level=0, col_fill=''):
For DataFrame with multi-level index, return new DataFrame with labeling information in the columns under the index
names, defaulting to 'level_0', 'level_1', etc. if any are None. For a standard index,the index name will be used
(if set), otherwise a default 'index' or 'level_0' (if 'index' is already taken) will be used.
将已经层次化的索引转换回列里面，同时这个函数还能够重新建立index

level : int, str, tuple, or list, default None
      Only remove the given levels from the index. Removes all levels by default
drop : boolean, default False
      Do not try to insert index into DataFrame columns. This resets the index to the default integer index.
      如果drop=true，则意味着原有的index会被删除
      如果默认为false，则意味着原有的index会被作为一个列
inplace : boolean, default False
      Modify the DataFrame in place (do not create a new object)
col_level : int or str, default 0
      If the columns have multiple levels, determines which level the labels are inserted into. By default it is
      inserted into the first level.
col_fill : object, default ''
      If the columns have multiple levels, determines how the other levels are named.
      If None then the index name is repeated.
"""
from pandas import DataFrame

# 例子
sf = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'year': [2000, 2001, 2002, 2001, 2002],
      'pop': [3, 1, 1, 5, 0]}
df = DataFrame(sf)
df1 = df.set_index('state')  # 将state转换为index
df2 = df.set_index(['state', 'year'])  # 将state和year作为index
df3 = df.set_index('state')[['year', 'pop']]
df4 = df3.reset_index()
print('df', df)
print('df1', df1)
print('df2', df2)
print('df3', df3)
print('df4', df4)

# 下方的操作讲index重新从0到1进行重新排列
df.reset_index(inplace=True)
print('df5', df)
