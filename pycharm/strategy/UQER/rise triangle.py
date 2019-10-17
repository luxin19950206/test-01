# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""
"""
整理形态  一种暂时方向连续的状态，这是一种过渡形态，一旦完成主力目的（比如基本出货完毕），随之而来的就是转折。
上升三角形  在某价格水平呈现出相当强大的卖压，价格从低点回升到这水平便告回落.若把每一个短期波动高点连接起来，可划出一条水平阻力线。但市场的购买力十分良好，价格未回至上次低点即告弹升，此情形持续令价格承受着一条阻力水平线波动日渐收窄。每一个短期波动点则可相连出另一条向上倾斜的线，这就是“上升三角 形”。通常在“上升三角形”中，上升的部分成交较大，而下跌的部分成交则较少。
上升三角形形态市场含义  上升三角形显示买卖双方在该范围内的较量，但买方的力量稍占上风。卖方在其特定的价水平不断沽售虽不急于出货，但卖方不看好后市，于是价每升到理想的沽售水平，卖方便即沽出。这样在同一股价的沽售就形成了一条水平的供给线。不过，买方持续看好后市, 市场的购买力量加强，买方不待股价回落到上次的低点，更急不可待地购进，因此形成一条向右上方倾斜的需求线。这种上升趋势，反映出买方对后市认可度的不断增加。
另外，也可能是有计划的市场行为，不排除部分人有意把价暂时压低，以达到逢低大量吸纳之目的。

上升三角形判断方法
1.峰值、谷底计算
我们以某点为参考，与 包含本日、前后各两日共计5日的数据比较。
如果该日的最高值为5日最大值最大，则该日的最高值为峰值，local_high；如果该日的最低值为5日最低值最小，则该日的最低值为谷底,local_low。
2.水平阻力线
最近一个月的所有峰值的平均值称为该上升三角形的水平阻力线, mean(local_high)。
为了保证水平的稳定性，要求最近一个月所有峰值在一定范围，如最大峰值和最小峰值相差在10%以内.仅考虑后3个.
max(local_high)-min(local_high)< 0.15* max(local_high)
3.上升趋势线
该趋势线由所有的谷底链接而成。 为了保证上升, 要求local_low逐渐增大，即sorted(local_low)==local_low

突破判断
突破判断要求价格的突破，同时也需要成交量的增加，否则可能继续维持盘整。
1.价格突破 close_price > mean(local_high) × r1
2.成交量突破 volume > mean(volume[:-1]) × r2

买入择时
买入有两种方法，一种是突破即买入。第二种是突破后，价格回踩仍在阻力线上方.

止损止盈
1.一般方法
一般的止损方法是股价降低到cost的92 % 则止损卖出，升到120 % 止盈卖出。
2.改进方法A
动态的方法是，不断记录在未触及cost的92 % 和120 % 时的累计最大值，以此作为新的mod_cost，股价降低到mod_cost的90 % 则止损卖出，升到120 % 止盈卖出。
3.改进方法B
一般方法出现的问题是可能止盈太早，而改进方法1不排除某日的最高值未触及止损止盈点，但相较过往或以后的最大值有点偏离太大。此处我尝试建议用加权平均的方法；第一次的mod_cost即实际的cost。在后续的计算中使用下面的公式，

aux = max(mod_cost, high)
mod_cost += (aux - prev_mod_cost) × r3
r3取值在[0, 1]之间。很明显，r3 = 0即回到一般方法，r3 = 1则回到改进方法A。在计算中取r3 = 2 / 5.0

风险控制
始终把资产平均分给满足条件的合约。比如该合约上次占有全部资产，但第二天另一个合约满足条件，那么将上次买进的合约卖出一半，用来买进新的合约
"""
import pandas as pd
import numpy as np
from CAL.PyCAL import *
from matplotlib import pyplot as plt
import datetime

data_ = DataAPI.FutuGet(contractStatus="L", field=u"contractObject", pandas="1")
universe = [x + 'M0' for x in set(data_.contractObject)]
start = '2016-02-01'  # 回测开始时间
end = '2017-01-07'  # 回测结束时间
capital_base = 1e10  # 初试可用资金
refresh_rate = 2  # 调仓周期
freq = 'd'  # 调仓频率：m-> 分钟；d-> 日
commission = Commission(0.00005, 0.00005, 'perValue')
calendar = Calendar('China.SSE')


