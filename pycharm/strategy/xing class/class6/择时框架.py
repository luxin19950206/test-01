# -*- coding: utf-8 -*-

import pandas as pd
import Functions
import Signals

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# ==读入数据
code = 'sz300001'
df = Functions.import_stock_data(code)
# 判断股票上市是否满一定时间，若不满足，则不运行策略，通过股票行数来
if df.shape[0] < 250:
    print('股票上市未满一年，不运行策略')
    exit()

# ==计算复权价
df = Functions.fuquan_price(df, '后复权')
del df['成交量']

# ==产生交易信号
df = Signals.signal_ma(df, ma_short=5, ma_long=10)
# print df[['交易日期', '股票代码', 'signal']]
# exit()

# ==根据交易信号计算每天的仓位
df = Functions.position(df)
# print df[['交易日期', '股票代码', 'signal', 'pos']]
# exit()

# ==截取上市一年之后的交易日
df = df.iloc[250 - 1:]
# 将第一天的仓位设置为0
df.iloc[0, -1] = 0
# print df[['交易日期', '股票代码', 'signal', 'pos']]
# exit()

# ==根据仓位计算资金曲线
# 资金曲线是一个策略最终的结果。是评价一个策略最重要的标准。

# 第五节课讲的简单计算方式
# print(Functions.equity_curve_simple(df))

# 稍复杂方式
df, zf = Functions.equity_curve(df)
# print(df)


# ===遍历dataframe的方式
# 遍历行
# for index, row in df.iterrows():
#     print(index)
#     print(row)
#     print(type(row))  # series
#     print(row['交易日期'])
#     exit()

# 遍历列
# for index, col in df.iteritems():
#     print(index)
#     print(col)
#     print(type(col))
#     exit()

# 我个人比较喜欢的遍历方式
# for index in df.index:
#     print(index)  # index
#     print(df.loc[index])  # 取一整行
#     print(df.at[index, '交易日期'])  # 取某个元素
#     df.at[index, '新增一列'] = 1  # 新增一列数据
#     print(df)
#     exit()

df.reset_index(inplace=True, drop=True)
for i in df.index:
    # 第一天不买入股票
    if i == 0:
        df.at[i, 'cash'] = 1000000
        df.at[i, 'stock_num'] = 0
        continue

    # 若今天的仓位和昨天的仓位一样
    if df.at[i, 'pos'] == df.at[i - 1, 'pos']:
        # cash资产部分不变
        df.at[i, 'cash'] = df.at[i - 1, 'cash']
        # 股票资产的变动幅度，和今天股票的涨跌幅一样
        df.at[i, 'stock'] = df.at[i - 1, 'stock'] * (df.at[i, '涨跌幅'] + 1)

        # 判断是否需要re balance?
        # 一般设置一个阈值

    # 若今天相比于昨天，增仓了（比如由空仓增加为20%仓位，比如由30%增加为60%，比如有20%增加为100%）。
    if df.at[i, 'pos'] > df.at[i - 1, 'pos']:
        # 目前的仓位是多少？
        # 增仓时能买多少股股票？
        pass

    # 若今天相比与昨天，减仓了（比如由满仓减为20%仓位，比如由满仓减少为0%，比如有60%较少为30%）。
    if df.at[i, 'pos'] < df.at[i - 1, 'pos']:
        pass
