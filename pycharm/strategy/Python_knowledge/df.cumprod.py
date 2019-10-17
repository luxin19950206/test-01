from pandas import DataFrame, Series

'''
numpy.cumpord(a, axis=None, dtype=None, out=None) 累计乘积
return the cumulative product of elements along a given axis
'''

sf = {'change': [0.01, 0.02, -0.02, 0.03, 0.05, -0.01, 0, -0.1, 0.01, 0],
      '目前的仓位': [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
      'close': [10, 11, 10.5, 11.1, 10.3, 9.8, 9.7, 10.05, 11, 10.6]}
df = DataFrame(sf)
df['资金指数'] = (df['change'].values * df['目前的仓位'].values + 1.0).cumprod()
print(df)
initial_idx = df.iloc[0]['close'] / (1 + df.iloc[0]['change'])
df['资金指数'] *= initial_idx
print(df)