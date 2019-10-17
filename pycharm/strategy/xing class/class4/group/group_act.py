# -*- coding: utf-8 -*-
"""
"""
import pandas as pd
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# ====导入数据
def import_stock_data(stock_code):
    """
    导入股票数据，股票数据必须与程序处于同一文件路径。
    只导入如下字段：'交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '成交量'
    最终输出结果按照日期排序
    :param stock_code:
    :return:
    """
    df = pd.read_csv(stock_code + '.csv', encoding='gbk')
    # df.columns = [i.encode('utf8') for i in df.columns]
    df = df[['交易日期', '股票代码', '开盘价', '最高价', '最低价', '收盘价', '涨跌幅', '成交量']]
    df.sort_values(by=['交易日期'], inplace=True)
    df['交易日期'] = pd.to_datetime(df['交易日期'])
    df.reset_index(inplace=True, drop=True)

    return df


# =====如何批量导入股票数据
# ===批量读取文件名称
stock_list = []
# 指定路径，若路径中包含中文，会出错，如果包含中文的话前面加u
data_path = '/Users/ShiRuo/PycharmProjects/untitled2/group'
# print(os.path.exists(data_path))

# 系统自带函数os.walk，用于遍历文件夹中的所有文件
for root, dirs, files in os.walk(data_path):
    # root输出文件夹，dirs输出root下所有的文件夹，files输出root下的所有的文件
    # print(root, dirs, files)
    if files:  # 当files不为空的时候
        for f in files:
            if f.endswith('.csv'):
                stock_list.append(f[:8])
                # stock_list.append(os.path.join(root, f))

# ===批量导入股票数据
stock_data = pd.DataFrame()
for code in stock_list:
    df = import_stock_data(code)
    stock_data = stock_data.append(df, ignore_index=True)
# 若一下子导入很多股票的时候，可能会内存溢出
print(stock_data)
# 作业：求每天3个股票中涨幅最大的股票，在下一天的涨幅，可以使用group操作很方便的完成。
# stock_data['第二天的涨跌幅']=stock_data['涨跌幅'].shift(-1)
# stock_data.sort_values(by=['交易日期', '涨跌幅'], inplace=True)
# stock_data.groupby('交易日期').tail()
# print(stock_data)

# =====groupby常用操作汇总
# # 根据'交易日期'进行group
# print(stock_data.groupby('交易日期'))  # 生成一个group对象
# # group后可以使用相关函数，size()计算每个group的行数
# print(stock_data.groupby('交易日期').size())
# # 根据'股票代码'进行group
# print(stock_data.groupby('股票代码').size())
# # 获取某一个group
# print(stock_data.groupby('股票代码').get_group('sz300433'))
# # 也可以同时用多个变量来进行group
# stock_data.groupby(['股票代码', '交易日期'])
#
# # 其他常见函数
# print(stock_data.groupby('股票代码').describe())
# print(stock_data.groupby('股票代码').head(3)) #开头三行
# print(stock_data.groupby('股票代码').tail(3))  # 每个group里面的行顺序，会保留。结尾三行
# print(stock_data.groupby('股票代码').first())
# print(stock_data.groupby('股票代码').last())
# print(stock_data.groupby('股票代码').nth(2))
# # 将group变量不设置为index
# print(stock_data.groupby('股票代码', as_index=False).nth(2))

# # 在group之后，取一部分变量进行计算
# # 计算每个group的均值
# print(stock_data.groupby('股票代码')['收盘价', '涨跌幅'].mean())
# # 计算每个group的最大值
# print(stock_data.groupby('股票代码')['收盘价', '涨跌幅'].max())
# # 计算每个group的加总
# print(stock_data.groupby('股票代码')['成交量'].sum())
# # 计算该数据在每个group中的排名，比如按照股票代码来，300424和300423就是两个group
# print(stock_data.groupby('股票代码')['成交量'].rank())
# print(stock_data.groupby('股票代码')['成交量'].rank(pct=True))

# # 如何根据年份进行group
# print(stock_data.groupby(stock_data['交易日期'].dt.year).size())
#
# # 我们之前讲过的resample、fillna、apply等常见操作，在group里面都可以进行。
# # 若直接在group上进行这些操作不熟练，可以使用已下的方式
#
# # 遍历group，对每个group进行单独操作，然后将这些group合并起来。
# # for key, group in df.groupby['']:
# for code, group in stock_data.groupby('股票代码'):
#     print(code)
#     print(group)
#     group.fillna()
#     group.apply()

# 作业：求每天3个股票中涨幅最大的股票，在下一天的涨幅，可以使用group操作很方便的完成。
