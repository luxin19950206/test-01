# -*- coding: utf-8 -*-
"""
@author: xingbuxing
汇总常用函数
"""
import os
import pandas as pd  # 导入pandas，我们一般为pandas去一个别名叫做pd
import config


# 导入某文件夹下所有股票的代码
def get_stock_code_list_in_one_dir(path):

    stock_list = []

    # 系统自带函数os.walk，用于遍历文件夹中的所有文件
    for root, dirs, files in os.walk(path):
        if files:  # 当files不为空的时候
            for f in files:
                if f.endswith('.csv'):
                    stock_list.append(f[:8])

    return stock_list


# 导入数据
def import_stock_data(stock_code):
    """
    导入股票数据，股票数据必须与程序处于同一文件路径。
    只导入如下字段：'交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '成交量'
    最终输出结果按照日期排序
    :param stock_code:
    :return:
    """
    df = pd.read_csv(config.input_data_path + '/stock/' + stock_code[:2] + '/' + stock_code + '.csv', encoding='gbk')
    df.columns = [i.encode('utf8') for i in df.columns]
    df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '成交额', '总市值', '市盈率TTM']]
    df.sort_values(by=['交易日期'], inplace=True)
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df.reset_index(inplace=True, drop=True)

    return df


# 导入指数
def import_sh000001_data():
    # 导入指数数据
    df_index = pd.read_csv(config.input_data_path + '/index/' + 'sh000001.csv', parse_dates=['date'])
    df_index = df_index[['date', 'change']]
    df_index.rename(columns={'date': '交易日期', 'change': '大盘涨跌幅'}, inplace=True)
    df_index.sort_values(by=['交易日期'], inplace=True)
    df_index.dropna(subset=['大盘涨跌幅'], inplace=True)
    df_index.reset_index(inplace=True, drop=True)
    return df_index


# 和指数数据合并
def merge_with_index_data(df, index_data, fill_0_list=['成交额', '涨跌幅']):

    # 将股票数据和上证指数合并
    df = pd.merge(left=df, right=index_data, on='交易日期', how='right')

    # 将停盘时间的['成交量', '涨跌幅']数据填补为0
    df.loc[:, fill_0_list] = df[fill_0_list].fillna(value=0)

    # 将停盘时间的其他数据填补为最近交易日数据
    df.sort_values('交易日期', inplace=True)
    df.fillna(method='ffill', inplace=True)

    # 去除上市之前的数据
    df = df[df['股票代码'].notnull()]
    df.reset_index(drop=True, inplace=True)

    # 计算是否交易
    df['是否交易'] = 1
    df.loc[df[df['成交额'] <= 0.5].index, '是否交易'] = 0

    return df


# 转换数据周期
def transfer_to_period_data(df, period_type='m'):

    df['最后交易日'] = df['交易日期']

    # 将交易日期设置为index
    df.set_index('交易日期', inplace=True)

    # 转换为周期数据
    period_df = df.resample(rule=period_type).last()  # 大部分columns，在转换时使用last

    period_df['开盘价'] = df['开盘价'].resample(period_type).first()
    period_df['最高价'] = df['最高价'].resample(period_type).max()
    period_df['最低价'] = df['最低价'].resample(period_type).min()
    period_df['成交额'] = df['成交额'].resample(period_type).sum()
    period_df['涨跌幅'] = df['涨跌幅'].resample(period_type).apply(lambda x: (x + 1.0).prod() - 1.0)
    period_df['最后一天涨跌幅'] = df['涨跌幅'].resample(period_type).last()

    period_df['交易天数'] = df['是否交易'].resample(period_type).sum()

    # 去除一天都没有交易的周
    period_df.dropna(subset=['股票代码'], inplace=True)

    # 重新设定index
    period_df.reset_index(inplace=True)

    return period_df


# 计算复权价
def cal_fuquan_price(input_stock_data, fuquan_type='后复权'):
    # copy输入的数据
    df = input_stock_data.copy()

    # 判断输入数据中是否包含计算复权价格所需要的字段
    # col_list = df.columns
    # for i in ['开盘价', '最高价', '最低价', '收盘价', '涨跌幅', 'a']:
    #     if i not in col_list:
    #         raise '数据中不包含收盘价'

    # 计算复权收盘价
    num = {'后复权': 0, '前复权': -1}
    price1 = df['收盘价'].iloc[num[fuquan_type]]
    df['复权因子'] = (1.0 + df['涨跌幅']).cumprod()
    price2 = df['复权因子'].iloc[num[fuquan_type]]
    df['收盘价_' + fuquan_type] = df['复权因子'] * (price1 / price2)

    # 计算复权的开盘价、最高价、最低价
    df['开盘价_' + fuquan_type] = df['开盘价'] / df['收盘价'] * df['收盘价_' + fuquan_type]
    df['最高价_' + fuquan_type] = df['最高价'] / df['收盘价'] * df['收盘价_' + fuquan_type]
    df['最低价_' + fuquan_type] = df['最低价'] / df['收盘价'] * df['收盘价_' + fuquan_type]

    return df[[i + '_' + fuquan_type for i in '开盘价', '最高价', '最低价', '收盘价']]


