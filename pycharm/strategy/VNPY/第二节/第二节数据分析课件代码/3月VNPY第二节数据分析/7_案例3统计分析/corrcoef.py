# -*- coding: ''tf-8 -*-
"""
Created on Wed Mar 29 00:34:28 2017

@author: Administrator
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
from statsmodels.tsa.stattools import adfuller

#首先想到利用统计套利，可能会想到两只股票的相关系数是否会让两只股票的走势有一种特定关系。
#我们来看看相关系数高的数据集具体长什么样
#X = np.random.rand(50)
#Y = X + np.random.normal(0, 0.1, 50)
#
#plt.scatter(X,Y)
#plt.xlabel('X Value')
#plt.ylabel('Y Value')
#
#print ('相关系数：' + str(np.corrcoef(X, Y)[0, 1]))

#从图像上看，数据基本都落在一条直线上那么它们之间的相关性就会很高。 
#接下来我们来看看两只股票价格之间相关性高长什么样


#此处时间一定要与回测的时间相对应，因为不同时间可能相关性不一致
start = '2014-01-01'
end   = '2016-11-01'
stock1='601618'
stock2='600026'
a1 = ts.get_hist_data(stock1, start,end)
a1 = a1['close']
a2 = ts.get_hist_data(stock2, start,end)
a2 = a2['close']

#处理缺失值
stock = pd.DataFrame()
stock['a1'] = a1
stock['a2'] = a2
stock = stock.dropna()
a1 = stock['a1']
a2 = stock['a2']

##画出散点图判断相关性
#plt.scatter(a1.values,a2.values)
#plt.xlabel(stock1)
#plt.ylabel(stock2)
#plt.title('Stock prices from ' + start + ' to ' + end)
#print (stock1+" and "+stock2+" corrcoef : ", np.corrcoef(a1,a2)[0,1])

##同样数据大多都集中在一条直线上
##找到相关性高的股票对，我们要来研究它们之间的价差，因为这是我们策略套利的关键

##a3表示他们的价差
a3=a1-a2
#a3.plot(figsize=(10,5))
#
#从图中看出，所以相关系数高，两者之间的价差不一定会围绕一个常数波动，
#价差会具有一定的变异性，即价差序列是非平稳的。 我们来检验下价差的平稳性。

adftest = adfuller(a3)#使用adf单位根检验平稳性
result = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
for key,value in adftest[4].items():
        result['Critical Value (%s)'%key] = value
print(result)
#
#上面使用了adf单位根检验，此处检验出来价差非平稳，套利策略的数据基础不好。
#

##进一步的我们来看看以均值加减一倍标准差是否包含了大部分的差价区间
mean=np.mean(a3)
std=np.std(a3)
up=mean+std
down=mean-std
time=a3.index
mean_line=pd.Series(mean,index=time)
up_line=pd.Series(up,index=time)
down_line=pd.Series(down,index=time)
set=pd.concat([a3,mean_line,up_line,down_line],axis=1)
set.columns=['spreadprice','mean','upper','down']
set.plot(figsize=(10,5))

#可以看到虽然包含了大部分价差区间，但是开仓次数太少，
#并且在2014年股票的差价都是在上开仓线附近小幅波动，
#会造成频繁开仓使得成本十分高。
#同时观察2015年价差出现极端值，此时如果开仓，价差不收敛，
#如果没做到好的平仓条件此时会造成大量亏损。

print'\n结论：此股票虽然相关性足够，但协整性不足，不可以进行套利\n'
print'简单来说我们无法利用这个不收敛的价差来进行套利'