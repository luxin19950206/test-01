# -*- coding: utf-8 -*-
import pandas as pd
import Functions

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====读入数据
code = 'sz300001'
df = Functions.import_stock_data(code)

# =====计算复权价
fuquan_type = '后复权'
df = Functions.fuquan_price(df, fuquan_type)


# ===计算均线择时策略
def signal_ma(date, ma_short=10, ma_long=30):
    """
    :param date: 一个股票的dataframe
    :param ma_short:
    :param ma_long:
    :return:
    """
    df = date.copy()
    df['ma_short'] = df['收盘价'].rolling(ma_short).mean()
    df['ma_long'] = df['收盘价'].rolling(ma_long).mean()
    df['ma_short'].fillna(value=df['收盘价'].expanding().mean(), inplace=True)
    df['ma_long'].fillna(value=df['收盘价'].expanding().mean(), inplace=True)
    condition1 = (df['ma_short'] >= df['ma_long'])
    condition2 = (df['ma_short'].shift(1) < df['ma_long'].shift(1))
    df.loc[condition1 & condition2, 'signal'] = 1
    condition1 = (df['ma_short'] <= df['ma_long'])
    condition2 = (df['ma_short'].shift(1) > df['ma_long'].shift(1))
    df.loc[condition1 & condition2, 'signal'] = 0
    df.drop(['ma_short', 'ma_long'], axis=1, inplace=True)

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
    # df['pos'].fillna(method='ffill', inplace=True)
    return df


# =====计算实际资金曲线
def equity_curve(date):
    df = date.copy()
    df['equity_rtn'] = df['pos'] * df['涨跌幅']  # 资金每日涨跌幅
    df['equity_curve'] = (df['equity_rtn'] + 1).cumprod()
    return df


print(signal_ma(df))
