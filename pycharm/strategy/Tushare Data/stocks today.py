import talib
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts

# ts.get_today_all() 得到的是实时的数据，index为数字
# code,name,changepercent涨跌幅,trade现价,open,high,low,settlement最日收盘价
# volume,turnoverratio,amount,per市盈率,pb市净率,mktcap总市值
# nmc流通市值
open('stocks today.csv','w')
df = ts.get_today_all()
df.to_csv('stocks today.csv')