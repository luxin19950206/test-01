import talib
import numpy as np
import pandas as pd
import tushare as ts
# 写入一个文件到处的例子
input=open('sample.csv','r')
print(input.read()) #读取整个文件到单一字符串
print('-------')

input2=open('sample.csv')
print(input2.read(5))
print(input2.read(2)) #所以可以看出这种是取得n个字节
print('-------')

input3=open('sample.csv')
print(input3.readline())
print('-------')

input4=open('sample.csv')
print(input4.readlines()) #读取整个文件到字符串列表

for line in open('sample.csv'):
    print(line,end='')