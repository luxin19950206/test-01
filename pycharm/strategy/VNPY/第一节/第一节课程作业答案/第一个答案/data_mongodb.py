# encoding: UTF-8
from datetime import datetime, timedelta
from Queue import Queue
from threading import Thread

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from data_read_tick import DemoTick

import sys

sys.path.append('..')
from vtFunction import loadMongoSetting
import re


class mongodb_client(object):
    def __init__(self):
        self.dbClient = None

    # ----------------------------------------------------------------------
    def writeLog(self, content):
        """日志"""
        print
        content

    # ----------------------------------------------------------------------
    def dbConnect(self):
        """连接MongoDB数据库"""
        if not self.dbClient:
            # 读取MongoDB的设置(vtFunction.py 里面的方法
            host, port, logging = loadMongoSetting()

            try:
                # 设置MongoDB操作的超时时间为0.5秒
                self.dbClient = MongoClient(host, port, serverSelectionTimeoutMS=500)

                # 调用server_info查询服务器状态，防止服务器异常并未连接成功
                self.dbClient.server_info()

                self.writeLog(u'MongoDB连接成功')
            except ConnectionFailure:
                self.writeLog(u'MongoDB连接失败')

    # ----------------------------------------------------------------------
    def dbInsert(self, dbName, collectionName, d):
        """向MongoDB中插入数据，d是具体数据"""
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            collection.insert(d)

    # ----------------------------------------------------------------------
    def dbQuery(self, dbName, collectionName, d):
        """从MongoDB中读取数据，d是查询要求，返回的是数据库查询的指针"""
        if self.dbClient:
            db = self.dbClient[dbName]
            collection = db[collectionName]
            cursor = collection.find(d)
            return cursor
        else:
            return None


class demo(object):
    def __init__(self):
        self.mc = None

    def log(self, content):
        """日志输出函数"""
        print
        content

    def import_days_ticks(self, main_path, start_date, end_date, symbol):
        """示例：导入一段日期的tick"""

        import_days = (end_date - start_date).days
        if import_days < 1:
            self.log(u'导入日期不足')
            return

        # 通过正则表达式获取symbol的短号
        p = re.compile(r"([A-Z]+)[0-9]+", re.I)
        short_symbol = p.match(symbol)
        if short_symbol is None:
            self.log(u'获取symbol的短号失败')
            return
        short_symbol = short_symbol.group(1)
        # 循环读取每天的数据，导入MongoDB
        for i in range(0, import_days):
            import_day = start_date + timedelta(days=i)
            self.log(u'导入日期:{0}'.format(import_day))

            # 加载运行白天数据
            file_name = '{0}\\{1}\{2}\\{3}\\{4}.txt'.format(main_path, import_day.strftime('%Y%m'),
                                                            short_symbol, import_day.strftime('%m%d'), symbol)

            self.import_tick(file_name, import_day.strftime('%Y%m%d'), symbol)

            # 加载运行夜盘数据
            file_name = '{0}_night\\{1}\{2}\\{3}\\{4}.txt'.format(main_path, import_day.strftime('%Y%m'),
                                                                  short_symbol, import_day.strftime('%m%d'), symbol)

            self.import_tick(file_name, import_day.strftime('%Y%m%d'), symbol)

    def import_tick(self, file_name, str_date, symbol):
        """读取某天的tick，写入mongodb"""
        d = DemoTick()
        ticks = d.load_tick_file(file_name, str_date, symbol)

        if len(ticks) == 0:
            self.log(u'没有读取tick成功')
            return

        self.log(u'读取tick共:{0}条'.format(len(ticks)))

        # 创建MongoDB链接库
        if self.mc is None:
            self.mc = mongodb_client()
            self.mc.dbConnect()

        count = 0
        # 逐一写入
        for tick in ticks:
            count = count + 1
            self.mc.dbInsert(dbName='Tick_Db', collectionName=tick.vtSymbol, d=tick.__dict__)

        self.log(u'写入完成，共{0}条'.format(count))


if __name__ == '__main__':
    d = demo()
    date1 = datetime.strptime('20141201', '%Y%m%d')
    date2 = datetime.strptime('20141205', '%Y%m%d')

    d.import_days_ticks('Z:\\ticks\\SHFE', start_date=date1, end_date=date2, symbol='RB1505')
