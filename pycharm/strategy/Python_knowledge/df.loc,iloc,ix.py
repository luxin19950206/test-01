# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

df = pd.DataFrame(np.arange(9).reshape((3, 3)), columns=['a', 'b', 'c'], index=['d', 'e', 'f'])
"""
   a  b  c
d  0  1  2
e  3  4  5
f  6  7  8
"""

# 另外一种取dataframe种多列的方式是
print(df[1:2])

# loc：通过行标签索引数据
print(df.loc['d'])  # 索引d行，但是这种应该是series格式
"""
a    0
b    1
c    2
Name: d, dtype: int64
"""
print(df.loc['e':])  # 索引多行
"""
   a  b  c
e  3  4  5
f  6  7  8
"""
print(df.loc['d', 'a':'c'])  # 索引d行，多列
"""
a    0
b    1
c    2
Name: d, dtype: int64
"""
print(df.loc['d':'e', 'a':'c'])  # 索引多行多列
"""
   a  b  c
d  0  1  2
e  3  4  5
"""
print(df.loc['d', ['a', 'b']])  # 索引d行，ab列
"""
a    0
b    1
Name: d, dtype: int64
"""
print(df.loc['d', 'a'])  # 索引某个数据
"""
0
"""
print(df.at['d', 'a'])  # 索引某个数据
"""
0
"""

# iloc：通过行号索引数据
print(df.iloc[1])  # 索引第1行
"""
a    3
b    4
c    5
Name: e, dtype: int64
"""
print(df.iloc[1:])  # 索引第多行
"""
   a  b  c
e  3  4  5
f  6  7  8
"""
print(df.iloc[1, 0:])  # 索引第1行，多列
"""
a    3
b    4
c    5
Name: e, dtype: int64
"""
print(df.iloc[0:, 1:])  # 索引多行多列
"""
   b  c
d  1  2
e  4  5
f  7  8
"""
print(df.iloc[1, 2])  # 索引单个数据
"""
5
"""
print(df.iat[1, 2])  # 索引单个数据
"""
5
"""

"""
ix：通过行号、行标签等索引数据
ix中先是行再是列
"""
for i in range(len(df.index)):
    if df.ix[i, 'key events'] is not None:
        df['key'] = 0
    else:
        df['key'] = 1