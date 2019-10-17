# -*- coding: utf-8 -*-
"""
@author：luxin
@usage：
"""
import pandas as pd
import Functions

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# ====导入数据
# 导入的数据包括'交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '成交量'
df1 = Functions.import_stock_data('sh600004')
df2 = Functions.import_stock_data('sz000656')

df1 = Functions.fuquan_price(df1, '后复权')
df2 = Functions.fuquan_price(df2, '后复权')


def signal_chaikinAD(date, short_period=9, long_period=13):
    df = date.copy()
    offset = (df['收盘价'] - df['最低价']) - (df['最高价'] - df['收盘价'])  # 偏移量
    zhenfu = df['最高价'] - df['最低价']
    df['ad' + str(short_period)] = offset / zhenfu * df['成交量'].rolling(short_period, min_periods=1).sum()
    df['ad' + str(long_period)] = offset / zhenfu * df['成交量'].rolling(long_period, min_periods=1).sum()
    df['chaikin'] = df['ad' + str(short_period)] - df['ad' + str(long_period)]
    df.loc[df['chaikin'] > 0, 'signal'] = 1
    df.loc[df['chaikin'] <= 0, 'signal'] = 0
    df.drop(['ad9', 'ad13'], axis=1, inplace=True)
    return df


# ====由signal计算出实际的每天的持有的股票仓位
def position(date):
    # ===计算仓位（理想中的仓位），满仓用1表示，空仓用0表示
    # signal的计算运用了收盘价，是每天收盘之后产生的信号
    df = date.copy()
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)

    # ===将涨跌停时不得买卖股票考虑进来
    cond_cannot_buy = df['开盘价'] > df['收盘价'].shift(1) * 1.097
    # 将开盘涨停日、并且当天position为1时的'pos'设置为空值
    df.loc[cond_cannot_buy & (df['pos'] == 1), 'pos'] = None

    # 找出开盘跌停的日期
    cond_cannot_sell = df['开盘价'] < df['收盘价'].shift(1) * 0.903
    df.loc[cond_cannot_sell & (df['pos'] == 0), 'pos'] = None

    # position为空的日期，不能买卖。position只能和前一个交易日保持一致。
    df['pos'].fillna(method='ffill', inplace=True)
    return df


# =====计算实际资金曲线
def equity_curve(date):
    df = date.copy()
    df['equity_rtn'] = df['pos'] * df['涨跌幅']  # 资金每日涨跌幅
    df['equity_curve'] = (df['equity_rtn'] + 1).cumprod()
    return df


if __name__ == '__main__':
    df1 = signal_chaikinAD(df1)
    df1 = position(df1)
    print(equity_curve(df1))
    df2 = signal_chaikinAD(df2)
    df2 = position(df2)
    print(equity_curve(df2))
