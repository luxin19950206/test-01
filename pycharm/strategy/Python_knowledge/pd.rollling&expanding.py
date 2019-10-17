from pandas import DataFrame, Series
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# 判断rolling_max的作用，判断windows区间内最大的值，并且不断地rolling，直到最后一个
"""
pd.rolling_max(arg, window, min_periods=None, freq=None, center=False, how='max', **kwargs)
Moving maximum, Moving max of 1d array of dtype=float64 along axis=0 ignoring NaNs.
arg: Series,DataFrame
wwindows: int
    size of the moving windows. This is the number of obeservations used for calculating the statistic
min_periods: int, default None
    Minimum number of observations in window required to have a value (otherwise result is NA).
    需要有值的最小范围的数据
    例如min_periods=1时，则代表从前期的数据从最小的1开始算
    min_periods=2时，则代表从前期的数量从最小的2开始算，那么第一个数量就会显示为Nan
    可以相应地取代下方函数的expanding.max

freq: string or DateOffset object, optional (default None)
    Frequency to conform the data to before computing the statistic. Specified as a frequency string or DateOffset object.
how: string,default 'max'
    Method for down- or re-sampling

Rolling.count()	rolling count of number of non-NaN
Rolling.sum()	rolling sum
Rolling.mean()	rolling mean
Rolling.median()	rolling median
Rolling.var()	rolling variance
Rolling.std()	rolling standard deviation 标准差
Rolling.min()	rolling minimum
Rolling.max()	rolling maximum
Rolling.corr()	rolling sample correlation
Rolling.cov()	rolling sample covariance
Rolling.skew()	Unbiased rolling skewness
Rolling.kurt()	Unbiased rolling kurtosis
Rolling.apply()	rolling function apply
Rolling.quantile()	rolling quantile
Window.mean()	window mean
Window.sum()	window sum
"""
sf = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'year': [2000, 2001, 2002, 2001, 2002],
      'pop': [0, 1, 1, 0, 3]}
df = DataFrame(sf, index=['a', 'b', 'c', 'd', 'e'])
# rolling的另外一种写法
# df['最近N1个交易日的最高点'] = df['pop'].rolling(2).max()
"""
pd.rolling_max好像被取消不用了
"""
df['最近N1个交易日的最高点'] = pd.rolling_max(df['pop'], 4)
df['最近N1个交易日的最高点'].fillna(value=pd.expanding_max(df['pop']), inplace=True)
df['最近N个交易日的最高点'] = df['pop'].rolling(4, min_periods=1).max()
print(df)

# 判断expanding_max的作用。不断扩大的最大值，从一开始至今的最大值
"""
pf.expanding_max(arg, min_period=1, freq=None, **kwargs)
Expanding maximum, Moving max of 1d array of dtype=float64 along axis=0 ignoring NaNs.
从一开始至今的最大值

arg: Series,DataFrame
min_periods : int, default None
    Minimum number of observations in window required to have a value (otherwise result is NA).
freq : string or DateOffset object, optional (default None)
    Frequency to conform the data to before computing the statistic. Specified as a frequency string or DateOffset object.


Expanding.count()	expanding count of number of non-NaN
Expanding.sum()	expanding sum
Expanding.mean()	expanding mean
Expanding.median()	expanding median
Expanding.var()	expanding variance
Expanding.std()	expanding standard deviation
Expanding.min()	expanding minimum
Expanding.max()	expanding maximum
Expanding.corr()	expanding sample correlation
Expanding.cov()	expanding sample covariance
Expanding.skew()	Unbiased expanding skewness
Expanding.kurt()	Unbiased expanding kurtosis
Expanding.apply()	expanding function apply
Expanding.quantile()	expanding quantile
"""

sf = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'year': [2000, 2001, 2002, 2001, 2002],
      'pop': [0, 1, 1, 0, 3]}
df = DataFrame(sf, index=['a', 'b', 'c', 'd', 'e'])
print(pd.expanding_max(df['pop']))

sf = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
      'year': [2000, 2001, 2002, 2001, 2002],
      'pop': [2, 1, 1, 0, 3]}
df = DataFrame(sf, index=['a', 'b', 'c', 'd', 'e'])
print(pd.expanding_max(df['pop']))
