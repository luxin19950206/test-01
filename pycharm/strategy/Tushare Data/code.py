import talib
import numpy as np
import pandas as pd
import tushare as ts

# 得到所有的股票代码和名字 实时
df=ts.get_today_all()
output=open('code.csv','w')
df.to_csv('code.csv',columns=['code','name'])
# /Users/ShiRuo/PycharmProjects/untitled2/Tushare Data/code.np