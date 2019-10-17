import pandas as pd
from pandas import DataFrame, Series

df = DataFrame({'a': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                'b': [2000, 2001, 2002, 2001, 2002],
                'c': [1.5, 1.7, 1.6, 2.4, 2.9]})

print(df['a'])  # 得到series
"""
0      Ohio
1      Ohio
2      Ohio
3    Nevada
4    Nevada
Name: a, dtype: object
"""
print(df[['a']])  # 得到新的dataframe
"""
        a
0    Ohio
1    Ohio
2    Ohio
3  Nevada
4  Nevada
"""
# DataFrame中的type输出相当于一整个df的格式
print(type(df['a']))  # <class 'pandas.core.series.Series'>
print(type(df[['a']]))  # <class 'pandas.core.frame.DataFrame'>

# DataFrame中的dtypes输出相当于每一个columns的格式
print(df['a'].dtypes)  # object
print(df[['a']].dtypes)
"""
a    object
dtype: object
"""
print(df['a'].dtype)  # object
# print(df[['a']].dtype)  #输出没有结果，因为dataframe不存在dtype
