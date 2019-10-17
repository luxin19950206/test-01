# encoding: UTF-8

# 在python3下运行
import rqdatac
from rqdatac import *
rqdatac.init('Dajia','------')

# 获取螺纹钢的指数数据，15分钟周期
df = get_price('RB99', start_date='2009-01-01', end_date='2017-03-12', frequency='15m')
# 导出到文件
df.to_csv('RB99_20090101_20170312_M15.csv')

