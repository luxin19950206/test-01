# -*- coding: utf-8 -*-
"""
DataFrame.apply(func, axis=0, broadcast=False, raw=False, reduce=None, args=(), **kwds)
Applies function along input axis of DataFrame.
例如df.apply(func)表示对df进行func的函数操作
"""
import pandas as pd

df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/sz300001.csv', encoding='gbk')


def func(x): return x * 20


print(df['收盘价'].apply(func))
