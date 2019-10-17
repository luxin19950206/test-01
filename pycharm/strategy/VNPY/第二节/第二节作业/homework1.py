
# coding: utf-8

# In[77]:


import tushare as ts
import talib as ta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[78]:

hs300=ts.get_hist_data('hs300')


# In[79]:

hs300=hs300.sort_index()


# In[80]:

upper,middle,lower = ta.BBANDS(
                                hs300['close'].values,
                                timeperiod=20,
                                nbdevup = 2,
                                nbdevdn = 2,
                                matype = 0
                               )


# In[81]:

hs300.loc[:,'upper']=np.round(upper)
hs300.loc[:,'middle']=np.round(middle)
hs300.loc[:,'lower']=np.round(lower)


# In[82]:

hs300[['close','upper','middle','lower']].plot(figsize=(8,3),grid=True)
a=plt.setp(plt.gca().get_xticklabels(),rotation=20)


# In[83]:

hs300=hs300[['close','upper','middle','lower']]


# In[92]:

hs300['close-min']=hs300['close']-hs300['middle']
hs300['close-up']=hs300['close']-hs300['upper']
hs300['close-lo']=hs300['close']-hs300['lower']
hs300['ii']=range(len(hs300))
hs300['pos']=0


# In[104]:

hs300.ix[230:240]
#hs300.to_excel('bulin.xlsx')


# In[103]:

for index,r in hs300.iterrows():
        if  hs300.pos[hs300.ii==r.ii-1].values==0 and r['close-up']>0:
            hs300.loc[hs300.ii==r.ii,'pos']=1
        if hs300.pos[hs300.ii==r.ii-1].values==1 and r['close-min']>0:
            hs300.loc[hs300.ii==r.ii,'pos']=1
        if hs300.pos[hs300.ii==r.ii-1].values==0 and r['close-lo']<0:
            hs300.loc[hs300.ii==r.ii,'pos']=-1
        if  hs300.pos[hs300.ii==r.ii-1].values==-1 and r['close-min']<0:
            hs300.loc[hs300.ii==r.ii,'pos']=-1
      


# In[105]:

hs300['pos'].plot(lw=1.5,figsize=(8,3))


# In[106]:

hs300['market']=np.log(hs300['close']/hs300['close'].shift(1))
hs300['straegy']=hs300['pos'].shift(1)*hs300['market']


# In[107]:

hs300[['market','straegy']].cumsum().apply(np.exp).plot(figsize=(8,3),grid=True)

