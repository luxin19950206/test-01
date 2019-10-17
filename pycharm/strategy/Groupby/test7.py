import talib
import numpy as np
import pandas as pd
import os
import tushare as ts
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

frame = DataFrame({'data1': np.random.randn(10),
                   'data2': np.random.randn(10)})

factor = pd.cut(frame.data1, 4)
print(factor)
print(pd.value_counts(factor))

def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}

grouped=frame.data2.groupby(factor)
print(grouped.apply(get_stats))
print(grouped.agg(get_stats))