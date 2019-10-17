# encoding: UTF-8

import tushare as ts

# 股票数据
df = ts.get_hist_data('600000') #一次性获取全部日k线数据

print df.head(10)



