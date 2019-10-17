import talib
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import tushare as ts


# 导入数据
def load_data():  # 倒入数据
    """
    :return: close
    """
    stocks = ts.get_today_all()['code'].values
    for stock in stocks:
        close = ts.get_h_data(stock, start='2015-01-01', end='2015-03-16')['close'].values  # 两个日期之间的前复权数据
        return close


# 运用pandas自带的ewma编写的MACD策略
def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
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
