# -*- coding:utf-8 -*-

import pandas as pd


# ===用于处理导入数据
def data_slice(stock, i):

    stock.columns = [j.encode('utf8') for j in stock.columns]
    stock = stock[['交易日期', '涨跌幅']]
    stock = stock[(stock['交易日期']>='2016-01-04') & (stock['交易日期']<='2016-01-29')]
    stock = stock.rename(columns={'涨跌幅': s[i]+p})
    return stock


# 导入数据，stock1 = sh600000, stock2 = sz000628, stock3 = sz300001
s = ['sh600000', 'sz000628', 'sz300001']
p = '_涨幅'
stock1 = pd.read_csv(s[0]+'.csv', encoding='gbk', parse_dates=[2])
stock2 = pd.read_csv(s[1]+'.csv', encoding='gbk', parse_dates=[2])
stock3 = pd.read_csv(s[2]+'.csv', encoding='gbk', parse_dates=[2])


stock1 = data_slice(stock1, 0)
stock2 = data_slice(stock2, 1)
stock3 = data_slice(stock3, 2)


# merge
for r in [stock2, stock3]:
    stock1 = stock1.merge(
        right=r,
        on=['交易日期'],
    )

# sort
stock1.sort_values(by='交易日期', inplace=True)
stock1['最大涨幅'] = stock1[[s[0]+p, s[1]+p, s[2]+p]].max(axis=1)

for i in stock1.index:
    for j in [0, 1, 2]:
        if stock1.loc[i, '最大涨幅'] == stock1.loc[i, s[j]+p]:
            stock1.loc[i, '当天涨幅最大的股票'] = s[j]
            if i-1 in stock1.index:
                stock1.loc[i, '当天涨幅最大的股票第二天的涨幅'] = stock1.loc[i-1, s[j]+p]


# print stock1
stock1.to_csv('XueTing_HW2_20161223.csv', encoding='gbk', index=False, mode='w')
