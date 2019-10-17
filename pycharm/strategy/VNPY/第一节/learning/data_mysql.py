# encoding: UTF-8
import MySQLdb
import json
import os

class DemoMysql(object):

    mysql_connection = None
    mysql_connected = False

    history_ticks = None

    def log(self,content):
        """日志输出函数"""
        print content

    def connect_mysql(self):
        """连接MysqlDB"""

        # 载入json文件
        fileName = 'mysql_connect.json'
        try:
            f = file(fileName)
        except IOError:
            self.log(u'读取Mysql_connect.json失败')
            return

        # 解析json文件
        setting = json.load(f)
        try:
            mysql_host = str(setting['host'])
            mysql_port = int(setting['port'])
            mysql_user = str(setting['user'])
            mysql_passwd = str(setting['passwd'])
            mysql_db = str(setting['db'])

        except IOError:
            self.log(u'读取Mysql_connect.json,连接配置缺少字段，请检查')
            return

        try:
            self.mysql_connection = MySQLdb.connect(host=mysql_host, user=mysql_user,
                                                    passwd=mysql_passwd, db=mysql_db, port=mysql_port)
            self.mysql_connected = True
            self.log(u'连接MysqlDB成功')
        except Exception as e:
            self.log('连接Mysql异常{0}'.format(e))
    def qry_data_history_tick(self, symbol, startDate, endDate):
        """从Mysql载入历史TICK数据
            startDate 开始日期
            endDate 结束日期
        """

        try:
            self.connect_mysql()
            if self.mysql_connected:

                # 获取指针
                cur = self.mysql_connection.cursor(MySQLdb.cursors.DictCursor)

                if endDate:

                    # 开始日期 ~ 结束日期
                    sqlstring = ' select \'{0}\' as InstrumentID, str_to_date(concat(ndate,\' \', ntime),' \
                               '\'%Y-%m-%d %H:%i:%s\') as UpdateTime,price as LastPrice,vol as Volume, day_vol as DayVolume,' \
                               'position_vol as OpenInterest,bid1_price as BidPrice1,bid1_vol as BidVolume1, ' \
                               'sell1_price as AskPrice1, sell1_vol as AskVolume1 from TB_{0}MI ' \
                               'where ndate between cast(\'{1}\' as date) and cast(\'{2}\' as date) order by UpdateTime'.\
                               format(symbol,  startDate, endDate)

                elif startDate:

                    # 开始日期 - 当前
                    sqlstring = ' select \'{0}\' as InstrumentID,str_to_date(concat(ndate,\' \', ntime),' \
                               '\'%Y-%m-%d %H:%i:%s\') as UpdateTime,price as LastPrice,vol as Volume, day_vol as DayVolume,' \
                               'position_vol as OpenInterest,bid1_price as BidPrice1,bid1_vol as BidVolume1, ' \
                               'sell1_price as AskPrice1, sell1_vol as AskVolume1 from TB__{0}MI ' \
                               'where ndate > cast(\'{1}\' as date) order by UpdateTime'.\
                               format( symbol, startDate)

                else:

                    # 所有数据
                    sqlstring =' select \'{0}\' as InstrumentID,str_to_date(concat(ndate,\' \', ntime),' \
                              '\'%Y-%m-%d %H:%i:%s\') as UpdateTime,price as LastPrice,vol as Volume, day_vol as DayVolume,' \
                              'position_vol as OpenInterest,bid1_price as BidPrice1,bid1_vol as BidVolume1, ' \
                              'sell1_price as AskPrice1, sell1_vol as AskVolume1 from TB__{0}MI order by UpdateTime'.\
                              format(symbol)

                    self.log(sqlstring)

                # 执行查询
                count = cur.execute(sqlstring)
                self.log(u'历史TICK数据共{0}条'.format(count))


                # 分批次读取
                fetch_counts = 0
                fetch_size = 1000

                while True:
                    results = cur.fetchmany(fetch_size)

                    if not results:
                        break

                    fetch_counts = fetch_counts + len(results)

                    if not self.history_ticks:
                        self.history_ticks =results

                    else:
                        self.history_ticks = self.history_ticks + results

                    self.log(u'{1}~{2}历史TICK数据载入共{0}条'.format(fetch_counts,startDate,endDate))

            else:
                self.log(u'MysqlDB未连接，请检查')

        except MySQLdb.Error as e:
            self.log(u'MysqlDB载入数据失败，请检查.Error {0}'.format(e))

if __name__ == '__main__':

    demo = DemoMysql()
    demo.qry_data_history_tick('rb', startDate='2015-01-01', endDate='2015-01-10')

    print len(demo.history_ticks)
