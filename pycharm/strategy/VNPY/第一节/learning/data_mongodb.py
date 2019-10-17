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
            host, port = loadMongoSetting()

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
    def log(self, content):
        """日志输出函数"""
        print
        content

    def import_tick(self):
        d = DemoTick()
        ticks = d.load_tick_file('Z:\\ticks\\SHFE\\201408\RB\\0804\\RB1501.txt', '20140804', 'RB1501')

        if len(ticks) == 0:
            self.log(u'没有读取tick成功')
            return

        self.log(u'读取tick共:{0}条'.format(len(ticks)))

        mc = mongodb_client()

        mc.dbConnect()

        count = 0
        # 逐一写入
        for tick in ticks:
            count = count + 1
            mc.dbInsert(dbName='Tick_Db', collectionName=tick.vtSymbol, d=tick.__dict__)

        self.log(u'写入完成，共{0}条'.format(count))


if __name__ == '__main__':
    d = demo()

    d.import_tick()
