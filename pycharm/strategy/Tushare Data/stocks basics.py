import tushare as ts
# 实时数据
# ts.get_stock_basics 获取相关股票的基本面数据 index为code
# name,industry,area,pe市盈率,outstanding流通股本(亿股),totals总股本(亿股),totalAssets总资产(万)
# liquidAssets流动资产(万),fixedAssets固定资产(万),reserved公积金(万),reservedPerShare每股公积金,esp每股收益,bvps每股净资产,pb市净率
# timeToMarket上市日期,undp未分配利润,perundp每股未分配,rev收入同比％,profit利润同比％,gpr毛利率％,npr净利润率％
# holders股东人数

open('stocks basics.csv','w')
df = ts.get_stock_basics()
df.to_csv('stocks basics.csv')