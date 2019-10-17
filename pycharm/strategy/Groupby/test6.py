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

key = ['one', 'two', 'one', 'two', 'one']
print(people)
print(key)
print(people.groupby(key).mean())
print(people.groupby(key).transform(np.mean))


def demean(arr):
    return arr - arr.mean()


demeaned = people.groupby(key).transform(demean)
print(demeaned)
