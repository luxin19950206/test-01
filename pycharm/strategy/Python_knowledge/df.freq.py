"""
时间序列的基础频率
D: Day 每日历日
B: BusinessDay 每工作日
H: hour 每小时
T or min: Minute 每分钟
S: 每秒
L or ms: milli 每毫秒（即每千分之一秒）
U: 每微妙（即百万分之一秒）
M: MonthEnd 每月最后一个日历日
BM: BusinessMonthEnd 每月最后一个工作日
MS: MonthBegin 每月第一个日历日
BMS: BusinessMonthBegin 每月第一个工作日
W-MON\W-TUE: Week 从指定的星期几开始算起，每周
WOM-1MON,WOM-2MON: WeekOfMonth 产生每月第一、第二、第三、第四周的星期几，例如，WOM-3FRI表示每月第3个星期五
详细见利用python进行数据分析
"""