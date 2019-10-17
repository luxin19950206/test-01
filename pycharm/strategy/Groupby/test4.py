import talib
import numpy as np
import pandas as pd
import os
import tushare as ts
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

people = DataFrame(np.random.randn(5, 5),
                   columns=['a', 'b', 'c', 'd', 'e'],
                   index=['joe', 'steve', 'wes', 'jim', 'travis'])

group=people.groupby(['a', 'b'])
print(group['a','b'].mean())
print(group['a','b'].agg(['mean','count']))