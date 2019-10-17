# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:59:04 2017

@author: Administrator
"""
import numpy as np
import pandas as pd
import tushare as ts
import talib as ta


sh = ts.get_hist_data('sh')
sh = sh.sort_index()
close = sh[['close','volume']]

#函数用的price必须为narray
upper,middle,lower = ta.BBANDS(
                                sh['close'].values,
                                timeperiod=20,
                                nbdevup = 2,
                                nbdevdn = 2,
                                matype = 0
                               )


close.loc[:,'upper'] = upper
close.loc[:,'middle']= middle
close.loc[:,'lower'] = lower



close[['close','middle','upper','lower']].plot(figsize=(15,8),grid = True)


#sh[['close','mma5']].plot(figsize = (15,8),grid = True)