# -*- coding: utf-8 -*-
"""
@author: xingbuxing
"""
import os
import pandas as pd  # 导入pandas，我们一般为pandas去一个别名叫做pd
import config
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# # ===选择单个条件选择股票
# output_df = pd.DataFrame()
# # 从hdf文件中读取数据
# stock_data = pd.read_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data')
# stock_data.sort_values(['交易日期', '总市值'], inplace=True)
#
# # 计算所有股票在下个月的平均涨幅
# output_df['所有股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()
#
# # 计算市值排名
# stock_data['市值_排名'] = stock_data.groupby('交易日期')['总市值'].rank()
#
# # 选取前三的股票
# stock_data = stock_data[stock_data['市值_排名'] <= 10]
#
# # 计算选中的股票在下周的涨幅
# stock_data['股票代码'] += ' '
# output_df['股票代码'] = stock_data.groupby('交易日期')['股票代码'].sum()
# output_df['选中股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()
# output_df['capital_curve'] = (output_df['选中股票下月涨幅'] + 1).cumprod()
# output_df['capital_curve_benchmark'] = (output_df['所有股票下月涨幅'] + 1).cumprod()
#
# output_df.to_hdf(config.output_data_path + '/市值选股结果.h5', 'df', mode='w')

df = pd.read_hdf(config.output_data_path + '/市值选股结果.h5', 'df')
df.reset_index(inplace=True)
print df
# ===对资金曲线，收益的评价
# 总收益
total_return = (df.iloc[-1]['capital_curve'] / 1) - 1
print '总收益（%）：', round(total_return * 100, 2)

# 年华收益
# 年华收益：pow((1 + x), 年数) = 总收益
# 日化收益：pow((1 + x), 天数) = 总收益
# ((1 + 日化收益), 365) = 年华收益
# 整理得到：年华收益 = pow(总收益, 365/天数)
trading_days = (df['交易日期'].iloc[-1] -  df['交易日期'].iloc[0]).days + 1
annual_return = pow(total_return, 365.0/trading_days) - 1
print '年华收益（%）：', round(annual_return * 100, 2)

# ===对资金曲线，风险的评价
# 方差
print df['所有股票下月涨幅'].std()

# 最大回撤
# 计算当日之前的最大资产净值
# df['max2here'] = pd.expanding(df['capital_curve']).max()
df['max2here'] = df['capital_curve'].expanding().max()
# 计算到历史最高值到当日的跌幅
df['dd2here'] = df['capital_curve'] / df['max2here'] - 1
# 计算最大回撤，以及最大回撤结束时间
end_date, max_draw_down = tuple(df.sort_values(by=['dd2here']).iloc[0][['交易日期', 'dd2here']])
print '最大回撤（%）：', round(max_draw_down * 100, 2)
# 计算最大回撤开始时间
start_date = df[df['交易日期'] <= end_date].sort_values(by='capital_curve', ascending=False).iloc[0]['交易日期']
print '最大回撤开始时间', start_date.date()
print '最大回撤结束时间', end_date.date()

# 如何计算最大上涨呢？

# ===终极指标
# 如果只用一个指标来衡量策略，我最常用的就是：年化收益 / abs(最大回撤)
# 一般这个指标大于1，说明可行。

# ==对每次操作的评价
# 平均涨幅
print '平均涨幅（%）', round(df['选中股票下月涨幅'].mean() * 100, 2)

# 胜率
print '涨幅>0比例（%）', df[df['选中股票下月涨幅'] > 0].shape[0] / float(df.shape[0]) * 100

# 胜率
print '跑赢同期均值比例（%）', df[df['选中股票下月涨幅'] > df['所有股票下月涨幅']].shape[0] / float(df.shape[0]) * 100

# 最大单月涨幅，最大单月跌幅
print '最大单月涨幅（%）：', round(df['选中股票下月涨幅'].max() * 100, 2)
print '最大单月跌幅（%）：', round(df['选中股票下月涨幅'].min() * 100, 2)

# 最大连续上涨，最大连续下跌
df.loc[df['选中股票下月涨幅'] > 0, 'up_or_down'] = 1
df.loc[df['选中股票下月涨幅'] < 0, 'up_or_down'] = -1
df['up_or_down'].fillna(method='ffill', inplace=True)
df['up_or_down_sum'] = df['up_or_down'].expanding().sum()
# 对df['up_or_down_sum']计算最大上涨、最大回撤，上涨的值就是最大连续





