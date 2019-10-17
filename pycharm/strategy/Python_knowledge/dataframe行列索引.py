# -*- coding: utf-8 -*-
import pandas as pd

k_data = pd.read_csv('/Users/hengzong/Documents/pycharm/strategy/Tushare Data/000001/000001_30_Mins.csv')
"""Dataframe索引单行、多行数据"""
print(k_data[:2])  # 索引0、1两行数据
print(k_data[3:4])  # 索引第3行数据
# loc通过index进行索引，不过这组数据中
print(k_data.loc[0])  # 索引单行数据
print(k_data.loc[0:])  # 索引多行数据
# iloc通过行号（数字）来进行索引
print(k_data.iloc[0])  # 索引第0行数据
print(k_data.loc[0:])  # 索引多行数据
# ix通过行号或者index进行索引
print(k_data.ix[0:, 'open':'close'])

"""Dataframe索引多列数据"""
print(k_data.loc[0, 'open':'close'])
print(k_data.iloc[1, 0:])

"""Dataframe索引多行多列"""
print(k_data.loc[0:3, 'open':'close'])
print(k_data.iloc[0:, 3:])

"""Dataframe索引单个数据"""
print(k_data.loc[0, 'open'])
print(k_data.at[0, 'open'])
print(k_data.iloc[0, 1])
print(k_data.iloc[0, 1])
