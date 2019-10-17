# encoding: UTF-8
from WindPy import w
from datetime import *
import pandas as pd

# 启动接口
w.start()

#定义获取的字段（可通过代码生成器生成）
fields = "open,high,low,close,volume,amt"

# 提取分钟数据
data = w.wsi("RB1710.SHF", fields, beginTime='2017-3-17 09:00:00', endTime='2017-3-17 15:00:00')

print data

#演示如何将api返回的数据装入Pandas的DataFrame
df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Times)
df = df.T #将矩阵转置
print(':/n', df)
