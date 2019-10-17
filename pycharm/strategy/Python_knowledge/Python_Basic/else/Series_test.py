# -*- coding: utf-8 -*-
"""
Series()
One-dimensional ndarray with axis labels (including time series).
Series是一种类似于一维数组的对象,其由一组数据以及一组与之相关的数据标签组成

Operations between Series (+, -, /, *, **) align values based on their associated index values-- they need not be the
same length. The result index will be the sorted union of the two indexes.

data : array-like, dict, or scalar value
    Contains data stored in Series
index : array-like or Index (1d)
    Values must be unique and hashable, same length as data. Index object (or other iterable of same length as data)
    Will default to RangeIndex(len(data)) if not provided. If both a dict and index sequence are used, the index will
    override the keys found in the dict.
dtype : numpy.dtype or None
    If None, dtype will be inferred
copy : boolean, default False
    Copy input data
"""

from pandas import Series

# example1
sf = Series([5, 4, 6, 7], index=['b', 'a', 'c', 'd'])  # 传入一个list或者一个一维numpy
print(sf)  # 数据类型为numpy.ndarray

# example2
stock_code_dict = {
    '600000.sh': '浦发银行',
    '600004.sh': '白云机场',
    '000005.sz': '世纪星源',
    '000006.sz': '深振业Ａ',
    '600005.sh': '武钢股份',
    '600006.sh': '东风汽车',
    '600007.sh': '中国国贸',
    '000001.sz': '平安银行',
    '000002.sz': '万科Ａ',
    '000004.sz': '国农科技', }
sf1 = Series(stock_code_dict)  # 传入一个dict，index即为keys并且自动排序
print(sf1)
