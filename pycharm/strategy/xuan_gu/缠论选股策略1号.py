# 思路:
# 股票选择仅限于次新股,利用macd的背驰概念进行30f和5f区间套的选股
# 所以第一步应该是把我想选择的相关的次新股选出来
# 第二部就是画出关于个股的分笔
# 第三部就是和把同样的相邻的下降趋势进行macd方面的比较

# 首先这里的次新股的选择应该在上市8月以内,同时流通市值小于50亿
import tushare as ts

df = ts.get_stock_basics()
d = ts.get_today_all()
for c in d['code']:
    date = df.ix[c]['timeToMarket']
    if 20160830 - date < 800:
        if d['nmc'][d.get_index(c)] < 500000:
            print(c,date)
