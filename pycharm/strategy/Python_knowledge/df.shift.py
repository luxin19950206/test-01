# -*- coding: utf-8 -*-
"""
DataFrame.shift(period=1,freq=None,axis=0)
periods:类型为int，代表移动的幅度，可以是正数，也可以是负数，这里移动的是数据而不是索引，移动后没有赋值的为nan
当为正数的时候，就向下移动
"""

from pandas import DataFrame, Series

sf = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'year': [1, 2, 3, 4, 5],
      'pop': [0, 1, 1, 0, 0]}
df = DataFrame(sf, index=['a', 'b', 'c', 'd', 'e'])
print(df)
print(df['year'].shift())
"""
   pop   state  year
a    0    Ohio     1
b    1    Ohio     2
c    1    Ohio     3
d    0  Nevada     4
e    0  Nevada     5
a    NaN
b    1.0
c    2.0
d    3.0
e    4.0
Name: year, dtype: float64
"""

"""
DataFrame.diff(period=1,axis=0)
1st discrete difference of object
求本行数据和上一行数据相减得到的值

periods : int, default 1
    Periods to shift for forming difference
axis : {0 or ‘index’, 1 or ‘columns’}, default 0
    Take difference over rows (0) or columns (1).

a    NaN
b    1.0
c    1.0
d    1.0
e    1.0
Name: year, dtype: float64
"""
print(df['year'].diff())

"""
DataFrame.pct_change(periods=1, fill_method='pad', limit=None, freq=None, **kwargs)
求两个数之间的比例减1，即(b－a)/a（当period为1时）或者b/a－1（今日的收盘价除以昨天的收盘价然后减去1）

periods : int, default 1
      Periods to shift for forming percent change
fill_method : str, default ‘pad’
      How to handle NAs before computing percent changes
limit : int, default None
      The number of consecutive NAs to fill before stopping
freq : DateOffset, timedelta, or offset alias string, optional
      Increment to use from time series API (e.g. ‘M’ or BDay())

a         NaN
b    1.000000
c    0.500000
d    0.333333
e    0.250000
Name: year, dtype: float64
"""
print(df['year'].pct_change())
