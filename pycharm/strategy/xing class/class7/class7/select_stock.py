# coding=utf-8
from __future__ import division
import pandas as pd
# import matplotlib.pyplot as plt
import xing_class.class7.config as cinfig
import xing_class.class7.class7.Functions as Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# ===读取所有股票代码的列表
# stock_code_list = Functions.get_stock_code_list_in_one_dir(config.input_data_path+'/stock')

stock_code_list = ['sz000002', 'sh600000']

# ===循环读取并且合并
# stock_data = pd.DataFrame()
for code in stock_code_list:
    print(code)


    # 读入数据
    # df = Functions.import_stock_data(code)
    # print(df)
    # exit()
#     # 导入上证指数
#     index_data = Functions.import_sh000001_data()
#
#     # 将股票和上证指数合并
#     df = Functions.merge_with_index_data(df, index_data)
#     # print df[df['交易日期'] > pd.to_datetime('20151201')]
#
#     # 将日线数据转化为月线
#     df = Functions.transfer_to_period_data(df, period_type='m')
#
#     # 计算下个月的涨跌幅
#     df['下月涨幅'] = df['涨跌幅'].shift(-1)
#
#     # 将导入数据合并到stock_data
#     stock_data = stock_data.append(df, ignore_index=True)
#
# # 将数据存储到hdf文件
# stock_data.to_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data', mode='w')


# # ===对合并的股票数据进行筛选
# # 从hdf文件中读取数据
# stock_data = pd.read_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data')
# stock_data.sort_values(['交易日期', '股票代码'], inplace=True)
#
# # 开始时间太早
# stock_data = stock_data[stock_data['交易日期'] > pd.to_datetime('20060101')]
# # 发现有下月涨幅为空的
# stock_data.dropna(subset=['下月涨幅'], inplace=True)
# # 万科在2015年12月18日停牌，2016年7月4日停牌。我在12月31日那一天是不能买入这个股票的。即最后一天不交易的股票，不能买入。
# # 并且像万科在12月，停牌时间过长，这样的股票也不能买入。得知道这个股票在本月的交易天数
# stock_data = stock_data[stock_data['是否交易'] == 1]
# stock_data = stock_data[stock_data['交易天数'] >= 10]
# # 在当天涨停的股票，也不能买入
# stock_data = stock_data[stock_data['涨跌幅'] <= 0.097]
# # 将数据存储到hdf文件
# stock_data.to_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data', mode='w')


# # ===选择单个条件选择股票
# output_df = pd.DataFrame()
# # 从hdf文件中读取数据
# stock_data = pd.read_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data')
# stock_data.sort_values(['交易日期', '收盘价'], inplace=True)
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
# print output_df
#
# # 画图
# plt.plot(output_df['capital_curve'])
# plt.plot(output_df['capital_curve_benchmark'])
# plt.legend(loc='best')
# plt.show()


# # ===根据多个条件选择股票
# output_df = pd.DataFrame()
# # 从hdf文件中读取数据
# stock_data = pd.read_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data')
# stock_data.sort_values(['交易日期', '收盘价'], inplace=True)
#
# # 计算所有股票在下个月的平均涨幅
# output_df['所有股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()
#
# # 计算市盈率
# stock_data = stock_data[stock_data['市盈率TTM'] > 0]
# stock_data['市盈率_排名'] = stock_data.groupby('交易日期')['市盈率TTM'].rank()
#
# # 计算市值排名
# stock_data['市值_排名'] = stock_data.groupby('交易日期')['总市值'].rank()
#
# # 将所有排名加总，得到总排名
# stock_data['排名加总'] = stock_data['市值_排名'] +  stock_data['市盈率_排名']
# stock_data['总排名'] = stock_data.groupby('交易日期')['排名加总'].rank()
#
# # 选取总排名前几名的股票
# stock_data = stock_data[stock_data['总排名'] <= 10]
#
# # 计算选中的股票在下周的涨幅
# stock_data['股票代码'] += ' '
# output_df['股票代码'] = stock_data.groupby('交易日期')['股票代码'].sum()
# output_df['选中股票下月涨幅'] = stock_data.groupby('交易日期')['下月涨幅'].mean()
# output_df['capital_curve'] = (output_df['选中股票下月涨幅'] + 1).cumprod()
# output_df['capital_curve_benchmark'] = (output_df['所有股票下月涨幅'] + 1).cumprod()
# print output_df

# # 画图
# plt.plot(output_df['capital_curve'])
# plt.plot(output_df['capital_curve_benchmark'])
# plt.legend(loc='best')
# plt.show()
