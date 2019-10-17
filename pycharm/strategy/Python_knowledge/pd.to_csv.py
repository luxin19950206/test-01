# -*- coding: utf-8 -*-
from pandas import DataFrame, Series
import tushare as ts

'''
pd.to_csv(path, index=True, sep=",", na_rep='', float_format=None,header=False, index_label=None, mode='w',
nanRep=None,encoding=None, date_format=None, decimal='.'):
Write Series to a comma-separated values (csv) file

path : string file path or file handle / StringIO. If None is provided the result is returned as a string.
na_rep : string, default ''
        Missing data representation
float_format : string, default None
        Format string for floating point numbers
        控制浮点数的精确度
        float_format='%.15f'，这个代表着所有数字都是15位小数
header : boolean, default False
        Write out series name
        如果header＝none的话，输出到csv文件不会输出原有文件的表头
index : boolean, default True
        当为True的时候就写入index，当为False就不写入index
        Write row names (index)
index_label : string or sequence, default None
        Column label for index column(s) if desired. If None is given, and
        `header` and `index` are True, then the index names are used. A
        sequence should be given if the DataFrame uses MultiIndex.
mode : Python write mode, default 'w'
        默认为w，意味是覆盖原有的文件
        mode=a时，代表着接在了原来数据的末尾
sep : character, default ","
        Field delimiter for the output file.
encoding : string, optional 编码方式，默认utf8，有些csv文件需要将编码方式设置为encoding='gbk'
        a string representing the encoding to use if the contents are
        non-ascii, for python versions prior to 3
date_format: string, default None
        Format string for datetime objects.
decimal: string, default '.'
        Character recognized as decimal separator. E.g. use ',' for
        European data
'''

# 方法1
# 首先创建一个csv文件，然后将相关的文件导入到csv文件中
open('stocks basics.csv', 'w')
df = ts.get_stock_basics()
df.to_csv('stocks basics.csv')

# 方法2
# 直接将csv文件进csv文件
df = ts.get_stock_basics()
df.to_csv('stocks basics.csv')

