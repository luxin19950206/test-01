"""
def from_dict(data, orient='columns', dtype=None):
Construct DataFrame from dict of array-like or dicts ＃将array类型的dict或者多个dict转换为DataFrame

data : dict
    {field : array-like} or {field : dict}
orient : {'columns', 'index'}, default 'columns' ＃
    The "orientation" of the data. If the keys of the passed dict should be the columns of the resulting DataFrame,
    pass 'columns' (default). Otherwise if the keys should be rows, pass 'index'.
dtype : dtype, default None
    Data type to force, otherwise infer
"""

import pandas as pd

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
    '000004.sz': '国农科技'}

df = pd.DataFrame.from_dict(stock_code_dict, orient='index')
print(df)