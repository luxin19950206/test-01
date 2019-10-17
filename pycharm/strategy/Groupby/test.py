import numpy as np
from pandas import DataFrame, Series

df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                'key2': ['one', 'two', 'one', 'two', 'one'],
                'data1': np.random.randn(5),
                'data2': np.random.randn(5)})
print(df)
# price=df.groupby('key1').mean()
# price1=df.groupby('key1')['data1'].mean()
# price2=df.groupby('key1')[['data1','data2']].mean()
# price3=df.groupby(['key1','key2'])['data1'].mean()
# price4=df.groupby(['key1','key2'])[['data1','data2']].mean()
# print(price)
# print('-----')
# print(price2)
# print('-----')
# print(price3)
# print('-----')
# print(price4)

# grouped=df.groupby(df.dtypes,axis=1)
# print(list(grouped))

grouped = df.groupby('key1')


def peak_to_peak(arr):
    return arr.max() - arr.min()


print(grouped.agg(peak_to_peak))
