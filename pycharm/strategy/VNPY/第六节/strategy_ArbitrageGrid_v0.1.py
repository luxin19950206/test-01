# encoding: UTF-8

# 首先写系统内置模块
import sys
from datetime import datetime, timedelta, date
from time import sleep

# 然后是自己编写的模块
from ctaTemplate import *
from ctaBase import CtaBarData,CtaTickData
from vtConstant import  EMPTY_STRING, EMPTY_INT, DIRECTION_LONG, DIRECTION_SHORT, OFFSET_OPEN, STATUS_CANCELLED
from ctaPolicy import *
from ctaLineBar import *
from ctaPosition import *
from ctaGridTrade import *

import requests
import execjs


######################################from##################################
class Strategy_ArbitrageGrid(CtaTemplate):
    """套利+网格交易
    跨期合约价差套利（豆粕跨期）
    置信区间（+100以上,-100以下做多)
    采用5分钟布林特线
    置信区间内(>100)，超过Boll上轨，网格做空价差合约
    置信区间内(<-100)，低于Boll下轨，网格做多价差合约
    风控
    网格和开仓数量，根据资金比例和承受力计算
    近月合约结束前一个月开始，不再开仓，只平仓
    近月合约结束前一周，强制平仓


    """
    className = 'Strategy_ArbitrageGrid'
    author = u'李来佳'

    # 策略在外部设置的参数
    inputSS = 1                # 参数SS，下单，范围是1~100，步长为1，默认=1，
    minDiff = 1                # 商品的最小交易单位
    maxPos = 10                # 最大仓位（网格）数量

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting=None):
        """Constructor"""
        super(Strategy_ArbitrageGrid, self).__init__(ctaEngine, setting)

        self.paramList.append('inputSS')
        self.paramList.append('symbol')        # 标准合约
        self.paramList.append('D1Symbol')       # 近期合约
        self.paramList.append('D2Symbol')       # 远期合约
        self.paramList.append('minDiff')
        self.paramList.append('shortSymbol')
        self.paramList.append('maxPos')
        self.paramList.append('maxLots')
        self.paramList.append('height')
        self.paramList.append('win')
        self.paramList.append('baseUpLine')
        self.paramList.append('baseMidLine')    # 基准中轴
        self.paramList.append('baseDnLine')
        self.paramList.append('deadLine')       # 最后开仓期限，超过设置期限就不再开仓
        self.paramList.append('fixedGrid')

        self.varList.append('pos')
        self.varList.append('entrust')
        self.varList.append('grids')
        self.varList.append('tradingOpen')

        self.curDateTime = None                 # 当前Tick时间
        self.curTick = None                     # 最新的tick


        # 交易窗口
        self.tradeWindow = False
        # 开市窗口
        self.openWindow = False
        # 收市平仓窗口
        self.closeWindow = False

        # 仓位状态
        self.position = CtaPosition(self)       # 0 表示没有仓位，1 表示持有多头，-1 表示持有空头

        self.position.maxPos = self.maxPos

        self.lastTradedTime = datetime.now()    # 上一交易时间
        self.deadLine = EMPTY_STRING            # 允许最后的开仓期限（参数，字符串）
        self.deadLineDate = None                # 允许最后的开仓期限（日期类型）
        self.tradingOpen = True                 # 允许开仓

        # 是否完成了策略初始化
        self.inited = False

        self.backtesting = False

        # 初始化时读取的历史数据的起始日期(可以选择外部设置)
        self.startDate = None
        self.policy = CtaPolicy()               # 成交后的执行策略

        self.resubmitOrders = True              # 重新提交平仓订单。在每个交易日的下午14点59分时激活，在新的交易日（21点）开始时，重新执行。

        self.height = 2
        self.win = 4
        self.grids = EMPTY_STRING
