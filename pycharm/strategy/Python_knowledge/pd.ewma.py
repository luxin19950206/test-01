"""
pandas.ewma(arg, com=None, span=None, halflife=None, min_periods=0, freq=None, adjust=True, how=None, ignore_na=False)
Exponentially-weighted moving average 指数加权移动平均值

arg : Series, DataFrame
com : float. optional
    Center of mass: alpha = 1 / (1 + com),
span : float, optional span改动后相当于股票软件中的ema指数（指数平滑移动平均线）
    Specify decay in terms of span, alpha = 2 / (span + 1)
"""
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Tushare Data/000001/000001_Daily.csv', parse_dates=['date'])
df.sort_values(by='date', inplace=True)
df['ema'] = pd.ewma(df['close'], span=5)  # 这个得出来的结果等同于股票软件中的ema
df['ma'] = pd.rolling_mean(df['close'], 5)  # 这个得出来的结果等同于股票软件中的均线
print(df[['date', 'ema', 'ma']])
