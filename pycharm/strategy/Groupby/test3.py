import talib
import numpy as np
import pandas as pd
import os
import tushare as ts
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

columns=pd.MultiIndex.from_arrays([['US','US','US','JP','JP'],[1,3,5,1,3]],names=['cty','tenor'])
print(columns)
hier_df=DataFrame(np.random.randn(4,5),columns=columns) #在导出后cty代表的是us和jp，tenor代表的是［1，3，5，1，3］
print(hier_df)
print(hier_df.groupby(level=1,axis=1).count())

