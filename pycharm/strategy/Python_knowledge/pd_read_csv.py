# -*- coding: utf-8 -*-
import pandas as pd

'''
pd.read_csv()

filepath_or_buffer:
    ＃表示文件系统位置、URl、文件型对象的字符串
sep:默认','
    ＃该参数代表数据的分隔符，csv文件默认是逗号。其他常见的是'\t'
skiprows : list-like or integer, default None
    Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file
    ＃跳过数据文件的的第1行，skiprows＝1
nrows : int, default None
    Number of rows of file to read. Useful for reading pieces of large files
    ＃读取多少行的数据，例如nrows＝20，即为读取20前20行的数据
parse_dates:boolean or list of ints or names or list of lists or dict, default False
    ＃尝试将指定的列解析为日期格式，default=False，如果为True，则尝试解析所有列，此外还可以制定解析一组列号或列名
index_col : int or sequence or False, default None
    Column to use as the row labels of the DataFrame. If a sequence is given, a MultiIndex is used.
    If you have a malformed file with delimiters at the end of each line, you might consider index_col=False to force
    pandas to _not_ use the first column as the index (row names)
    ＃将指定列设置为index。若不指定，index默认为0, 1, 2, 3, 4...
    eg：index_col=['交易日期']
usecols : array-like, default None
    ＃读取指定的这几列数据，若不知定，默认读取全部列
    eg：usecols=['交易日期', '股票代码', '股票名称', '收盘价', '涨跌幅', '成交量']
'''

df = pd.read_csv('/Users/hengzong/Documents/Python_knowledge/code.csv')
print(df)
i = df.loc[:, ['code', 'name']]
# print(i)
