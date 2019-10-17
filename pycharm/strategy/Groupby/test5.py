import talib
import numpy as np
import pandas as pd
import os
import tushare as ts
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

df=DataFrame({'key1':['a','a','b','b','a'],
              'key2':['one','two','one','two','one'],
              'data1':np.random.randn(5),
              'data2':np.random.randn(5)})

k1_means=df.groupby('key1').mean().add_prefix('mean_')
a=pd.merge(df,k1_means,left_on='key1',right_index=True)
print(a)

a=pd.pivot_talbe(row='key1')
print(a)