# -*- coding: utf-8 -*-
"""
@author: Xing
"""
import pandas as pd
import Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====读入数据
code = 'sz300001'
df = Functions.import_stock_data(code)

# =====以日线数据转化为周线数据为例，具体说明的案例
# ===将'交易日期'这一列设置为index，之后讲为什么需要这么做
df.set_index('交易日期', inplace=True)


# ===周期转换方法：resample
# ===周线上导出来的数据通常是以星期天为最后一天
week_df = df.resample(rule='w').last()
# 'w'意思是week，意味着转变为周线；
# last意思是取最后一个值
# print(week_df)
# print(df.iloc[:7])

week_df['开盘价'] = df['开盘价'].resample('w').first()
week_df['最高价'] = df['最高价'].resample('w').max()
week_df['最低价'] = df['最低价'].resample('w').min()
week_df['成交量'] = df['成交量'].resample('w').sum()
week_df['涨跌幅'] = df['涨跌幅'].resample('w').apply(lambda x: (x + 1.0).prod() - 1.0)

# 去除一天都没有交易的周
week_df.dropna(how='all', inplace=True)

# week_df的index并不是这一周最后一个交易日，而是这一周星期天的日期。
# 如何才能保留这周最后一个交易日的日期？
# 在将'交易日期'set_index之前，先增加df['最后交易日'] = df['交易日期']，然后在resample的时候取'最后交易日'的last就是最后一个交易日
# 这个操作可以自己尝试完成

# 为什么在一开始时候需要set_index？
# 因为进行resample操作的前提：以时间变量作为index
# 在0.19版本的pandas开始，resample函数新增on参数，可以不在事先set_index。具体可见：http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.resample.html
# 如何查看自己的pandas版本？
# print pd.__version__  # 或者去pycharm中查看

# rule='w'代表转化为周
# 'm'代表月，'q'代表季度，'y'代表年份，'5min'代表5分钟，等等

# 非常人性化的ohlc函数，直接得到open、high、low、close价格
print(df['收盘价'].resample(rule='w').ohlc())