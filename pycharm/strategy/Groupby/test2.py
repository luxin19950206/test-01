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
print(people)

mapping = {'a': 'red', 'b': 'red', 'c': 'blue', 'd': 'blue', 'f': 'orange'}
print(people.groupby(mapping,axis=1).sum())

my_series = Series(mapping)
print(my_series)
print(people.groupby(my_series,axis=1).count())