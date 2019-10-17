# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas import Series, DataFrame


df = pd.DataFrame([10,20,30,40],columns=['number'],index = ['a','b','c','d'])

df['floats'] = (1.5,2.5,3.5,4.5)


df.append(pd.DataFrame({'number':100,'floats':5.7},index=['z']))

df['squares'] = (1,4,9,16)

df[['number','squares']].mean()
df[['number','squares']].std()



a = np.random.standard_normal((9,4))

df = pd.DataFrame(a)
#print df

df.columns = [['No1','No2','No3','No4']]
#print df
#
#print df['No2'][3]


dates = pd.date_range('2015-1-1',periods = 9,freq = 'D')
#print dates
df.index = dates
print df