# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#设置参数
spread=3
#获取数据
hs300=ts.get_hist_data('hs300')
hs300=hs300.sort_index()

#显示沪深300三年走势
#hs300['close'].plot(figsize=(12,6))
#plt.setp(plt.gca().get_xticklabels(),rotation=20)
#plt.show()


#使用numpy画均线
hs300['short']=np.round(hs300['close'].rolling(window=10,center=False).mean(),2)
hs300['long']=np.round(hs300['close'].rolling(window=40,center=False).mean(),2)
hs300['short-long']=hs300['short']-hs300['long']
#显示走势以及均线
hs300[['close','short','long']].plot(figsize=(12,6))
plt.setp(plt.gca().get_xticklabels(),rotation=20)
plt.show()

#产生交易信号
hs300['signal']=np.where(hs300['short-long']>spread,1,0)
hs300['signal']=np.where(hs300['short-long']<spread,-1,hs300
['signal'])
#print hs300['signal'].value_counts()
#显示交易信号
hs300['signal'].plot(figsize=(8,4))
plt.ylim([-1.2,1.2])
plt.setp(plt.gca().get_xticklabels(),rotation=20)
plt.show()

#显示资金曲线
hs300['market']=np.log(hs300['close']/hs300['close'].shift(1))
hs300['straegy']=hs300['signal'].shift(1)*hs300['market']
hs300[['market','straegy']].cumsum().apply(np.exp).plot(figsize=(12,6))
plt.setp(plt.gca().get_xticklabels(),rotation=20)
plt.show()