#
        self.baseUpLine = EMPTY_INT             # 网格做空起步线
        self.baseMidLine = EMPTY_INT         # 基准中轴线，区分多空
        self.baseDnLine = EMPTY_INT             # 网格做多起步线

        self.maxLots = 10                       # 网格的最大数量#
        
        self.lineM5 = None                      # 5分钟K线

        self.logMsg = EMPTY_STRING              # 临时输出日志变量

        if setting:

            # 根据配置文件更新参数
            self.setParam(setting)

            # 创建的M5 K线
            lineM5Setting = {}
            lineM5Setting['name'] = u'M5'
            lineM5Setting['barTimeInterval'] = 60*3
            lineM5Setting['inputBollLen'] = 20
            lineM5Setting['inputBollStdRate'] = 1.5
            lineM5Setting['minDiff'] = self.minDiff
            lineM5Setting['shortSymbol'] = self.shortSymbol
            self.lineM5 = CtaLineBar(self, self.onBar, lineM5Setting)

        self.onInit()

    #----------------------------------------------------------------------
    def onInit(self, force=False):
        """初始化
        从sina上读取近期合约和远期合约，合成价差
        """

        if force:
            self.writeCtaLog(u'策略强制初始化')
            self.inited = False
            self.trading = False                        # 控制是否启动交易
        else:
            self.writeCtaLog(u'策略初始化')
            if self.inited:
                self.writeCtaLog(u'已经初始化过，不再执行')
                return

        if not self.backtesting:
            # 从sina获取最近5天的数据，初始化K线数据
            if not self.__InitDataFromSina():
                return

        # 初始化持仓相关数据
        self.position.pos = EMPTY_INT
        self.pos = self.position.pos
        self.position.maxPos = self.maxPos

        # 初始化网格
        self.gridHeight = self.height * self.minDiff
        self.gridWin = self.win * self.minDiff

        if self.baseUpLine == EMPTY_INT:
            self.writeCtaLog(u'初始化baseUpLine为空，缺省设置为50个MinDiff')
            self.baseUpLine = 50 * self.minDiff         # 网格做空起步线
        if self.baseDnLine == EMPTY_INT:
            self.writeCtaLog(u'baseDnLine，缺省设置为-50个MinDiff')
            self.baseDnLine = -50 * self.minDiff        # 网格做多起步线

        self.upLine = self.baseUpLine                   # 网格做空的上轨
        self.dnLine = self.baseDnLine                   # 网格做多的下轨

        # 创建网格交易策略
        self.gt = CtaGridTrade(strategy=self, maxlots=self.maxLots, height=self.gridHeight, win=self.gridWin, vol=self.inputSS)

        # 更新初始化标识和交易标识
        self.inited = True
        self.trading = True                             # 控制是否启动交易
        self.resubmitOrders = True

        if self.deadLine != EMPTY_STRING:
            try:
                self.deadLineDate = datetime.strptime(self.deadLine, '%Y-%m-%d')
                if not self.backtesting:
                    dt = datetime.now()
                    if (dt - self.deadLineDate).days >= 0:
                        self.tradingOpen = False
                        self.writeCtaLog(u'日期超过最后开仓日期，不再开仓')
            except Exception:
                pass

        self.putEvent()
        self.writeCtaLog(u'策略初始化完成')

    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'启动')

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.uncompletedOrders.clear()
        self.position.pos = 0
        self.entrust = 0

        self.writeCtaLog(u'保存下网格')
        self.gt.save(direction=DIRECTION_LONG)
        self.writeCtaLog(u'保存上网格')
        self.gt.save(direction=DIRECTION_SHORT)

        self.writeCtaLog(u'停止' )
        self.putEvent()


    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """交易更新"""
        self.writeCtaLog(u'{0},OnTrade(),当前持仓：{1} '.format(self.curDateTime, self.position.pos))

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """报单更新"""
        self.writeCtaLog(u'OnOrder()报单更新，orderID:{0},total:{1},traded:{2},offset:{3},price:{4},direction:{5},status:{6}'
                         .format(order.orderID, order.totalVolume,
                                 order.tradedVolume, order.offset, order.price, order.direction, order.status))

        orderkey = order.gatewayName+u'.'+order.orderID

        if orderkey in self.uncompletedOrders:

            if order.totalVolume == order.tradedVolume:
                # 开仓，平仓委托单全部成交
                self.__onOrderAllTraded(order)

            elif order.tradedVolume > 0 and not order.totalVolume == order.tradedVolume and order.offset != OFFSET_OPEN:
                # 平仓委托单部分成交
                self.__onCloseOrderPartTraded(order)

            elif order.offset == OFFSET_OPEN and order.status == STATUS_CANCELLED:
                # 开仓委托单被撤销
                self.__onOpenOrderCanceled(order)

            else:
                self.writeCtaLog(u'OnOrder()委托单返回，total:{0},traded:{1}'
                                 .format(order.totalVolume, order.tradedVolume,))

        self.__updateGridsDisplay()
        self.putEvent()

    def __onOrderAllTraded(self, order):
        """订单的所有成交事件"""

        self.writeCtaLog(u'onOrderAllTraded(),{0},委托单全部完成'.format(order.orderTime ))

        orderkey = order.gatewayName+u'.'+order.orderID

        # 平空仓完成(cover)
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_LONG and order.offset != OFFSET_OPEN:
            # 更新仓位
            self.position.closePos(direction=DIRECTION_LONG, vol = order.tradedVolume)

            # 更新网格交易器，重新建立新的其余upgrids
            self.writeCtaLog(u'平空仓完成，更新网格交易器')
            updateGrid = self.gt.getGrid(direction=DIRECTION_SHORT, closePrice=order.price,
                                         orderRef=order.orderID, t=u'ClosePrice')
            if type(updateGrid) != type(None):
                updateGrid.orderStatus = False
                updateGrid.openStatus = False
                updateGrid.closeStatus = False
                updateGrid.orderRef = EMPTY_STRING
                updateGrid.openDatetime = EMPTY_STRING

                self.writeCtaLog(u'移除网格:{0}'.format(updateGrid.toStr()))
                self.gt.closeGrid(direction=DIRECTION_SHORT, closePrice=updateGrid.closePrice,
                                  closeVolume=order.tradedVolume)
            else:
                self.writeCtaLog(u'异常，找不到网格[closePrice={0}]'.format(order.price))

            if abs(self.position.pos)/self.inputSS > 5:
                self.writeCtaLog(u'持仓超过5个，提升第一个网格的平仓价')
                self.__resubmitFirstGrid(direction=DIRECTION_SHORT,lastVolume=order.tradedVolume)

            self.gt.save(direction=DIRECTION_SHORT)


        # 平多仓完成(sell)
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_SHORT and order.offset != OFFSET_OPEN:
            # 更新仓位
            self.position.closePos(direction=DIRECTION_SHORT, vol=order.tradedVolume)

            # 更新网格交易器，重新建立新的其余dngrids
            self.writeCtaLog(u'平空仓完成，更新网格交易器')
            updateGrid = self.gt.getGrid(direction=DIRECTION_LONG, closePrice=order.price,
                                         orderRef=order.orderID, t=u'ClosePrice')
            if type(updateGrid) != type(None):
                updateGrid.orderStatus = False
                updateGrid.openStatus = False
                updateGrid.closeStatus = False
                updateGrid.orderRef = EMPTY_STRING
                updateGrid.openDatetime = EMPTY_STRING

                self.writeCtaLog(u'移除网格:{0}'.format(updateGrid.toStr()))
                self.gt.closeGrid(direction=DIRECTION_LONG, closePrice=updateGrid.closePrice,
                                  closeVolume=order.tradedVolume)
            else:
                self.writeCtaLog(u'异常，找不到网格[closePrice={0}]'.format(order.price))

            if abs(self.position.pos)/self.inputSS > 5:
                self.writeCtaLog(u'持仓超过5个，降低第一个网格的平仓价')
                self.__resubmitFirstGrid(direction=DIRECTION_LONG,lastVolume=order.tradedVolume)

            self.gt.save(direction=DIRECTION_LONG)

        # 开多仓完成
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_LONG and order.offset == OFFSET_OPEN:

            self.writeCtaLog(u'开多仓完成')
            # 更新仓位
            self.position.openPos(direction=DIRECTION_LONG, vol=order.tradedVolume, price=order.price)

            # 更新网格交易器，发送挂单平多仓
            self.writeCtaLog(u'开多仓完成，更新网格交易器，发送挂单平多仓')
            updateGrid = self.gt.getGrid(direction=DIRECTION_LONG, openPrice=order.price,
                                         orderRef=order.orderID, t=u'OpenPrice')
            if type(updateGrid)!=type(None):
                self.writeCtaLog(u'更新网格[{0}]的状态为开仓成功'.format(updateGrid.openPrice))
                updateGrid.openStatus = True
                updateGrid.openDatetime = datetime.now()

                ref = self.sell(updateGrid.closePrice, updateGrid.volume)
                if ref:
                    updateGrid.orderRef = ref
                    self.writeCtaLog(u'提交平仓委托单[{0}]'.format(updateGrid.toStr()))
            else:
                self.writeCtaLog(u'异常，找不到网格[{0}]'.format(order.price))

            self.gt.save(direction=DIRECTION_LONG)

        # 开空仓完成
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_SHORT and order.offset == OFFSET_OPEN:

            self.writeCtaLog(u'开空仓完成')
            # 更新仓位
            self.position.openPos(direction=DIRECTION_SHORT, vol=order.tradedVolume, price=order.price)

            # 更新网格交易器，发送挂单平空仓
            self.writeCtaLog(u'开空仓完成，更新网格交易器，发送挂单平空仓')
            updateGrid = self.gt.getGrid(direction=DIRECTION_SHORT, openPrice=order.price,
                                         orderRef=order.orderID, t=u'OpenPrice')
            if type(updateGrid)!=type(None):
                self.writeCtaLog(u'更新网格[{0}]的状态为开仓成功'.format(updateGrid.openPrice))
                updateGrid.openStatus = True
                updateGrid.openDatetime = datetime.now()

                ref = self.cover(updateGrid.closePrice, updateGrid.volume)
                if ref:
                    updateGrid.orderRef = ref
                    self.writeCtaLog(u'提交平仓委托单[{0}]'.format(updateGrid.toStr()))
            else:
                self.writeCtaLog(u'异常，找不到网格[{0}]'.format(order.price))

            self.gt.save(direction=DIRECTION_SHORT)

        del self.uncompletedOrders[orderkey]

        self.entrust = 0

    def __onCloseOrderPartTraded(self, order):
        """订单部分平仓"""
        self.writeCtaLog(u'onCloseOrderPartTraded(),{0},委托平仓单部分完成'.format(order.orderTime ))

        orderkey = order.gatewayName+u'.'+order.orderID

        # 平空仓部分完成(cover)
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_LONG and order.offset != OFFSET_OPEN:

            # 更新网格交易器
            self.writeCtaLog(u'平空仓部分完成:{0}/{1}，更新网格交易器'.format(order.tradedVolume,order.totalVolume))
            updateGrid = self.gt.getGrid(direction=DIRECTION_SHORT, closePrice=order.price,
                                         orderRef=order.orderID, t=u'ClosePrice')
            if type(updateGrid) != type(None):
                updateGrid.tradedVolume = order.tradedVolume
            else:
                self.writeCtaLog(u'异常，找不到网格[closePrice={0}]'.format(order.price))

        # 平多仓完成(sell)
        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_SHORT and order.offset != OFFSET_OPEN:

            # 更新网格交易器
            self.writeCtaLog(u'平空仓部分完成:{0}/{1}，更新网格交易器'.format(order.tradedVolume,order.totalVolume))
            updateGrid = self.gt.getGrid(direction=DIRECTION_LONG, closePrice=order.price,
                                         orderRef=order.orderID, t=u'ClosePrice')
            if type(updateGrid) != type(None):
                updateGrid.tradedVolume = order.tradedVolume

            else:
                self.writeCtaLog(u'异常，找不到网格[closePrice={0}]'.format(order.price))


    def __onOpenOrderCanceled(self, order):
        """委托开仓单撤销"""
        self.writeCtaLog(u'__onOpenOrderCanceled(),{0},委托开仓单已撤销'.format(order.orderTime ))

        orderkey = order.gatewayName+u'.'+order.orderID

        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_LONG :
            # 更新网格交易器
            updateGrid = self.gt.getGrid(direction=DIRECTION_LONG, openPrice=order.price,
                                         orderRef=order.orderID, t=u'OpenPrice')
            if type(updateGrid)!=type(None):
                self.writeCtaLog(u'更新网格[{0}]的状态为开多仓撤销'.format(updateGrid.openPrice))
                updateGrid.openStatus = False
                updateGrid.openDatetime = EMPTY_STRING
            else:
                self.writeCtaLog(u'异常，找不到网格[{0}]'.format(order.price))

            self.gt.save(direction=DIRECTION_LONG)

        if self.uncompletedOrders[orderkey]['DIRECTION'] == DIRECTION_SHORT :

            # 更新网格交易器
            updateGrid = self.gt.getGrid(direction=DIRECTION_SHORT, openPrice=order.price,
                                         orderRef=order.orderID, t=u'OpenPrice')
            if type(updateGrid)!=type(None):
                self.writeCtaLog(u'更新网格[{0}]的状态为开空仓撤销'.format(updateGrid.openPrice))
                updateGrid.openStatus = False
                updateGrid.openDatetime = EMPTY_STRING
            else:
                self.writeCtaLog(u'异常，找不到网格[{0}]'.format(order.price))

            self.gt.save(direction=DIRECTION_SHORT)

    # ----------------------------------------------------------------------
    def onStopOrder(self, orderRef):
        """停止单更新"""
        self.writeCtaLog(u'{0},停止单触发，orderRef:{1}'.format(self.curDateTime, orderRef))
        pass

    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """行情更新
        :type tick: object
        """

        # 修正lastPrice，大于中轴(0)时，取最小值，小于中轴时，取最大值
        if tick.bidPrice1 > self.baseMidLine and tick.askPrice1 > self.baseMidLine:
            tick.lastPrice = min(tick.bidPrice1, tick.askPrice1)
        elif tick.bidPrice1 < self.baseMidLine and tick.askPrice1 < self.baseMidLine:
            tick.lastPrice = max(tick.bidPrice1, tick.askPrice1)

        self.curTick = tick

        if (tick.datetime.hour >= 3 and tick.datetime.hour <= 8) or (tick.datetime.hour >= 16 and tick.datetime.hour <= 20):
            self.writeCtaLog(u'休市/集合竞价排名时数据不处理')
            return

        if tick.datetime.hour == 14 and tick.datetime.minute == 59 and not self.resubmitOrders:
            self.writeCtaLog(u'激活重新提交平仓单')
            self.resubmitOrders = True

        if not self.deadLine and self.tradingOpen:
            if (tick.datetime - self.deadLineDate).days >= 0:
                self.tradingOpen = False
                self.writeCtaLog(u'日期超过最后开仓日期，不再开仓')

        # 更新策略执行的时间（用于回测时记录发生的时间）
        self.curDateTime = tick.datetime

        # 2、计算交易时间和平仓时间
        self.__timeWindow(tick)

        # 合约已计算好价差，无需在k线内计算价差,直接推送Tick到lineM5中即可。    
        self.lineM5.onTick(tick)
    

        # 4、交易逻辑

        # 首先检查是否是实盘运行还是数据预处理阶段
        if not (self.inited and len(self.lineM5.lineMiddleBand) > 0):
            return

        # 初始化网格交易器（或从本地记录文件中获取）
        if len(self.gt.upGrids) <= 0 or len(self.gt.dnGrids) <= 0:
            self.writeCtaLog(u'OnTick(),初始化网格交易器')

            upper = round(self.lineM5.lineUpperBand[-1],2)           
            upper = upper - upper % self.minDiff

            lower = round(self.lineM5.lineLowerBand[-1], 2)            
            lower = lower - lower % self.minDiff + self.minDiff

            self.upLine = upper
            self.dnLine = lower
            self.gt.initGrid(upline=max(self.baseUpLine, upper), dnline=min(self.baseDnLine,lower ))

            self.resubmitOrders = True

            return

        # 开盘高开/低开过滤器：如果tick的价差，超出合理平均值，该分钟内不执行交易和挂单；
        if tick.lastPrice > self.baseUpLine :
            if tick.lastPrice - self.lineM5.lineBar[-1].close > self.gridHeight*5:
                self.writeCtaLog(u'tick价格高于上一Bar的收盘价5个网格，不做交易')
                return

        elif tick.lastPrice < self.baseDnLine:
            if self.lineM5.lineBar[-1].close - tick.lastPrice > self.gridHeight*5:
                self.writeCtaLog(u'tick价格低于上一Bar的收盘价5个网格，不做交易')
                return

        if self.tradeWindow and self.resubmitOrders:
            self.writeCtaLog(u'交易时间，撤销订单和重新提交订单')
            # 撤销symbol的所有订单
            self.ctaEngine.cancelOrders(self.symbol)

            # 生产模式下，撤销订单指令提交后，等待1秒
            if not self.backtesting:
                sleep(1)

            # 重新提交订单
            self.__resubmitOrders()

            # 判断是否超过开仓最后期限
            if type(self.deadLineDate) != type(None):
                if (tick.datetime - self.deadLineDate).days >= 0 and self.tradingOpen:
                    self.tradingOpen = False
                    self.writeCtaLog(u'日期超过最后开仓日期，不再开仓')
                    self.putEvent()

            return

        if not self.tradeWindow and self.closeWindow:
            self.resubmitOrders = True

        # 价差与本地挂单最接近价格时，激活本地挂单，提交至服务器，若价差离开挂单太多时，服务器取消挂单
        # 价差进入做空区域；价差高于布林下轨；价差不是当前最高点时，开始挂反套单
        if tick.bidPrice1 >= max(self.baseUpLine, self.lineM5.lastBollMiddle) \
                and tick.askPrice1 < self.lineM5.lineBar[-1].high and self.tradingOpen:

            # 动态网格，获取价格接近的未挂单(当前价格+-1跳)
            pendingGrids = self.gt.getGrids(direction=DIRECTION_SHORT, begin=tick.bidPrice1-self.minDiff,
                                            end=tick.bidPrice1 + self.minDiff)

            m5Up = round(self.lineM5.lineUpperBand[-1], 2)

            # 逐一提交挂单
            for x in pendingGrids[:]:
                openFlag = False
                if x.openPrice >= m5Up :
                    openFlag = True

                # 大于压力上轨才能提交订单
                if openFlag and self.position.avaliablePos2Add()>0:
                    ref = self.short(x.openPrice, x.volume, orderTime=tick.datetime)
                    if ref:
                        self.writeCtaLog(u'开空委托单号{0}'.format(ref))
                        self.gt.updateOrderRef(direction=DIRECTION_SHORT, openPrice=x.openPrice, orderRef=ref)
                        self.gt.removeGrids(direction=DIRECTION_SHORT, priceline=x.openPrice)
                    else:
                        self.writeCtaLog(u'开空委托单失败:{0},v:{1}'.format(x.openPrice, x.volume))
                else:
                    if self.position.avaliablePos2Add()> 0:
                        msg = u'网格[{0}]< M5:{1}，不挂单'.format(x.openPrice, m5Up)
                    else:
                        msg = u'持空仓数量已满，不再开仓'
                    if msg != self.logMsg:
                        self.logMsg = msg
                        self.writeCtaLog(msg)

        # 价差进入做多区域；价差低于布林下轨；价差不是当前最低点时，开始挂正套单
        if tick.askPrice1 < min(self.baseDnLine, self.lineM5.lastBollMiddle) \
                and tick.bidPrice1 > self.lineM5.lineBar[-1].low and self.tradingOpen:

            # 获取价格接近的未挂多单（当前价格 +- 1跳）
            pendingGrids = self.gt.getGrids(direction=DIRECTION_LONG, begin=tick.askPrice1+self.minDiff,
                                            end=tick.askPrice1-self.minDiff)

            m5Dn= round(self.lineM5.lineLowerBand[-1], 2)

            # 逐一提交挂单
            for x in pendingGrids:

                openFlag = False
                if x.openPrice <= m5Dn:
                    # 低于压力下轨才能能开仓
                    openFlag = True

                if openFlag and self.position.avaliablePos2Add()>0:
                    ref = self.buy(x.openPrice, x.volume, orderTime=tick.datetime)
                    if ref:
                        self.writeCtaLog(u'开多委托单号{0}'.format(ref))
                        self.gt.updateOrderRef(direction=DIRECTION_LONG, openPrice=x.openPrice, orderRef=ref)
                    else:
                        self.writeCtaLog(u'开多委托单失败:{0},v:{1}'.format(x.openPrice, x.volume))
                else:
                    if self.position.avaliablePos2Add() > 0:
                        msg = u'网格[{0}]> M5:{1}，不挂单'.format(x.openPrice, m5Dn)
                    else:
                        msg = u'持多仓数量已满，不再开仓'

                    if msg != self.logMsg:
                        self.logMsg = msg
                        self.writeCtaLog(msg)
        # 委托反套状态下，如果价差距离网格超过三个格，取消挂单
        if self.entrust == -1:
            # 若价差离开挂单太多时（三倍网格），服务器取消挂单
            orderedGrids = self.gt.getGrids(direction=DIRECTION_SHORT, ordered=True,
                                            begin=tick.lastPrice+self.gridHeight*3, end=99999)
            for x in orderedGrids:
                self.writeCtaLog(u'取消挂空单：{0}'.format(x.openPrice))
                self.cancelOrder(x.orderRef)
                x.orderRef = EMPTY_STRING
                x.orderStatus = False
                x.openStatus = False

        # 委托正套状态下，如果价差距离网格超过三个格，取消挂单
        if self.entrust == 1:
            orderedGrids = self.gt.getGrids(direction=DIRECTION_LONG, ordered=True,
                                            begin=tick.lastPrice-self.gridHeight*3, end=-99999)
            for x in orderedGrids:
                self.writeCtaLog(u'取消挂多单：{0}'.format(x.openPrice))
                self.cancelOrder(x.orderRef)
                x.orderRef = EMPTY_STRING
                x.orderStatus = False
                x.openStatus = False

        # 收市平仓检查
        #if self.closeWindow:
        #    self.__dailyCloseMarket(tick)

    # ----------------------------------------------------------------------
    def onBar(self, bar):
        """分钟K线数据更新
        bar，k周期数据
        """

        if len(self.lineM5.lineUpperBand) > 0:
            upper = round(self.lineM5.lineUpperBand[-1], 2)
        else:
            upper = 0

        if len(self.lineM5.lineMiddleBand) > 0:
            middle = round(self.lineM5.lineMiddleBand[-1], 2)
        else:
            middle = 0

        if len(self.lineM5.lineLowerBand) > 0:
            lower = round(self.lineM5.lineLowerBand[-1], 2)
        else:
            lower = 0

        upper = upper - upper % self.minDiff
        lower = lower - lower % self.minDiff + self.minDiff

        # 若初始化完毕
        if self.inited:
            if len(self.gt.upGrids) <= 0 or len(self.gt.dnGrids) <= 0:
                self.writeCtaLog(u'OnBar()初始化网格交易器')

                self.gt.initGrid(upline=max(self.baseUpLine, upper), dnline=min(self.baseDnLine,lower ))

                self.resubmitOrders = True

            else:
                # 检查重建
                if bar.close > self.baseUpLine and upper != self.upLine :
                    self.upLine = upper
                    self.gt.rebuildGrids(direction=DIRECTION_SHORT, upline=max(self.baseUpLine, self.upLine), midline=self.baseMidLine)
                    self.__updateGridsDisplay()

                if bar.close < self.baseDnLine and lower != self.dnLine :
                    self.dnLine = lower
                    self.gt.rebuildGrids(direction=DIRECTION_LONG, dnline=min(self.baseDnLine, self.dnLine), midline=self.baseMidLine)
                    self.__updateGridsDisplay()

            self.putEvent()

    def __updateGridsDisplay(self):
        """更新网格显示信息"""

        if self.curTick.lastPrice > self.baseMidLine:
            self.grids = self.gt.toStr(direction=DIRECTION_SHORT)
            self.writeCtaLog(self.grids)

        else:
            self.grids = self.gt.toStr(direction=DIRECTION_LONG)
            self.writeCtaLog(self.grids)

    def __InitDataFromSina(self):
        """从sina获取初始化数据"""

        # 从sina加载最新的M1数据
        try:
            sleep(1)

            # 获取D2的5日分时数据

            D2 = {}

            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False

            url = u'http://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesService.getInnerFutures5MLine?symbol={0}'.format(self.D2Symbol)
            self.writeCtaLog(u'从sina下载{0}数据 {1}'.format(self.D2Symbol, url))
            responses = execjs.eval(s.get(url).content.decode('gbk').split('\n')[-1])

            datevalue = datetime.now().strftime('%Y-%m-%d')

            for j, day_item in enumerate(responses[str(self.D2Symbol).upper()]):
                for i, item in enumerate(day_item):

                    tick = CtaTickData()

                    tick.vtSymbol = self.vtSymbol
                    tick.symbol = self.symbol

                    if len(item) >= 6:
                        datevalue = item[6]

                    tick.date = datevalue
                    tick.time = item[4]+u':00'
                    tick.datetime = datetime.strptime(tick.date+' '+tick.time, '%Y-%m-%d %H:%M:%S')

                    tick.lastPrice = float(item[0])
                    tick.volume = int(item[2])

                    if type(item[3]) == type(None) :
                        tick.openInterest = 0
                    else:
                        tick.openInterest = int(item[3])

                    D2[tick.date+' '+tick.time] = tick

            sleep(1)

            url = u'http://stock2.finance.sina.com.cn/futures/api/json.php/InnerFuturesService.getInnerFutures5MLine?symbol={0}'.format(self.D1Symbol)
            responses = execjs.eval(s.get(url).content.decode('gbk').split('\n')[-1])

            self.writeCtaLog(u'从sina下载{0}数据 {1}'.format(self.D1Symbol, url))

            datevalue = datetime.now().strftime('%Y-%m-%d')

            for j, day_item in enumerate(responses[str(self.D1Symbol).upper()]):
                for i, item in enumerate(day_item):

                    bar = CtaBarData()

                    bar.vtSymbol = self.vtSymbol
                    bar.symbol = self.symbol

                    if len(item) >= 6:
                        datevalue = item[6]

                    bar.date = datevalue
                    bar.time = item[4]+u':00'
                    bar.datetime = datetime.strptime(bar.date+' '+bar.time, '%Y-%m-%d %H:%M:%S')

                    d1LastPrice = float(item[0])
                    bar.volume = int(item[2])

                    if bar.date+' '+bar.time in D2:
                        tick = D2[bar.date+' '+bar.time]
                        d2LastPrice = tick.lastPrice

                        bar.open = d1LastPrice - d2LastPrice
                        bar.high = d1LastPrice - d2LastPrice
                        bar.low = d1LastPrice - d2LastPrice
                        bar.close = d1LastPrice - d2LastPrice
                       
                        self.lineM5.addBar(bar)
                        
            D2.clear()

            return True

        except Exception as e:
            self.writeCtaLog(u'策略初始化加载历史数据失败：'+str(e))
            return False

    # ----------------------------------------------------------------------
    def __timeWindow(self, tick):
        """交易与平仓窗口"""
        # 交易窗口 避开早盘和夜盘的前5分钟，防止隔夜跳空。

        self.closeWindow = False
        self.tradeWindow = False
        self.openWindow = False

        # 初始化当日的首次交易
        #if (tick.datetime.hour == 9 or tick.datetime.hour == 21) and tick.datetime.minute == 0 and tick.datetime.second ==0:
        #  self.firstTrade = True

        # 开市期，波动较大，用于判断止损止盈，或开仓
        if (tick.datetime.hour == 9 or tick.datetime.hour == 21) and tick.datetime.minute < 10:
            self.openWindow = True

        # 日盘
        if tick.datetime.hour == 9 and tick.datetime.minute >= 0:
            self.tradeWindow = True
            return

        if tick.datetime.hour == 10:
            if tick.datetime.minute <= 15 or tick.datetime.minute >= 30:
                self.tradeWindow = True
                return

        if tick.datetime.hour == 11 and tick.datetime.minute <= 30:
            self.tradeWindow = True
            return

        if tick.datetime.hour == 13 and tick.datetime.minute >= 30:
            self.tradeWindow = True
            return

        if tick.datetime.hour == 14:

            if tick.datetime.minute < 59:
                self.tradeWindow = True
                return

            if tick.datetime.minute == 59:                 # 日盘平仓
                self.closeWindow = True
                return

        # 夜盘

        if tick.datetime.hour == 21 and tick.datetime.minute >= 0:
            self.tradeWindow = True
            return

        # 上期 贵金属， 次日凌晨2:30
        if self.shortSymbol in NIGHT_MARKET_SQ1:

            if tick.datetime.hour == 22 or tick.datetime.hour == 23 or tick.datetime.hour == 0 or tick.datetime.hour ==1:
                self.tradeWindow = True
                return

            if tick.datetime.hour == 2:
                if tick.datetime.minute < 29:                 # 收市前29分钟
                    self.tradeWindow = True
                    return
                if tick.datetime.minute == 29:                 # 夜盘平仓
                    self.closeWindow = True
                    return
            return

        # 上期 有色金属，黑色金属，沥青 次日01:00
        if self.shortSymbol in NIGHT_MARKET_SQ2:
            if tick.datetime.hour == 22 or tick.datetime.hour == 23:
                self.tradeWindow = True
                return

            if tick.datetime.hour == 0:
                if tick.datetime.minute < 59:              # 收市前29分钟
                    self.tradeWindow = True
                    return

                if tick.datetime.minute == 59:                 # 夜盘平仓
                    self.closeWindow = True
                    return

            return

        # 上期 天然橡胶  23:00
        if self.shortSymbol in NIGHT_MARKET_SQ3:

            if tick.datetime.hour == 22:
                if tick.datetime.minute < 59:              # 收市前1分钟
                    self.tradeWindow = True
                    return

                if tick.datetime.minute == 59:                 # 夜盘平仓
                        self.closeWindow = True
                        return

        # 郑商、大连 23:30
        if self.shortSymbol in NIGHT_MARKET_ZZ or self.shortSymbol in NIGHT_MARKET_DL:
            if tick.datetime.hour == 22:
                self.tradeWindow = True
                return

            if tick.datetime.hour == 23:
                if tick.datetime.minute < 29:                 # 收市前1分钟
                    self.tradeWindow = True
                    return
                if tick.datetime.minute == 29 and tick.datetime.second > 30:                 # 夜盘平仓
                    self.closeWindow = True
                    return
            return


    def __resubmitFirstGrid(self, direction, lastVolume):
        """修改第一个网格的平仓价格"""

        if direction == DIRECTION_SHORT:
            grid = self.gt.upGrids[0]
            if not grid.openStatus or not grid.orderStatus or grid.closeStatus or grid.orderRef == EMPTY_STRING:
                self.writeCtaLog(u'网格[open={0},close={1} 不满足状态'.format(grid.openPrice,grid.closePrice))
                return

            self.writeCtaLog(u'取消平空单:[ref={0},closeprice={1}]'.format(grid.orderRef,grid.closePrice))
            self.cancelOrder(grid.orderRef)

            sleep(0.3)

            oldPrice = grid.closePrice
            if lastVolume > (grid.volume-grid.tradedVolume):
                grid.closePrice = grid.closePrice + self.gt.gridHeight
            else:
                grid.closePrice = grid.closePrice + self.minDiff

            ref = self.cover(price=grid.closePrice, volume=grid.volume-grid.tradedVolume)

            if ref:
                grid.orderRef = ref
                self.writeCtaLog(u'提交平仓委托单[closeprice={0},volume={1}]'
                                 .format(grid.closePrice, grid.volume-grid.tradedVolume))
            else:
                self.writeCtaLog(u'提交平仓委托单失败')

                grid.closePrice = oldPrice

        if direction == DIRECTION_LONG:
            grid = self.gt.dnGrids[0]
            if not grid.openStatus or not grid.orderStatus or grid.closeStatus or grid.orderRef == EMPTY_STRING:
                self.writeCtaLog(u'网格[open={0},close={1} 不满足状态'.format(grid.openPrice,grid.closePrice))
                return

            self.writeCtaLog(u'取消平多单:[ref={0},closeprice={1}]'.format(grid.orderRef,grid.closePrice))
            self.cancelOrder(grid.orderRef)

            sleep(0.1)
            oldPrice = grid.closePrice

            if lastVolume > grid.volume:
                grid.closePrice = grid.closePrice - self.gt.gridHeight
            else:
                grid.closePrice = grid.closePrice - self.minDiff

            ref = self.sell(price=grid.closePrice, volume=grid.volume)

            if ref:
                grid.orderRef = ref
                self.writeCtaLog(u'提交平仓委托单[closeprice={0},volume={1}]'.format(grid.closePrice,grid.volume))
            else:
                self.writeCtaLog(u'提交平仓委托单失败')
                grid.closePrice = oldPrice


    def __resubmitOrders(self):
        """重新提交平仓订单"""

        self.writeCtaLog(u'扫描网格，重新提交上一交易日的平仓委托单')

        # 重置pos为零
        self.position.pos = 0

        resubmits = EMPTY_INT

        # 扫描上网格
        for x in self.gt.upGrids[:]:
            # 已发送订单，已开仓，未平仓
            if x.orderStatus and x.openStatus and not x.closeStatus:
                closePrice = min(x.closePrice, self.curTick.askPrice1)
                # 未平仓的volume=网格的volume-已交易的volume，
                ref = self.cover(closePrice, x.volume-x.tradedVolume)
                if ref:
                    # 更新仓位
                    self.position.openPos(direction=DIRECTION_SHORT, vol=x.volume-x.tradedVolume, price=x.openPrice)
                    x.orderRef = ref
                    x.closePrice = closePrice
                    resubmits = resubmits+1
                    self.writeCtaLog(u'重新提交平空仓委托单[{0}]'.format(x.closePrice))

            elif x.orderStatus and not x.openStatus:
                self.writeCtaLog(u'重置网格的开仓单为空')
                x.orderStatus = False
                x.orderRef = EMPTY_STRING


        if resubmits == EMPTY_INT:
            self.writeCtaLog(u'上网格没有平空仓委托单')

        resubmits = EMPTY_INT
        # 扫描下网格
        for x in self.gt.dnGrids[:]:
            # 已发送订单，已开仓，未平仓
            if x.orderStatus and x.openStatus and not x.closeStatus:
                closePrice = max(x.closePrice, self.curTick.bidPrice1)
                # 未平仓的volume=网格的volume-已交易的volume，
                ref = self.sell(closePrice, x.volume-x.tradedVolume)
                if ref:
                    # 更新仓位
                    self.position.openPos(direction=DIRECTION_LONG, vol=x.volume-x.tradedVolume, price=x.openPrice)

                    x.orderRef = ref
                    x.closePrice = closePrice
                    resubmits = resubmits+1
                    self.writeCtaLog(u'重新提交平多仓委托单[{0}]'.format(x.closePrice))
            elif x.orderStatus and not x.openStatus:
                self.writeCtaLog(u'重置网格的开仓单为空')
                x.orderStatus = False
                x.orderRef = EMPTY_STRING

        if resubmits == EMPTY_INT:
            self.writeCtaLog(u'下网格没有平空仓委托单')

        # 重置为已执行
        self.resubmitOrders = False

    #----------------------------------------------------------------------
    def strToTime(self, t, ms):
        """从字符串时间转化为time格式的时间"""
        hh, mm, ss = t.split(':')
        tt = datetime.time(int(hh), int(mm), int(ss), microsecond=ms)
        return tt

     #----------------------------------------------------------------------
    def saveData(self, id):
        """保存过程数据"""
        # 保存K线
        if not self.backtesting:
            return


