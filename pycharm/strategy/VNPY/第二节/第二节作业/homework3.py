
# coding: utf-8

# In[2]:

get_ipython().magic(u'matplotlib inline')
import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import datetime
import numpy as np
import talib as ta


# In[3]:

sh = ts.get_hist_data('sh')
hist_data = sh[['open','high','low','close','volume']]


# In[4]:

hist_data=hist_data.sort_index()
hist_data.head(5)


# In[5]:

data_list = []
data_volume=[]
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
    t = date2num(date_time)
    open,high,low,close = row[:4]
    volume = row[4]
    datas = (t,open,high,low,close)
    data_v = (t,volume)
    data_list.append(datas)
    data_volume.append(data_v)
    volume = np.array(data_volume)


# In[6]:

volume


# In[79]:

S = 12;
L = 26;
EMA1 = ta.EMA(hist_data['close'].values, S);
EMA2 = ta.EMA(hist_data['close'].values, L);
DIFF = EMA1-EMA2;
M = 10;
DEA = ta.EMA(DIFF, M);
MACD = 2*(DIFF-DEA);


# In[85]:

fig,(ax1,ax2,ax3) = plt.subplots(3,sharex=True,figsize=(12,6))

mpf.candlestick_ohlc(ax1,data_list,width=1.5,colorup='r',colordown='green')
ax1.set_title('szzs Index')
ax1.set_ylabel('Price')
ax1.grid(True)
ax1.xaxis_date()


ax2.bar(volume[:,0],volume[:,1]/10000)
ax2.set_ylabel('volume(wan)')
ax2.grid(True)
ax2.autoscale_view()



# ax2.plot(DIFF)
#ax2.plot(DEA)
ax3.bar(volume[:,0],MACD)
ax3.set_ylabel('macd')


# In[ ]:

# ax2.plot(DIFF)
# ax2.plot(DEA)
# ax2.bar(range(len(MACD)),MACD)

