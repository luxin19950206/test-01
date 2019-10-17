import pandas as pd
import tushare as ts
import talib as ta


sh = ts.get_hist_data('sh')
sh = sh.sort_index()
#print sh['close']
ma = ta.MA(sh['close'].values,20)
ma1 = pd.DataFrame(ma)
ma1.index = sh.index
#print ma1
sh['mma5'] = ma1



sh[['close','mma5']].plot(figsize = (15,8),grid = True)
