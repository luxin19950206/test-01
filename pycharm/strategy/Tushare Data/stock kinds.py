import talib
import numpy as np
import pandas as pd
import tushare as ts

# 行业分类
open('stocks industry.csv','w')
df=ts.get_industry_classified()
df.to_csv('stocks industry.csv')

# 概念分类
open('stocks concept.csv','w')
df=ts.get_concept_classified()
df.to_csv('stocks concept.csv')

# 地域分类
open('stocks area.csv','w')
df=ts.get_area_classified()
df.to_csv('stocks area.csv')

# 中小板分类
open('stocks zxb.csv','w')
df=ts.get_sme_classified()
df.to_csv('stocks zxb.csv')

# 创业板分类
open('stocks cyb.csv','w')
df=ts.get_gem_classified()
df.to_csv('stocks cyb.csv')

# 风险警示板
open('stocks st.csv','w')
df=ts.get_st_classified()
df.to_csv('stocks st.csv')

# # h沪深300成份及权重
# open('stocks hs300.csv','w')
# df=ts.get_hs300s()
# df.to_csv('stocks hs300.csv')

# # 上证50成份股
# open('stocks sz50.csv','w')
# df=ts.get_sz50s()
# df.to_csv('stocks sz50.csv')
#
# # 中证500成分股
# open('stocks zz500.csv','w')
# df=ts.get_zz500s()
# df.to_csv('stocks zz500.csv')