# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:38:27 2017

@author: Administrator
"""

# 导入需要的库
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import talib as ta
import datetime
import numpy as np
 
#np.set_printoptions(precision=30)

hs300 = ts.get_hist_data('hs300')
hist_data = hs300[['open','high','low','close','volume','ma5','ma10']]

# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
data_list = []
data_volume=[]
data_ma=[]
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
    t = date2num(date_time)
    open,high,low,close = row[:4]
    volume = row[4]
    ma1 = row[4:]
    datas = (t,open,high,low,close)
    data_v = (t,volume)
    data_list.append(datas)
    data_volume.append(data_v)
    volume = np.array(data_volume)
    ma = np.array(ma1)

 
## 创建子图
##设置子图1
fig,(ax1,ax2) = plt.subplots(2,sharex=True,figsize=(12,6))
mpf.candlestick_ohlc(ax1,data_list,width=1.5,colorup='r',colordown='green')
ax1.set_title('Hs300 Index')
ax1.set_ylabel('Price')
ax1.grid(True)
ax1.xaxis_date()

#设置子图2
plt.bar(volume[:,0],volume[:,1]/10000)
ax2.set_ylabel('volume(wan)')
ax2.grid(True)
ax2.autoscale_view()


plt.setp(plt.gca().get_xticklabels(),rotation = 30)



