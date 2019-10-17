# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""

import pandas as pd

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
out_put.groupby()