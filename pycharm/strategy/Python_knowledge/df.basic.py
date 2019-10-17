# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：做一些dataframe中简单常用的操作
"""
import pandas as pd

df = pd.read_csv('/Users/ShiRuo/PycharmProjects/untitled2/Python_knowledge/sh000001.csv',
                 encoding='gbk')
print(df.shape)  # 取到的数据分别为行和列
"""
(6359, 9)
"""
print(df.shape[0])  # 取行的数据
"""
6359
"""
print(df.columns)  # 得到所有的行名称
"""
Index(['index_code', 'date', 'open', 'close', 'low', 'high', 'volume', 'money',
       'change'],
      dtype='object')
"""
print(df.index)  # 输出每一列的名字
"""
RangeIndex(start=0, stop=6359, step=1)
"""
print(df.dtypes)  # 输出每一列变量类型，其中的object代表的是字符串格式
"""
index_code     object
date           object
open          float64
close         float64
low           float64
high          float64
volume        float64
money         float64
change        float64
dtype: object
"""
print(df.size)  # 元素的总数 即行数*列数
"""
57231
"""
print(df.head(3))  # 输出前三行的数据
"""
  index_code        date     open    close      low     high        volume
0   sh000001  2016-12-16  3111.51  3122.98  3106.35  3128.87  1.649887e+10
1   sh000001  2016-12-15  3125.76  3117.68  3100.91  3138.78  1.899906e+10
2   sh000001  2016-12-14  3149.38  3140.53  3136.35  3170.02  2.013589e+10
"""
print(df.tail(3))  # 输出最后三行的数据
"""
     index_code        date    open   close     low    high     volume
6356   sh000001  1990-12-21  109.07  109.13  103.73  109.13    28000.0
6357   sh000001  1990-12-20  104.30  104.39   99.98  104.39   197000.0
6358   sh000001  1990-12-19   96.05   99.98   95.79   99.98  1260000.0
"""
print(df.sample(3))  # 随机抽取三行数据
"""
     index_code        date    open   close     low    high       volume
5012   sh000001  1996-04-18  592.81  600.28  589.80  600.28  165678900.0
5687   sh000001  1993-08-06  841.39  855.52  841.39  860.73  524069000.0
5688   sh000001  1993-08-05  853.71  849.30  842.72  863.94  538329000.0
"""

