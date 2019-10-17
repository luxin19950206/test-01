# -*- coding: utf-8 -*-
import pandas as pd
# ===对print出的数据格式进行修正
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行，这里注意不是df，而是直接用pd就行
pd.set_option('max_colwidth', 3)  # 设定最大宽度，恢复原设置的方法

# =====数据导入
# ===导入股票数据
df = pd.read_csv('sz300001.csv', encoding='gbk', parse_dates=[2])  # 导入数据
# df.columns = [i.encode('utf8') for i in df.columns]  # 将columns从unicode改成str(python2需要）
df = df[['交易日期', '股票代码', '收盘价', '成交量', '涨跌幅']]  # 保留需要的列，其余的去除
df.sort_values(by=['交易日期'], inplace=True)  # 按照交易日期从小到大排序
start_date = df.iloc[0]['交易日期']  # 取数据开始的日期
end_date = df.iloc[-1]['交易日期']  # 取数据结束的日期

# ===导入指数数据
df_index = pd.read_csv('sh000001.csv', parse_dates=['date'])  # 导入指数数据
df_index = df_index[['date', 'change']]  # 保留需要的列，其余的去除
df_index.rename(columns={'date': '交易日期', 'change': '涨跌幅'}, inplace=True)  # 进行重命名
df_index.sort_values(by=['交易日期'], inplace=True)  # 按照交易日期从小到大排序
df_index = df_index[(df_index['交易日期'] >= start_date) &
                    (df_index['交易日期'] <= end_date)]  # 选取日期

# =====将指数数据和股票数据进行横向合并
# ===在excel中演示横向合并的含义
# ===使用merge函数
df = pd.merge(
    left=df,  # 两个表合并，放在左边的表
    right=df_index,  # 两个表合并，放在右边的表
    on=['交易日期'],  # 以哪个变量作为合并的主键，可以是多个
    how='outer',
    # left：只保留左表的主键，right：只保留右表的主键，
    # outer：两边的主键都保留，inner：两边都有的主键才保留
    # 此处使用outer和right都可以
    sort=True,  # 结果数据是否按照主键进行排序,如果没有这个排序，df会将有Nan的数据放置在最后
    suffixes=['_股票', '_指数'],  # 若两边有相同的列名，给这些列加上后缀
    indicator=True  # 增加_merge列，表明这一行数据来自哪个表，会显示数据来自于right、left还是both
)


# ===查看2016年3月14日停盘附件的数据
print(df[df['交易日期'] >= pd.to_datetime('20160310')])

# ===填补合并之后的缺失值
# 对于'股票代码', '收盘价'，应该如何填补？
df[['股票代码', '收盘价']] = df[['股票代码', '收盘价']].fillna(method='ffill')
# 对于'成交量', '涨跌幅_股票'，应该如何填补？
df[['成交量', '涨跌幅_股票']] = df[['成交量', '涨跌幅_股票']].fillna(0)
print(df[df['交易日期'] >= pd.to_datetime('20160310')])

# ===判断当天是否交易
df.loc[df[df['成交量'] > 0.1].index, '是否交易'] = 1
df['是否交易'].fillna(value=0, inplace=True)
print(df[df['交易日期'] >= pd.to_datetime('20160310')])

# =====输出
# df.to_csv('outout_sz300000.csv', index=False)
# del df['_merge']
# df.to_csv('outout_sz300000.csv', index=False)

