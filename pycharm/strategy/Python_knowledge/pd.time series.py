"""
字符串日期
'1/10/2011' 1月10号
'20110110'
'2011-01-01'
'2011'
'2011-05'
'5-2011'

datetime
datetime(2011,1,10)
datetime(1/10/2011)
"""

from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from dateutil.parser import parse
from pandas import DataFrame, Series



# ===datetime通常以毫秒形式储存日期和时间
now = datetime.now()
print(now)
"""2016-12-26 10:20:45.037502"""
start = datetime(2011, 1, 1)  # datetime.datetime格式
print(start)
"""2011-01-01 00:00:00"""
delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
print(delta)
print(delta.days)
print(delta.seconds)
"""
926 days, 15:45:00
926
56700
"""

# ===timedelta表示两个datetime对象之间的时间差
print(start + timedelta(12))
print(start - 2 * timedelta(12))
"""
2011-01-13 00:00:00
2010-12-08 00:00:00
"""

# ===利用str或strftime方法传入一个格式化字符串，从而使datetime和pandas的timestamp对象可以呗格式化为字符串
print(str(start))  # 字符串格式
print(start.strftime('%Y-%m-%d'))

# ===dateutil可以解析几乎全部的日期表现形式
print(parse('2011-1-3'))
print(parse('jan 31, 1997 10.30 PM'))
print(parse('6/12/2011', dayfirst=True))  # 日期通常出现在月的前面，传入dayfirst=true即可解决这个问题
"""
2011-01-03 00:00:00
1997-01-31 22:00:00
2011-12-06 00:00:00
"""

# ===to_datetime方法可以解析多种不同的日期表现形式
datestrs = ['7/6/2011', '8/6/2011']
print(pd.to_datetime(datestrs))

# ====时间序列基础，对series的相关操作
# pandas最基本的时间序列就是以时间轴为索引的Series
date = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7), datetime(2011, 1, 8), datetime(2011, 1, 10),
        datetime(2011, 1, 12)]
ts = Series(np.random.randn(6), index=date)
print(ts)
print(type(ts))  # <class 'pandas.core.series.Series'>
print(type(ts.index))  # <class 'pandas.tseries.index.DatetimeIndex'>
print(ts.dtypes)  # float64
print(ts.index.dtype)  # datetime64[ns]
print(ts.index)
print(ts.index[0])
"""2011-01-02 00:00:00"""

# ===索引、切片
print(ts[ts.index[1]])
print(ts['1/10/2011'])  # 传入一个可以被解释为日期的字符串
print(ts['20110110'])

# 对于较长的时间序列，只需传入'年'或'年月'即可轻松选取数据的切片
print(pd.date_range('20110101', periods=2))
"""DatetimeIndex(['2011-01-01', '2011-01-02'], dtype='datetime64[ns]', freq='D')"""
longer_ts = Series(np.random.randn(100),
                   index=pd.date_range('1/1/2000', periods=100))
print(longer_ts)
print(longer_ts['2000'])  # 能够得到范围内2000年的所有数据
print(longer_ts['2000-03'])  # 能够得到所有3月日期的数据

# ===分别传入datetime，字符串日期，Timestamp
print(ts[datetime(2011, 1, 1):])  # 用不存在于该时间序列的时间轴对其进行切片
print(ts['2011-01-06':])
print(ts['1/6/2011':'20110111'])

# ====对DataFrame同样适用
dates = pd.date_range(start='1/1/2000', periods=100, freq='W-WED')
long_df = DataFrame(np.random.randn(100, 4),
                    index=dates,
                    columns=['Colorado', 'Texas', 'New York', 'Ohio'])
print(long_df.ix['5-2001'])
"""
            Colorado     Texas  New York      Ohio
2001-05-02 -1.137907  1.064727 -1.271845  0.733882
2001-05-09  1.130685  1.015091 -0.017426  1.380220
2001-05-16  0.030939  0.069766  0.353213 -2.215995
2001-05-23  0.117024 -0.117483 -0.189213  1.107446
2001-05-30 -0.097159 -1.748038  0.162881 -0.767520
"""

