# encoding: UTF-8

# 载入相关模块
import os                       # 操作系统模块
import csv                      # csv格式文件模块
from datetime import datetime   # 时间模块，这里只加载其中一个子模块，其他不加载，节省内存

import sys
sys.path.append('..')
from ctaAlgo.ctaBase import CtaTickData

class DemoTick(object):

    def log(self,content):
        """日志输出函数"""
        print content

    def load_tick_file(self, file_name, tick_date, tick_symbol):
        """
        读取tick文件
        返回ctatick对象列表，无内容返回[]
        """
        if not os.path.isfile(file_name):
            self.log(u'{0}文件不存在'.format(file_name))
            return []

        # 初始化队列对象
        ticks = []
        last_tick_datetime = None

        # 文件句柄
        csv_read_file = file(file_name, 'rb')

        # 通过csv模块的DictReader，一次性读取所有数据
        reader = csv.DictReader(csv_read_file, delimiter=",")
        self.log(u'加载{0}'.format(file_name))

        # 逐行数据处理
        for row in reader:
            tick = CtaTickData()
            # vtSymbol：CF1705， symbol：CF1705
            tick.vtSymbol = tick_symbol
            tick.symbol = tick_symbol

            # 日期格式为 '20170120',交易日期，在夜盘时，交易日期为下一交易日
            tick.date = tick_date
            tick.time = row['Time']
            tick.tradingDay = tick.date

            # 转换为datetime格式
            try:
                tick.datetime = datetime.strptime(tick.date + ' ' + tick.time, '%Y%m%d %H:%M:%S.%f')
            except Exception as ex:
                # 抛弃本tick
                self.log(u'日期转换错误:{0},{1}:{2}'.format(tick.date + ' ' + tick.time, Exception, ex))
                continue

            # 修正毫秒
            if tick.datetime.replace(microsecond=0) == last_tick_datetime:
                # 与上一个tick的时间（去除毫秒后）相同,修改为500毫秒
                tick.datetime = tick.datetime.replace(microsecond=500)
                tick.time = tick.datetime.strftime('%H:%M:%S.%f')

            else:
                tick.datetime = tick.datetime.replace(microsecond=0)
                tick.time = tick.datetime.strftime('%H:%M:%S.%f')

            # 记录最新tick的时间
            last_tick_datetime = tick.datetime

            tick.lastPrice = float(row['LastPrice'])             # 最新价
            tick.volume = int(float(row['LVolume']))             # 成交量
            tick.bidPrice1 = float(row['BidPrice'])              # 叫买价（价格低）
            tick.bidVolume1 = int(float(row['BidVolume']))       # 叫买量
            tick.askPrice1 = float(row['AskPrice'])              # 叫卖价（价格高）
            tick.askVolume1 = int(float(row['AskVolume']))       # 叫卖量

            tick.openInterest = int(float(row['OpenInterest']))  # 持仓量
            tick.dayVolume = int(float(row['TradeVolume']))      # 当日累计成交量

            # 排除涨停/跌停的数据 （这里在套利中使用！）
            if (tick.bidPrice1 == float('1.79769E308') and tick.bidVolume1 == 0) \
                    or (tick.askPrice1 == float('1.79769E308') and tick.askVolume1 == 0):
                continue

            ticks.append(tick)

        return ticks

if __name__ == '__main__':
    d = DemoTick()
    ticks = d.load_tick_file('Z:\\ticks\\SHFE\\201408\RB\\0801\\RB1501.txt', '20140801', 'RB1501')

    print u'一共加载:{0}条数据'.format(len(ticks))