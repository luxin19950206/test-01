# -*- coding: utf-8 -*-
"""
@author：日行小逻辑19950206
@usage：PYTHON FOR FINANCE

"""
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2019, 2, 1)
data = pdr.get_data_yahoo(['AAPL', 'F'], start, end)
price_F = data['Adj Close']['F']
price_AAPL = data['Adj Close']['AAPL']
new_data = pd.DataFrame()

new_data['Log_price_AAPL'] = np.log(price_F) / np.log(price_F).shift(1)
new_data['Log_price_F'] = np.log(price_AAPL) / np.log(price_AAPL).shift(1)
new_data['Volatility'] = new_data['Log_price_AAPL'].rolling(252).std()*np.sqrt(252)

new_data[['Log_price_AAPL','Volatility']].plot(subplots=True,color='blue',figsize=(8,6))

