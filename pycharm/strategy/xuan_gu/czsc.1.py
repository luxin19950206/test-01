# -*- coding: utf-8 -*-
import pandas as pd

def bhgx(k_data):  # 包含关系
    merge_data=pd.DataFrame()
    high = k_data['high']
    low = k_data['low']
    for i in xrange(len(k_data)):  # 提取序列
        if high[i + 1] <= high[i] and low[i + 1] >= low[i]:  # 后一根K线被前一根K线包含
            if high[i] > high[i-1] and low[i] > low[i-1]:  # 向上
                merge_data.high[i]=high[i]
                merge_data.low[i]=low[i + 1]  # 取高高点
            if high[i] < high[i-1] and low[i] < low[i-1]:  # 向下
                high1.append(high[i + 1])
                low1.append(low[i + 1])  # 取低低点
        elif high[i + 1] > high[i] and low[i + 1] < low[i]:  # 前一根K线被后一根K线包含
            if high[i] > high[i-1] and low[i] > low[i-1]:  # 向上
                high1.append(high[i + 2])
                low1.append(low[i + 1])  # 取高高点
            if high[i] < high[i-1] and low[i] < low[i-1]:  # 向下
                high1.append(high[i + 1])
                low1.append(low[i + 2])  # 取低低点
        else:
            high1.append(high[i])
            low1.append(low[i])

def ddfx(k_data):  # 确定顶底分型
    high1 = []
    low1 = []
    high = m['high']
    low = m['low']
    for i in range(1, len(m) - 2):  # 提取序列
        if high[i + 1] > high[i] and high[i + 1] > high[i + 2]:  # 确定顶分型的顶
            high1.append(high[i + 1])  # 顶
        if low[i + 1] < low[i] and low[i + 1] < low[i + 2]:  # 确定底分型的底
            low1.append(low[i + 1])  # 底
    return high1, low1


# 接下来就是连接顶底使之能够成为一笔
# 相关特点:1相邻的顶连接相邻的底; 2包含后的顶底之间要有5跟K线; 3做向下笔的比较,要保证后一根的高点比前一根的高点低,后一根的低点比前一跟的低点低;

if __name__ == '__main__':
    k_data = pd.read_csv('/Users/hengzong/Documents/pycharm/strategy/Tushare Data/000001/000001_30_Mins.csv')
    print(m)
    # xuangu()
    bhgx(m)
    # ddfx(m)