def initialize(futures_account):  # 初始化虚拟期货账户，一般用于设置计数器，回测辅助变量等。
    futures_account.mod_cost = {}
    futures_account.value = capital_base
    pass


def handle_data(futures_account):  # 回测调仓逻辑，每个调仓周期运行一次，可在此函数内实现信号生产，生成调仓指令。
    symbols = get_symbol(universe)
    prices = get_symbol_history(symbols, time_range=1)

    buy_long = []
    window = 30
    r = 0.15
    for symbol in symbols:
        data = pd.DataFrame(get_symbol_history(symbol, time_range=window + 3)[symbol]).replace(0, np.NAN)
        data = data.dropna(axis=0)  # 排除未交易日
        High = np.array(data['highPrice'])[-window:] ＃取30个数据
        Low = np.array(data['lowPrice'])[-window:]
        Close = np.array(data['closePrice'])[-window:]
        Volume = np.array(data['volume'])[-window:]
        if len(Volume) < window: continue
        local_high = []
        local_low = []
        index_low = []
        index_high = []
        for i in range(2, window - 2):  # 从2到28
        if High[i] >= max(High[i - 2:i + 3]):  # 近5个中最大的数值
            local_high.append(High[i])  # 将high值放入local_high中
            index_high.append(i)  # 将index放入index_high中
        if Low[i] <= min(Low[i - 2:i + 3]):
            local_low.append(Low[i])
            index_low.append(i)
    local_low = local_low[-3:]
    local_high = local_high[-3:]
    if len(local_high) <= 1 or len(local_low) <= 1 or sorted(local_low) != local_low:
        continue

    price = np.array(prices[symbol]['closePrice'])[-1]
    # 突破，1.价格突破 close_price > mean(local_high) × r1，成交量突破 volume > mean(volume[:-1]) × r2
    if (index_low[-1] > index_high[-1] and price >= 1.02 * np.mean(local_high)
        and max(local_high) - min(local_high) < r * min(local_high)
        and Volume[-1] > 1.2 * Volume[index_low[-1]:-1].mean()):
        buy_long.append(symbol)
    # 回踩
    elif (len(local_high) > 2 and index_low[-1] < index_high[-1]
          and max(local_high[:-1]) - min(local_high[:-1]) < r * min(local_high[:-1])
          and price > 1.02 * np.mean(local_high[:-1]) and local_high[-1] > 1.02 * np.mean(local_high[:-1])
          and Volume[index_high[-1]] > 1.2 * Volume[index_low[-1]:index_high[-1]].mean()):
        buy_long.append(symbol)


sell_list = []
for symbol in futures_account.position.keys():
    long_position = futures_account.position[symbol]['long_position']
    try:
        price = np.array(prices[symbol]['closePrice'])[-1]
    except:  # 这里实际是处理当合约更换时，平仓
        sell_list.append(symbol)
        order(symbol, -long_position, 'close')
        continue
    if ((price <= futures_account.mod_cost[symbol] * 0.92 or price >= futures_account.mod_cost[symbol] * 1.2)
        and symbol not in buy_long) or not (price > 0):
        sell_list.append(symbol)
        order(symbol, -long_position, 'close')

buy_long += list(set(futures_account.position.keys()).difference(set(sell_list)))
n = float(len(buy_long))
if n == 0: return

per_cash = futures_account.portfolio_value / n
for symbol in buy_long:
    coef = np.array(DataAPI.FutuGet(ticker=symbol, field=u"contMultNum", pandas="1").contMultNum)[-1]
    long_position = futures_account.position.get(symbol, dict()).get('long_position', 0)
    price = np.array(prices[symbol]['closePrice'])[-1]

    if long_position > 0:
        aux = max(futures_account.mod_cost[symbol], price)
        futures_account.mod_cost[symbol] += (aux - futures_account.mod_cost[symbol]) * 2 / 5.0
    else:
        futures_account.mod_cost[symbol] = price

    amount = int(per_cash / price / coef) - long_position
    if amount > 0:
        order(symbol, amount, 'open')
    elif amount < 0:
        order(symbol, amount, 'close')