import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import os

# 得到上证指数近3年的数据，目前截至到2016.11.23
# ts.get_hist_data 相关数据 index为date+时间
# open high close low volume price_change p_change涨跌幅 ma5 ma10 ma20 v_ma5 v_ma10 v_ma20 turnover换手率

open('SZ_Month.csv', 'w')
df = ts.get_hist_data('sh', ktype='M')  # 获取上证指数k线数据
df.to_csv('SZ_Month.csv')

open('SZ_Week.csv', 'w')
df = ts.get_hist_data('sh', ktype='W')  # 获取上证指数k线数据
df.to_csv('SZ_Week.csv')

open('SZ_Daily.csv', 'w')
df = ts.get_hist_data('sh')  # 获取上证指数k线数据
df.to_csv('SZ_Daily.csv')

open('SZ_60_Mins.csv', 'w')
df = ts.get_hist_data('sh', ktype='60')  # 获取上证指数k线数据
df.to_csv('SZ_60_Mins.csv')

open('SZ_30_Mins.csv', 'w')
df = ts.get_hist_data('sh', ktype='30')  # 获取上证指数k线数据
df.to_csv('SZ_30_Mins.csv')

open('SZ_15_Mins.csv', 'w')
df = ts.get_hist_data('sh', ktype='15')  # 获取上证指数k线数据
df.to_csv('SZ_15_Mins.csv')

open('SZ_5_Mins.csv', 'w')
df = ts.get_hist_data('sh', ktype='5')  # 获取上证指数k线数据
df.to_csv('SZ_5_Mins.csv')
