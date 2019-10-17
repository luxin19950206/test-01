# 高送转预期炒作选股策略
import talib
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts


# 选择有高送转预期的股票：
# 必要条件：
# 1,资本公积金大于2，每股盈利大于0.2，每股未分配利润＊资本公积金>10
# 2,1-2年内没有过高送转
# 3,基金家数少
# 4,年报高送转炒作的话在12月底或者1月初有解禁，中报高送转在6、7月有解禁
# 5,历史股性活跃，过去一年内有超过3个涨停板
# 6,实际流通市值小于30亿

# 非必要条件：
# 次新股
# 实际流通市值小于20亿
# 曾经作为前一阶段的高送转预期炒作的股票，也就是往前推半年，有涨幅超过30%的阶段


df = ts.get_stock_basics()
'''
包含code代码（index）,name名字,industry行业,area地区,pe市盈率,outstanding流通股本,totals总股本,totalAssets总资产,
liquidAssets流动资产,fixedAssets固定资产,reserved公积金,reservedPerShare每股公积金,esp每股收益,bvps每股净资产,pb市净率,timeToMarket上市日期、
'''
df2 = ts.get_today_all()
'''
包括index为数字，code代码,name名称,changepercent涨跌幅,trade现价,open开盘价,high最高价,low最低价,settlement最日收盘价,
volume成交量,turnoverratio换手率,amount成交量,per市盈率,pb市净率,mktcap总市值,nmc流通市值
'''
df2.index = df2.code

def GSZ():  # 高送转相关股票
    for stock in df.index:
        ReservedPerShare = df.ix[stock]['reservedPerShare']  # 每股资本公积金大于2
        Time=
        ESP = df.ix[stock]['esp']  # 每股收益大于0.2
        NMC = df2[stock]['nmc']  # 流通市值小于30亿
        if ReservedPerShare > 2 and ESP > 0.2 and NMC < 300000:
            return stock