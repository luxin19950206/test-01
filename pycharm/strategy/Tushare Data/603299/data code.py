import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts
import os

# 得到603299近三年的数据
# ts.get_hist_data 相关数据 index为date
# open high close low volume price_change p_change涨跌幅 ma5 ma10 ma20 v_ma5 v_ma10 v_ma20 turnover换手率
open('603299_Month.csv','w')
df=ts.get_hist_data('603299',ktype='M') #获取上证指数k线数据
df.to_csv('603299_Month.csv')

open('603299_Week.csv','w')
df=ts.get_hist_data('603299',ktype='W') #获取上证指数k线数据
df.to_csv('603299_Week.csv')

open('603299_Daily.csv','w')
df=ts.get_hist_data('603299') #获取上证指数k线数据
df.to_csv('603299_Daily.csv')

open('603299_60_Mins.csv','w')
df=ts.get_hist_data('603299',ktype='60') #获取上证指数k线数据
df.to_csv('603299_60_Mins.csv')

open('603299_30_Mins.csv','w')
df=ts.get_hist_data('603299',ktype='30') #获取上证指数k线数据
df.to_csv('603299_30_Mins.csv')

open('603299_15_Mins.csv','w')
df=ts.get_hist_data('603299',ktype='15') #获取上证指数k线数据
df.to_csv('603299_15_Mins.csv')

open('603299_5_Mins.csv','w')
df=ts.get_hist_data('603299',ktype='5') #获取上证指数k线数据
df.to_csv('603299_5_Mins.csv')

# 历史分笔数据 获取2016-01-11以及2016-01-12的分笔数据
open('603299_fb060111.csv','w')
df = ts.get_tick_data('603299',date='2016-01-11')
df.to_csv('603299_fb060111.csv')

open('603299_fb060112.csv','w')
df = ts.get_tick_data('603299',date='2016-01-12')
df.to_csv('603299_fb060112.csv')

# # 大单交易数据 获取2016-01-11以及2016-01-12的大于600手的数据，目前这个数据可能出现了bug
# open('603299_ddsj060111.csv','w')
# df = ts.get_sina_dd('603299', date='2016-01-11', vol=500)  #指定大于等于500手的数据
# df.to_csv('603299_ddsj060111.csv')
#
# open('603299_ddsj060112.csv','w')
# df = ts.get_sina_dd('603299', date='2016-01-12', vol=500)  #指定大于等于500手的数据
# df.to_csv('603299_ddsj060112.csv')