# 根据交易信号，计算每天的仓位
def position(df):
    """
    根据交易信号，计算每天的仓位
    :param df:
    :return:
    """
    # =====由signal计算出实际的每天持有股票仓位
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)
    # print df[df['交易日期'] > pd.to_datetime('2015-05-01')]

    # ===将涨跌停时不得买卖股票考虑进来
    # 找出开盘涨停的日期
    cond_cannot_buy = df['开盘价'] > df['收盘价'].shift(1) * 1.097  # 今天的开盘价相对于昨天的收盘价上涨了9.7%
    # 将开盘涨停日、并且当天position为1时的'pos'设置为空值
    df.loc[cond_cannot_buy & (df['pos'] == 1), 'pos'] = None
    # print df[df['交易日期'] > pd.to_datetime('2015-05-01')]

    # 找出开盘跌停的日期
    cond_cannot_sell = df['开盘价'] < df['收盘价'].shift(1) * 0.903  # 今天的开盘价相对于昨天的收盘价下得了9.7%
    # 将开盘跌停日、并且当天position为0时的'pos'设置为空值
    df.loc[cond_cannot_sell & (df['pos'] == 0), 'pos'] = None

    # position为空的日期，不能买卖。position只能和前一个交易日保持一致。
    df['pos'].fillna(method='ffill', inplace=True)
    # print df[df['交易日期'] > pd.to_datetime('2015-05-01')]

    # 在position为空值的日期，将position补全为0
    df['pos'].fillna(value=0, inplace=True)

    return df


# 计算资金曲线，简单版本
def equity_curve_simple(df):
    """
    最简单的计算资金曲线的方式，与实际不符合
    :param df:
    :return:
    """
    # =====计算实际资金曲线
    df['equity_change'] = df['涨跌幅'] * df['pos']
    df['equity_curve'] = (df['equity_change'] + 1).cumprod()
    return df


# 计算资金曲线，稍复杂版本，考虑手续费和滑点
def equity_curve(df, s_rate=1.0 / 1000, c_rate=2.0 / 1000):
    """
    根据position函数计算出来的每天的实际仓位，计算得到每天的资金曲线
    在计算过程中，考虑买入和卖出时候的滑点以及手续费
    :param df:
    :param s_rate: 滑点比例，short for slippage_rate
    :param c_rate: 手续费和印花税比例，short for commission_rate
    :return:
    """

    df['equity_change'] = 0  # equity_change代表资产每天的涨跌幅，先设置为0

    # ===当天仓位和上一天相比没有变化时，当天的equity_change = 当天的股票的涨跌幅 * pos
    # 当当天空仓是，pos为0，资产涨幅为0
    # 当当天空仓是，pos为1，资产涨幅为股票本身的涨跌幅
    df.loc[df['pos'] == df['pos'].shift(1), 'equity_change'] = df['涨跌幅'] * df['pos']

    # ===当当天由满仓变成空仓时，当天equity_change = 今天开盘卖出的position在今天的涨幅(扣除手续费)
    # 前一天满仓，假设收盘后持有股票的市值为S。
    # 当天该股票的开盘价涨跌幅是：df['开盘价'] / df['收盘价'].shift(1) - 1，记为zf。
    # 当天该股票开盘时的市值为：S * (1 + zf)
    # 在开盘时全部平仓。当股票市值转变为现金的时候，因为滑点，市值不能等量变为现金，会损失一部分。
    # 市值变成现金的值为：S * (1 + zf) * (1 - s_rate)
    # 当市值变为现金后，有一部分要作为手续费或者印花税上交，这部分的比例为：S * (1 + zf) * (1 - s_rate) * c_rate
    # 市值变现后减去上交的税，得到当天最终剩余的现金为：[S * (1 + zf) * (1 - s_rate)] - [S * (1 + zf) * (1 - s_rate) * c_rate]
    # 整理后的得当天最终剩余的现金：S * (1 + zf) * (1 - s_rate) * (1 - c_rate)
    # 当天最终剩余的现金，相比于昨天持有股票的市值S，最终涨幅为：S * (1 + zf) * (1 - s_rate) * (1 - c_rate) / S - 1
    # 最终整理后得到当天最终涨幅为：(1 + zf) * (1 - s_rate) * (1 - c_rate) - 1
    # 遂有下式
    df.loc[df['pos'] < df['pos'].shift(1), 'equity_change'] = \
        (1 + df['开盘价'] / df['收盘价'].shift(1) - 1) * (1 - s_rate) * (1 - c_rate) - 1

    # ===当当天由空仓变成满仓时，当天equity_change = 今天开盘新买入的position在今天的涨幅(并且要扣除买入手续费和滑点)
    # 前一天空仓，假设收盘后持有的现金量为C。
    # 在当天以开盘价全仓买入。假设准备用于买入股票的现金量为Cb。Cb会比C小，因为要预留一部分交手续费。
    # 在买入股票时，因为滑点，最终买到的股票的市值是：Cb * (1 - s_rate)
    # 在买入股票时，需要付出的手续费是：Cb * (1 - s_rate) * c_rate
    # 存在等式Cb + Cb * (1 - s_rate) * c_rate = C，整理得到：Cb = C / [1 + (1 - s_rate) * c_rate]
    # 当天结束时，股票的市值在当天的涨幅是：df['收盘价'] / df['开盘价'] - 1，记为zf。
    # 当天结束时，股票的市值变为Cb * (1 - s_rate) * （1 + zf）
    # 当天结束时，股票的市值相比于昨天的现金C，最终涨幅是：Cb * (1 - s_rate) * （1 + zf）/ C - 1
    # 将Cb带入上式，整理后得到最终涨幅是：((1 + zf - c_rate) - (1 / (1 - s_rate))) / ((1 / (1 - s_rate)) + c_rate)
    # 遂有下式
    df.loc[df['pos'] > df['pos'].shift(1), 'equity_change'] = \
        ((1 + df['收盘价'] / df['开盘价'] - 1 - c_rate) - (1 / (1 - s_rate))) / ((1 / (1 - s_rate)) + c_rate)

    df['equity_curve'] = (df['equity_change'] + 1).cumprod()

    return df, df.iloc[-1]['equity_curve'] - 1
