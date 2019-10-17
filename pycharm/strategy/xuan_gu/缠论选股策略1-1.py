# -*- coding: utf-8 -*-
# 思路:
# 股票选择仅限于次新股,利用macd的背驰概念进行30f和5f区间套的选股
# 所以第一步应该是把我想选择的相关的次新股选出来
# 第二部就是画出关于个股的分笔
# 第三部就是和把同样的相邻的下降趋势进行macd方面的比较

# 首先这里的次新股的选择应该在上市8月以内,同时流通市值小于50亿
import tushare as ts

# 这一步就是简单的筛选股票,这里筛选的是次新股,以后还会放入龙头股
df = ts.get_stock_basics()
d = ts.get_today_all()
for c in d['code']:
    date = df.ix[c]['timeToMarket']
    if 20160830 - date < 800:
        aa = 0
        m = ts.get_hist_data(c, ktype='30', start='2016-08-01', end='2016-08-02')  # 获取30分钟k线数据
        for b in m['open']:
            if open != 0:
                aa = aa + 1
        if aa > 6:
            print(c, m.loc[:, ['high', 'low']])


            # 这一步首先要确定分型区间——从而确定包含关系——再确定顶分型和底分型
            # 包含关系:1k线排序——2确定有包含关系——3确定方向——4包含处理


            # 这一步就是开始确定分笔关系



            # 这一步开始设定MACD
