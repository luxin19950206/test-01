# -*- coding: utf-8 -*-
import pandas as pd

"""
@author:luxin

"""
# ====统一print后的格式
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行，这里注意不是df，而是直接用pd就行

# ====读取数据并对交易时间进行确定
out_put = pd.DataFrame()
codes = ['sz000628', 'sh600000', 'sz300001']
for code in codes:
    df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/' + code + '.csv',
                     encoding='gbk',
                     parse_dates=['交易日期'])
    df = df[['交易日期', '涨跌幅']]
    df.sort_values(by='交易日期', inplace=True)
    df.rename(columns={'交易日期': 'date', '涨跌幅': code + '_涨幅'}, inplace=True)
    # 确定相关的交易时间
    df = df[(df['date'].dt.year == 2016) & (df['date'].dt.month == 1)]
    # df['交易日期'].dt.year == 2016判断下来是一系列bool
    # 另外一种方式就是先确定startdate=pd.to_datetime('01/01/2016')和enddate=pd.to_datetime('02/0102016')

    if out_put.empty:
        out_put = df
    else:
        out_put = pd.merge(left=out_put, right=df, how='outer', on='date')

# ===获取最大涨跌幅
out_put['最大涨幅'] = out_put.max(axis=1)

# ===获取最大涨幅的股票相对应的股票代码
out_put.loc[out_put[out_put['sh600000_涨幅'] == out_put['最大涨幅']].index, '当天最大涨幅的股票'] = 'sh600000'
out_put.loc[out_put[out_put['sz000628_涨幅'] == out_put['最大涨幅']].index, '当天最大涨幅的股票'] = 'sz000628'
out_put.loc[out_put[out_put['sz300001_涨幅'] == out_put['最大涨幅']].index, '当天最大涨幅的股票'] = 'sz300001'

# ===获取相关股票第二天的涨幅
out_put.loc[out_put[out_put['当天最大涨幅的股票'] == 'sh600000'].index, '当天涨幅最大的股票第二天涨幅'] = out_put['sh600000_涨幅'].shift(-1)
out_put.loc[out_put[out_put['当天最大涨幅的股票'] == 'sz000628'].index, '当天涨幅最大的股票第二天涨幅'] = out_put['sz000628_涨幅'].shift(-1)
out_put.loc[out_put[out_put['当天最大涨幅的股票'] == 'sz300001'].index, '当天涨幅最大的股票第二天涨幅'] = out_put['sz300001_涨幅'].shift(-1)

# ===重排columns
columns = ['sh600000_涨幅', 'sz000628_涨幅', 'sh300001_涨幅', '当天最大涨幅的股票', '最大涨幅', '当天涨幅最大的股票第二天涨幅']
out_put = out_put.reindex(columns=columns)
print(out_put)