def testM():

    # 创建回测引擎
    engine = BacktestingEngine()

    # 设置引擎的回测模式为Tick
    engine.setBacktestingMode(engine.TICK_MODE)

    # 设置回测用的数据起始日期
    engine.setStartDate('20160401')

    # 设置回测用的数据结束日期
    engine.setEndDate('20160830')

    # engine.connectMysql()
    engine.setDatabase(dbName='stockcn', symbol='m')

    # 设置产品相关参数
    engine.setSlippage(0)  # 1跳（0.1）2跳0.2
    engine.setRate(float(0.0001))  # 万1
    engine.setSize(10)  # 合约大小

    settings = {}
    settings['shortSymbol'] = 'M'
    settings['minDiff'] = 1
    settings['inputSS'] = 1
    settings['name'] = 'ArbM'
    settings['mode'] = 'tick'
    settings['D1Symbol'] = 'm1609'
    settings['D2Symbol'] = 'm1701'
    settings['backtesting'] = True
    settings['baseUpLine'] = 60
    settings['baseDnLine'] = -60
    settings['height'] = 4
    settings['win'] = 4
    settings['maxPos'] = 80
    settings['maxLots'] = 30
    settings['deadLine'] = '2016-8-29'

    # 删除本地json文件
    filename = os.getcwd() + '\{0}_upGrids.json'.format(settings['name'])
    if os.path.isfile(filename):
        print(u'{0}文件存在，先执行删除'.format(filename))
        try:
            os.remove(filename)
        except Exception as ex:
            print(u'{0}：{1}'.format(Exception, ex))
    filename = os.getcwd() + '\{0}_dnGrids.json'.format(settings['name'])
    if os.path.isfile(filename):
        print(u'{0}文件存在，先执行删除'.format(filename))
        try:
            os.remove(filename)
        except Exception as ex:
            print(u'{0}：{1}'.format(Exception, ex))

    # 在引擎中创建策略对象
    engine.initStrategy(Strategy_ArbitrageGrid, setting=settings)

    # 使用简单复利模式计算
    engine.usageCompounding = False  # True时，只针对FINAL_MODE有效

    # 启用实时计算净值模式REALTIME_MODE / FINAL_MODE 回测结束时统一计算模式
    engine.calculateMode = engine.REALTIME_MODE
    engine.initCapital = 100000  # 设置期初资金
    engine.percentLimit = 30  # 设置资金使用上限比例(%)
    engine.barTimeInterval = 60  # bar的周期秒数，用于csv文件自动减时间
    engine.fixCommission = 10  # 固定交易费用（每次开平仓收费）
    # 开始跑回测
    engine.runBackTestingWithArbTickFile('DCE','SP M1609&M1701')

    # 显示回测结果
    engine.showBacktestingResult()


# 从csv文件进行回测
if __name__ == '__main__':
    # 提供直接双击回测的功能
    # 导入PyQt4的包是为了保证matplotlib使用PyQt4而不是PySide，防止初始化出错
    from ctaBacktesting import *
    from setup_logger import setup_logger
    setup_logger(
        filename=u'TestLogs/{0}_{1}.log'.format(Strategy_ArbitrageGrid.className, datetime.now().strftime('%m%d_%H%M')),
        debug=False)

    # 回测豆粕
    testM()



