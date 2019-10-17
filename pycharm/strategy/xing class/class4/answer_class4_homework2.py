# -*- coding: utf-8 -*-
"""
@author: Xing
"""
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行，这里注意不是df，而是直接用pd就行

code_list = ['sh600000', 'sz000628', 'sz300001']

output_merge = pd.DataFrame()
for code in ['sh600000', 'sz000628', 'sz300001']:
    # 导入数据
    df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/' + code + '.csv', encoding='gbk',
                     parse_dates=[2])
    # df.columns = [i.encode('utf8') for i in df.columns] python2中需要，python3中无需
    df = df[['交易日期', '涨跌幅']]
    df = df[(df['交易日期'].dt.year == 2016) & (df['交易日期'].dt.month == 1)]
    df.sort_values('交易日期', inplace=True)
    df.rename(columns={'涨跌幅': code + '_涨幅'}, inplace=True)

    # 获取关于每只个股的涨跌幅和交易日期
    # merge
    if output_merge.empty:
        output_merge = df
    else:
        output_merge = pd.merge(output_merge, df, on='交易日期', how='outer', sort=True)

output_append = pd.DataFrame()
for code in ['sh600000', 'sz000628', 'sz300001']:
    # 导入数据
    df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/' + code + '.csv', encoding='gbk',
                     parse_dates=[2])
    # df.columns = [i.encode('utf8') for i in df.columns] python2中需要，python3中无需
    df = df[['股票代码', '交易日期', '涨跌幅']]
    df = df[(df['交易日期'].dt.year == 2016) & (df['交易日期'].dt.month == 1)]
    df.sort_values('交易日期', inplace=True)
    df['第二天涨跌幅'] = df['涨跌幅'].shift(-1)

    # append
    if output_append.empty:
        output_append = df
    else:
        output_append = output_append.append(df, ignore_index=True)  # 对三个df进行纵向拼接

output_append.sort_values(by=['交易日期', '涨跌幅'], ascending=[1, 0], inplace=True)
output_append.drop_duplicates('交易日期', keep='first', inplace=True)
output_append.rename(columns={'股票代码': "当天涨幅最大的股票", '涨跌幅': '最大涨幅', "第二天涨跌幅": '当天涨幅最大的股票第二天的涨幅'}, inplace=True)

output = pd.merge(output_merge, output_append, on='交易日期', how='outer', sort=True)
print(output)

output.to_csv('output.csv', encoding='gbk', index=False)