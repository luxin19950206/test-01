"""
DataFrame.empty
    True if NDFrame is entirely empty [no items], meaning any of the axes are of length 0.

"""
from pandas import DataFrame, Series

df = DataFrame()
print(df.empty)
"""True"""
df = DataFrame({'A': [None]})
print(df.empty)
"""False"""
print(df.dropna().empty)
"""True"""
