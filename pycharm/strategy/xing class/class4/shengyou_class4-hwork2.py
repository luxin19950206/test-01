# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

start_date = pd.Timestamp('2016-01-01')
end_date = pd.Timestamp('2016-01-31')


def getdataframe(code):
    df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/' + code + '.csv', encoding='gbk',
                     parse_dates=[2])  # 导入数据
    # df.columns = [i.encode('utf8') for i in df.columns]  # 将columns从unicode改成str
    df = df[['交易日期', '涨跌幅']]  # 保留需要的列，其余的去除
    df.rename(columns={'涨跌幅': code + '_涨幅'}, inplace=True)
    df.sort_values(by=['交易日期'], inplace=True)  # 按照交易日期从小到大排序
    df = df[(df['交易日期'] >= start_date) & (df['交易日期'] <= end_date)]  # 选取日期
    return df


def get_value(x):
    if True:
        return x


d01 = getdataframe('sh600000')
d03 = getdataframe('sz300001')
d02 = getdataframe('sz000628')
df = pd.merge(
    left=d01,  # 两个表合并，放在左边的表
    right=d02,  # 两个表合并，放在右边的表
    on=['交易日期'],  # 以哪个变量作为合并的主键，可以是多个
    how='outer',
    sort=True,  # 结果数据是否按照主键进行排序
)
df = pd.merge(
    left=df,  # 两个表合并，放在左边的表
    right=d03,  # 两个表合并，放在右边的表
    on=['交易日期'],  # 以哪个变量作为合并的主键，可以是多个
    how='outer',
    sort=True,  # 结果数据是否按照主键进行排序
)
df.set_index('交易日期', inplace=True)
max_values = df.max(axis=1)  # 计算当日最大涨幅
df2 = df.isin(max_values)
# print max_values   ##########################################
df2.iloc[:, 0] = df2.replace(True, df.columns[0][:8])
df2.iloc[:, 1] = df2.replace(True, df.columns[1][:8])
df2.iloc[:, 2] = df2.replace(True, df.columns[2][:8])
max_stocks = df2.iloc[:, 0].replace(False, df2.iloc[:, 1]).replace(False, df2.iloc[:, 2])
# print max_stocks   ##########################################
df3 = df.isin(max_values).shift(1).replace(False, np.nan)*df
second_day = df3.iloc[:, 0].replace(np.nan, df3.iloc[:, 1]).replace(np.nan, df3.iloc[:, 2]).shift(-1)
# print second_day
df['当天涨幅最大的股票'] = max_stocks
df['最大涨幅'] = max_values
df['当天涨幅最大的股票第二天的涨幅'] = second_day
