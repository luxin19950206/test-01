# -*- coding: utf-8 -*-
"""
dataframe.iterrows()
Iterate over DataFrame rows as (index, Series) pairs.
"""
import pandas as pd
import tushare as ts

df = ts.get_hist_data('600848')
print(df)
# ====遍历dataframe的方式
# ===遍历行
for index, row in df.iteritems():
    print(index)  # 输出df的列名，即df的columns
    print(row)  # 输出各个列的具体内容
    print(type(row))  # 结果为series格式
    print(row['open'])
exit()

# ===遍历列
for index, col in df.iterrows():
    print(index)  # 输出df的index。即df的全部index
    print(col)  # 输出各个行的具体内容
    print(type(index))  # series
    print(type(col))

# ===比较好的遍历的方式
for index in df.index:
    print(index)  # 输出df的index，即df的全部index
    print(df.loc[index])  # 取一整行
    print(index, 'date')  # 取某一个元素
    df.at[index, '新增一列'] = 1  # 新增一列数据
    print(df)

