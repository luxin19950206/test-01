# -*- coding: utf-8 -*-
"""
@author: Xing
"""
import pandas as pd
import Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====读入数据
code = 'sz300001'
df = Functions.import_stock_data(code)

# =====rolling操作
# 计算'收盘价'这一列的均值
print(df['收盘价'].mean())
# 如何得到每一天的最近3天收盘价的均值呢？即如何计算常用的移动平均线？
# 使用rolling函数
df['收盘价_3天均值'] = df['收盘价'].rolling(3).mean()
print(df)
# rolling(n)即为取最近n行数据的意思，只计算这n行数据。后面可以接各类计算函数
print(df['收盘价'].rolling(3).max())
print(df['收盘价'].rolling(3).min())
print(df['收盘价'].rolling(3).std())

# =====expanding操作
# rolling可以计算每天的最近3天的均值，如果想计算每天的从一开始至今的均值，应该如何计算？
# 使用expanding操作
df['收盘价_至今均值'] = df['收盘价'].expanding().mean()
print(df)
# expanding即为取从头至今的数据。后面可以接各类计算函数
print(df['收盘价'].rolling(3).max())
print(df['收盘价'].rolling(3).min())
print(df['收盘价'].rolling(3).std())
