import talib
import numpy as np
import pandas as pd
import tushare as ts
import os

# input1=open('code.csv')
# print(input.read())
# print('------')

input2 = open('code.csv')
print(input2.readlines())
print('------')

input3 = open('code.csv')
print(input3.readline())
print(input3.readline())
print('------')

print(pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Tushare Data/code.csv'))  # 读取后的数据类似与Dataframe
