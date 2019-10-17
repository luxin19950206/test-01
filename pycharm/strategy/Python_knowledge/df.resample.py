"""
DataFrame.resample(rule, how=None, axis=0, fill_method=None, closed=None, label=None, convention='start', kind=None,
                    loffset=None, limit=None, base=0, on=None, level=None)
Convenience method for frequency conversion and resampling of time series. Object must have a datetime-like index
(DatetimeIndex, PeriodIndex, or TimedeltaIndex), or pass datetime-like values to the on or level keyword.
将时间序列从一个频率转换到另一个频率的处理过程,object数据必须有一个datetime－like的index或者令on等于datetime中相关的时间参数

rule:string
    the offset string or object representing target conversion
    表示频率值
how: defalut 'mean'
    用于产生聚合值的函数名或者数组函数，例如'mean'，'ohlc'，'np.max'等，默认为'mean'，常用的值还包括'first'，'last'，'median'，'max'，'min'
fill_method：default＝None
    升采样时如何插值，比如'ffill'或者'bfill'，
closed：default=right
    在降采样中，各时间段的哪一端是闭合（即包含）的，'right'或者'left'
label＝'right'
    在降采样过程中，如何设置聚合值的标签，'right'或者'left'(面元的右边或者左边界)
"""

import pandas as pd
from pandas import DataFrame, Series

index = pd.date_range('3/1/2010', periods=9, freq='T')
series = Series(range(9), index=index)
print(series)
print(series.resample(rule='3T', how='sum'))
print(series.resample(rule='3T').sum())  # 最好还是用.sum函数
