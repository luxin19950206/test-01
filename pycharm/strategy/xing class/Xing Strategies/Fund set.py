# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt


def automatic_investment_plan(index_code, start_date, end_date):
    """
    :param index_code: 需要定投的指数代码
    :param start_date: 开始定投的日期
    :param end_date: 结束定投的日期
    :return: 返回从定投到现在每天的资金和累计投入的资金
    """
    # 读取指数数据，此处为csv文件的本地地址，请自行修改
    index_data = pd.read_csv('/stock data/' + str(index_code) + '.csv',
                             parse_dates=['date'], index_col=['date'])
    index_data = index_data[['index_code', 'close']].sort_index()
    index_data = index_data[start_date:end_date]
    index_data['无风险利率'] = (4.0 / 100 + 1) ** (1.0 / 250) - 1  # 假设年化无风险利率是4%(余额宝等理财产品),计算无风险日利率
    index_data['无风险收益_净值'] = (index_data['无风险利率'] + 1).cumprod()

    # 每月第一个交易日定投
    by_month = index_data.resample('M', how='first', kind='period')

    # 定投购买指数基金
    trade_log = pd.DataFrame(index=by_month.index)
    trade_log['基金净值'] = by_month['close'] / 1000  # 以指数当天收盘点位除以1000作为单位基金净值
    trade_log['money'] = 1000  # 每月月初投入1000元申购该指数基金
    trade_log['基金份额'] = trade_log['money'] / trade_log['基金净值']  # 当月的申购份额
    trade_log['总基金份额'] = trade_log['基金份额'].cumsum()  # 累积申购份额
    trade_log['累计定投资金'] = trade_log['money'].cumsum()  # 累积投入的资金
    # 定投购买余额宝等无风险产品
    trade_log['理财份额'] = trade_log['money'] / by_month['无风险收益_净值']  # 当月的申购份额
    trade_log['总理财份额'] = trade_log['理财份额'].cumsum()  # 累积申购份额

    temp = trade_log.resample('D', fill_method='ffill')
    index_data = index_data.to_period('D')

    # 计算每个交易日的资产（等于当天的基金份额乘以单位基金净值）
    daily_data = pd.concat([index_data, temp[['总基金份额', '总理财份额', '累计定投资金']]], axis=1, join='inner')
    daily_data['基金定投资金曲线'] = daily_data['close'] / 1000 * daily_data['总基金份额']
    daily_data['理财定投资金曲线'] = daily_data['无风险收益_净值'] * daily_data['总理财份额']

    return daily_data


# 运行程序
df = automatic_investment_plan('sh000001', '2007-10-01', '2009-07-31')
print(df[['累计定投资金', '基金定投资金曲线', '理财定投资金曲线']].iloc[[0, -1],])
print(temp = (df['基金定投资金曲线'] / df['理财定投资金曲线'] - 1).sort_values())
print("最差时基金定投相比于理财定投亏损: %.2f%%，日期为%s" % (temp.iloc[0] * 100, str(temp.index[0])))
print("最好时基金定投相比于理财定投盈利: %.2f%%，日期为%s" % (temp.iloc[-1] * 100, str(temp.index[-1])))

df[['基金定投资金曲线', '理财定投资金曲线']].plot(figsize=(12, 6))
df['close'].plot(secondary_y=True)
plt.legend(['close'], loc='best')
plt.show()
