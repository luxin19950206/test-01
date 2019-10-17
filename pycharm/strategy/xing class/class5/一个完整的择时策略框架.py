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

# =====计算复权价
fuquan_type = '后复权'
df= Functions.fuquan_price(df, fuquan_type)

# =====计算均线策略
# ===计算均线
ma_short = 10
ma_long = 30
df['ma_short'] = df['收盘价'].rolling(ma_short).mean()
df['ma_long'] = df['收盘价'].rolling(ma_long).mean()

# 将缺失的均线数据补全
df['ma_short'].fillna(value=df['收盘价'].expanding().mean(), inplace=True)
df['ma_long'].fillna(value=df['收盘价'].expanding().mean(), inplace=True)
# 补全数据的另外一种方式是使用rolling函数中的min_periods参数
# df['ma_short'] = df['收盘价'].rolling(ma_short, min_periods=1).mean()
# df['ma_long'] = df['收盘价'].rolling(ma_long, min_periods=1).mean()

# ===找出买入信号，金叉
# 当天的短期均线大于等于长期均线
condition1 = (df['ma_short'] >= df['ma_long'])
# 上个交易日的短期均线小于长期均线
condition2 = (df['ma_short'].shift(1) < df['ma_long'].shift(1))
# 将买入信号当天的signal设置为1
df.loc[condition1 & condition2, 'signal'] = 1

# ===找出卖出信号，死叉
# 当天的短期均线小于等于长期均线
condition1 = (df['ma_short'] <= df['ma_long'])
# 上个交易日的短期均线大于长期均线
condition2 = (df['ma_short'].shift(1) > df['ma_long'].shift(1))
# 将买入信号当天的signal设置为0
df.loc[condition1 & condition2, 'signal'] = 0

# 将无关的变量删除
df.drop(['ma_short', 'ma_long'], axis=1, inplace=True)

# =====由signal计算出实际的每天持有股票仓位
# ===计算仓位（理想中的仓位），满仓用1表示，空仓用0表示
# signal的计算运用了收盘价，是每天收盘之后产生的信号
df['pos'] = df['signal'].shift(1)

df['pos'].fillna(method='ffill', inplace=True)
print(df)
# 这就是实际的仓位了吗？有没有什么问题？
# 涨跌停的时候是不得买卖股票的。很多人策略表现好，可能就是没有考虑这些限制。
# 这类策略和实际操作不吻合的问题，是经常犯的问题。
# 有的问题隐藏的很深，很多时候只有到了实盘交易的时候才会发现

# ===将涨跌停时不得买卖股票考虑进来
# 找出开盘涨停的日期，例如有些股票复牌后直接涨停，这个时候是买不进去股票的
cond_cannot_buy = df['开盘价'] > df['收盘价'].shift(1) * 1.097  # 今天的开盘价相对于昨天的收盘价上涨了9.7%
# 将开盘涨停日、并且当天position为1时的'pos'设置为空值
df.loc[cond_cannot_buy & (df['pos'] == 1), 'pos'] = None
# print(df[df['交易日期'] > pd.to_datetime('20150125')])

# 找出开盘跌停的日期
cond_cannot_sell = df['开盘价'] < df['收盘价'].shift(1) * 0.903  # 今天的开盘价相对于昨天的收盘价下得了9.7%
# 将开盘跌停日、并且当天position为0时的'pos'设置为空值
df.loc[cond_cannot_sell & (df['pos'] == 0), 'pos'] = None
print(df[cond_cannot_sell])
# position为空的日期，不能买卖。position只能和前一个交易日保持一致。
df['pos'].fillna(method='ffill', inplace=True)

# =====计算实际资金曲线
df['equity_rtn'] = df['pos'] * df['涨跌幅']  # 资金每日涨跌幅
df['equity_curve'] = (df['equity_rtn'] + 1).cumprod()