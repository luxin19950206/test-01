import talib
import numpy as np
import pandas as pd
import os
import tushare as ts
from pandas import DataFrame, Series
import matplotlib.pyplot as plt


# 运用talib计算MA的方法
def talib_ma(close):
    MA5 = talib.MA(close, 5)  # 得到的数据是由近期到远期的，同时前4个数据是不存在的
    MA10 = talib.MA(close, 10)
    for i in range(len(close)):
        if MA5[i] > MA10[i] and MA5[i + 1] < MA10[i + 1]:  # 金叉
            return df.date[i], 'buy'  # 导出出现金叉的时间并标记buy
        if MA5[i] < MA10[i] and MA5[i + 1] > MA10[i + 1]:  # 死叉
            return df.date[i], 'sell'


# 利用rolling_mean计算MA以及EMA
def my_line_ma(close):
    ma_list = [5, 10, 20]
    for ma in ma_list:
        df['my_MA' + str(ma)] = pd.rolling_mean(close, ma)
    for ma in ma_list:
        df['my_EMA' + str(ma)] = pd.ewma(close, span=ma)


# 运用pandas自带的ewma编写的MACD策略
def pd_MACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    :param price:  这里输入收盘价
    :param fastperiod:
    :param slowperiod:
    :param signalperiod:
    :return:
    """
    ema12 = pd.ewma(price, span=fastperiod)
    ema26 = pd.ewma(price, span=slowperiod)
    DIF = ema12 - ema26
    DEA = pd.ewma(DIF, span=signalperiod)
    MACD = 2 * (DIF - DEA)
    return DIF, DEA, MACD


# 运用talib编写的MACD策略
def talib_MACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    :param price:
    :param fastperiod:
    :param slowperiod:
    :param signalperiod:
    :return:
    """
    DIF, DEA, macd = talib.MACD(price, fastperiod, slowperiod, signalperiod)
    MACD = 2 * macd
    return DIF, DEA, MACD
