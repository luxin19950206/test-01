import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import os

# 得到创业板近三年的数据
# ts.get_hist_data 相关数据 index为date+时间
# open high close low volume price_change p_change涨跌幅 ma5 ma10 ma20 v_ma5 v_ma10 v_ma20 turnover换手率
open('CYB_Month.csv', 'w')
df = ts.get_hist_data('cyb', ktype='M')  # 获取上证指数k线数据
df.to_csv('CYB_Month.csv')

open('CYB_Week.csv', 'w')
df = ts.get_hist_data('cyb', ktype='W')  # 获取上证指数k线数据
df.to_csv('CYB_Week.csv')

open('CYB_Daily.csv', 'w')
df = ts.get_hist_data('cyb')  # 获取上证指数k线数据
df.to_csv('CYB_Daily.csv')

open('CYB_60_Mins.csv', 'w')
df = ts.get_hist_data('cyb', ktype='60')  # 获取上证指数k线数据
df.to_csv('CYB_60_Mins.csv')

open('CYB_30_Mins.csv', 'w')
df = ts.get_hist_data('cyb', ktype='30')  # 获取上证指数k线数据
df.to_csv('CYB_30_Mins.csv')

open('CYB_15_Mins.csv', 'w')
df = ts.get_hist_data('cyb', ktype='15')  # 获取上证指数k线数据
df.to_csv('CYB_15_Mins.csv')

open('CYB_5_Mins.csv', 'w')
df = ts.get_hist_data('cyb', ktype='5')  # 获取上证指数k线数据
df.to_csv('CYB_5_Mins.csv')
