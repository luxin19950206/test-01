# coding=utf-8
import pandas as pd
import config
import numpy as np
import Functions as Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 构造现在持有的股票
holding_stock = pd.DataFrame()
holding_stock.loc[0, '股票代码'] = 'sh600000'
holding_stock.loc[0, '股票数量'] = 1000
holding_stock.loc[1, '股票代码'] = 'sz000002'
holding_stock.loc[1, '股票数量'] = 1000
holding_stock.loc[2, '股票代码'] = 'sz000001'
holding_stock.loc[2, '股票数量'] = 1000

cash = 100000

# 需要买入的股票
to_buy_stocks = pd.DataFrame()
to_buy_stocks.loc[0, '股票代码'] =  'sh600000'
to_buy_stocks.loc[0, '股票仓位'] =  0.3
to_buy_stocks.loc[1, '股票代码'] =  'sz300001'
to_buy_stocks.loc[1, '股票仓位'] =  0.4
to_buy_stocks.loc[2, '股票代码'] =  'sh601006'
to_buy_stocks.loc[2, '股票仓位'] =  0.3

# 获取持有股票最新的价格
df = Functions.get_latest_stock_price_from_sina(list(holding_stock['股票代码']))
# 将股票价格和股票数量合并
df = pd.merge(df, holding_stock, on='股票代码', how='inner')
# 计算股票市值
stock_value = (df['股票数量'] * df['卖一价']).sum()
# 计算总资产
equity = stock_value + cash

# 输出要卖出的股票
stock_to_sell = df[['股票代码', '股票数量']]
stock_to_sell['股票数量'] *= -1


# 获取要买入的股票最新的价格
df = Functions.get_latest_stock_price_from_sina(list(to_buy_stocks['股票代码']))
# 将过价格和仓位合并
df = pd.merge(df, to_buy_stocks, on='股票代码', how='inner')

# 计算用于买入每个股票的资金
df['theory_buy_money'] = equity * df['股票仓位']
# 计算买入每个股票的股数
df['theory_buy_num'] = df['theory_buy_money'] / df['买一价']
# 计算实际买入该股票的股数
df['actual_buy_num'] = df['theory_buy_num'].apply(lambda x: int(x/100)*100)
# 计算实际买入该股票的资金
df['actual_buy_money'] = df['actual_buy_num'] * df['买一价']
# 计算实际每个股票的仓位
df['actual_pos'] = df['actual_buy_money'] / equity
df['股票数量'] = df['actual_buy_num']

# 输出要买的股票数据
stock_to_buy = df[['股票代码', '股票数量']]

# 计算最终需要买卖的股票
stock = stock_to_buy.append(stock_to_sell, ignore_index=True)
stock = stock.groupby('股票代码').sum().reset_index()

# 计算最终需要买卖的股票的价格
df = Functions.get_latest_stock_price_from_sina(list(stock['股票代码']))
stock = pd.merge(stock, df, on='股票代码', how='inner')
