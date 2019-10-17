# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""

import pandas as pd
high=[]
a = pd.read_csv('/Users/ShiRuo/PycharmProjects/strategy/Tushare Data/stocks today.csv')
d=a['low']
print(d)
for n in range(10):
    high.append(d[n])
print(max(high))