import talib
import numpy as np
import pandas as pd
import tushare as ts

# 沪市融资融券汇总数据
# opDate:信用交易日期  rzye:本日融资余额(元)  rzmre: 本日融资买入额(元)  rqyl: 本日融券余量
# rqylje: 本日融券余量金额(元)  rqmcl: 本日融券卖出量  rzrqjyzl:本日融资融券余额(元)
open('rzrq_sz1.csv', 'w')
df = ts.sh_margins(start='2015-01-01', end='2015-06-01')
df.to_csv('rzrq_sz1.csv')

open('rzrq_sz2.csv', 'w')
df = ts.sh_margin_details(start='2015-06-01', end='2015-12-31')
df.to_csv('rzrq_sz2.csv')

# 深市融资融券汇总数据
open('rzrq_ss1.csv', 'w')
df = ts.sz_margins(start='2015-01-01', end='2015-06-01')
df.to_csv('rzrq_ss1.csv')

open('rzrq_ss2.csv', 'w')
df = ts.sz_margins(start='2015-06-01', end='2015-12-31')
df.to_csv('rzrq_ss2.csv')

# 沪市融资融券明细数据
# opDate:信用交易日期,stockCode:标的证券代码,securityAbbr:标的证券简称,rzye:本日融资余额(元),rzmre: 本日融资买入额(元)
# rzche:本日融资偿还额(元),rqyl: 本日融券余量,rqmcl: 本日融券卖出量,rqchl: 本日融券偿还量
# open('rzrq.csv', 'w')
# df = ts.sh_margin_details(start='2015-01-01', end='2015-06-31', symbol='601989')
# df.to_csv('rzrq.csv')
#
# 深市明细数据
# open('rzrq.csv')
# ts.sz_margin_details('2015-04-20') #深市融资融券明细一次只能获取一天的明细数据，如果不输入参数，则为最近一个交易日的明细数据