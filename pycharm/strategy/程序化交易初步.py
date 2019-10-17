# -*- coding: utf-8 -*-
"""
python是个简单、强大，可高度定制，并且还有很多包可以使用，所以可以考虑用python来编程实现股票的自动技术分析。
本文默认使用的是python3.5版本，并且未涉及爬虫与数据库等，仅为相关库和思路的介绍，以及一份示例代码。

一个完整的程序化交易平台应包括那些子系统和组件：1、证券信息组件，2、帐户体系组件，3、行情子系统，4、策略管理子系统，5、交易接口子系统，6、订单管理子系统，7、后台管理子系统，8、清算子系统，9、用户界面子系统，10、模拟撮合子系统。此处不讨论本类较为完善的系统。

从技术角度来说需要满足：1，业务的高扩展性、2，高性能、3，高稳定、4，高可验证性。实际上就是两个输入（行情、单回报），一个输出（订单）

一：股票的历史数据获取
此处可以使用tushare包[http://tushare.org/]或者是用通联的数据，不过tushare里面也有，实测没有通联直接的接口快。还是以tushare为例
mac系统下，在命令行下输入
pip3 install tushare
在安装的时候，pip会自动处理依赖包的，所以应该没有什么问题，如果提示缺少什么模块的话，就按照提示安装相应的模块就可以了
对了，pip是python的包管理器，pip3是python3版本下的，如果单独安装python3的话，应该可以直接用pip？mac默认的是有python2的，所以还是用pip3
关于pip[https://pip.pypa.io/en/stable/installing/]

二：技术分析相关
对于技术分析的话，就是对于所获取到的数据，进行处理，主要用到的包得安装方式同上，因为都是被放到了pypi上了，所以直接用pip安装，很方便的
技术指标，不得不提大名鼎鼎的tb-lib[http://ta-lib.org/],超过150+的技术指标
数据分析库，pandas[http://pandas.pydata.org/]
科学计算基础库，numpy[http://www.numpy.org/]
科学计算加强库，scipy[http://docs.scipy.org/doc/]
python的基础库中的cmath,bisect,collections分别是复杂计算，排序，容器的库 [https://docs.python.org/3.5/library/cmath.html] [https://docs.python.org/3.5/library/bisect.html] [https://docs.python.org/3.5/library/collections.html]

三：技术分析相关补充
一个用的比较多的画图的库，matplotlib[http://matplotlib.org/]
符号运算库，sympy[http://www.sympy.org/en/index.html]
统计回归的库，statsmodels[http://statsmodels.sourceforge.net/],目测好多平台的回测应该用的这个
机器学习的库，sklearn[]
隐马尔科夫链学习的库，hmmlearn[]
卡尔曼滤波的库，pykalman[]
小波分析的库，pywt[]
一个机器学习的框架,目前支持python接口，tensorflow[]
微软出的一个机器学习的框架，cntk[https://github.com/Microsoft/CNTK],好像目前性能是最好的

四：大致的思路是
1，引入数据源
2，判断持仓：
若已经持仓，则分析目前的信号根据编写的策略是否支持继续持有，此处信号应为实时信号
若为选股，则循环遍历选定的股票池，或者根据条件将对应选出的股票添加进股票池，或者写入文件或数据库，准备进一步分析
3，接入对应的买入卖出的接口，若不接实盘，则此步骤可略过
4，接入实时策略
在交易时间内，根据所接入的信号，执行所划定的止盈止损、技术指标信号等，调用买入卖出等函数，进行交易，如果需要，并且可以接入短信或者邮件进行通知

五，示例代码
下边是我从网上找的例子，我没调试。。估计调一下之后应该可以跑

这里用MACD的例子来坐下分析。
首先是用TA-lib的macd函数计算macd值，函数输出3个值，macd（对应diff），macdsignal（对应dea），macdhist（对应macd）。然后按照下面的原则判断买入还是卖出。
1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 
2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
3.DEA线与K线发生背离，行情反转信号。
4.分析MACD柱状线，由正变负，卖出信号；由负变正，买入信号。
"""

import tushare as ts
import talib as ta
import numpy as np
import pandas as pd
import os, time, sys, re, datetime
import csv
import scipy
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
 
# 首先是获取沪深两市的股票列表
# 这里得到是对应的dataframe数据结构，它是类似于excel中一片数据的数据结构，
# 有这些列：code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)
# liquidAssets,流动资产 fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率
# timeToMarket,上市日期
def Get_Stock_List():
    df = ts.get_stock_basics()
    return df


# 然后定义通过MACD判断买入卖出
def Get_MACD(df_Code):
    operate_array = []
    for code in df_Code.index:
# 获取每只股票的历史价格和成交量 对应的列有index列,0 - 6列是 date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量
# price_change：价格变动 p_change：涨跌幅
# 7-12列是 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量v_ma10:10日均量 v_ma20:20日均量
        df = ts.get_hist_data(code, start='2014-11-20')
        dflen = df.shape[0]
        operate = 0
        if dflen > 35:
            macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26,signalperiod=9)
            SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
            SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
            SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
            # 在后面增加3列，分别是13-15列，对应的是 DIFF  DEA  DIFF-DEA       
            df['macd'] = pd.Series(macd, index=df.index)  # DIFF
            df['macdsignal'] = pd.Series(macdsignal, index=df.index)  # DEA
            df['macdhist'] = pd.Series(macdhist, index=df.index)  # DIFF-DEA
            MAlen = len(SignalMA5)
# 2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    if df.iat[(dflen - 1), 13] > 0:
        if df.iat[(dflen - 1), 14] > 0:
            if df.iat[(dflen - 1), 13] > df.iat[(dflen - 1), 14]:
                operate = operate + 1  # 买入
            else:
                if df.iat[(dflen - 1), 14] < 0:
                    if df.iat[(dflen - 1), 13]]:
                        operate = operate - 1  # 卖出

                  # 3.DEA线与K线发生背离，行情反转信号。
                 if df.iat[(dflen-1), 7] >= df.iat[(dflen-1), 8] and df.iat[(dflen-1), 8] >= df.iat[(dflen-1), 9]:  # K线上涨
                        if SignalMA5[MAlen - 1] <= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] <= SignalMA20[MAlen - 1]:  # DEA下降
                            operate = operate - 1
                     elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[(dflen - 1), 9]:  # K线下降
                    if SignalMA5[MAlen - 1] >= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] >= SignalMA20[MAlen - 1]:  # DEA上涨
                            operate = operate + 1
                            
        # 4.分析MACD柱状线，由负变正，买入信号。
                    if df.iat[(dflen - 1), 15] > 0 and dflen > 30:
                            for i in range(1, 26):
                                if df.iat[(dflen - 1 - i), 15] <= 0:  #
                                    operate = operate + 1
                                break
                      # 由正变负，卖出信号   
                    if df.iat[(dflen - 1), 15] < 0 and dflen > 30:
                            for i in range(1, 26):
                                    if df.iat[(dflen - 1 - i), 15] >= 0:  #
                                            operate = operate - 1
                                break
                       
                operate_array.append(operate)        
            df_Code['MACD'] = pd.Series(operate_array, index=df_Code.index)   
            return df_Code
         
        # 输出CSV文件，其中要进行转码，不然会乱码
        def Output_Csv(df, Dist):

                TODAY = datetime.date.today()

            CURRENTDAY = TODAY.strftime('%Y-%m-%d')
            reload(sys)
            sys.setdefaultencoding("gbk")
            df.to_csv(Dist + CURRENTDAY + 'stock.csv', encoding='gbk')  # 选择保存   
         
        def Close_machine():

                o = "c:\\windows\\system32\\shutdown -s"  #########

            os.system(o)  #########
           
        # 发送邮件
        def Send_Mail(Message, Dist):

                TODAY = datetime.date.today()

            CURRENTDAY = TODAY.strftime('%Y-%m-%d')
            msg = MIMEMultipart()
           
            TODAY = datetime.date.today()
            CURRENTDAY = TODAY.strftime('%Y-%m-%d')
            att = MIMEText(open(Dist + CURRENTDAY + 'stock.csv', 'rb').read(), 'base64', 'gb2312')  # 设置附件的目录
            att['content-type'] = 'application/octet-stream'
            att['content-disposition'] = 'attachment;filename="stock.csv"'  # 设置附件的名称
            msg.attach(att)
           
            content = str(Message)  # 正文内容
            body = MIMEText(content, 'plain', 'GBK')  # 设置字符编码
            msg.attach(body)
            msgto = ['xx@126.com']  # 收件人地址多个联系人，格式['aa@163.com'; 'bb@163.com']
            msgfrom = 'xx@126.com'   # 寄信人地址 ,
            msg['subject'] = 'Finish at ' + CURRENTDAY    # 主题
            msg['date'] = time.ctime()  # 时间
              # msg['Cc']='bb@junbao.net' #抄送人地址 多个地址不起作用

            mailuser = 'xx'    # 用户名
            mailpwd = 'xx'  # 密码
            try:
                    smtp = smtplib.SMTP()
                smtp.connect(r'smtp.126.com')  # smtp设置
                smtp.login(mailuser, mailpwd)  # 登录
                smtp.sendmail(msgfrom, msgto, msg.as_string())  # 发送
                smtp.close()
                print
        "success mail"
            except Exception, e:
                print
        e
               
        df = Get_Stock_List()
        df = Get_MACD(df)
        Dist = 'E:\\08 python\\Output\\'
        Output_Csv(df, Dist)
        # 生成的csv文件中，macd列大于0的就是可以买入的，小于0的就是卖出的
        Send_Mail('Finish TA', Dist)
        Close_machine()
        # coding=utf-8
        import tushare as ts
        import talib as ta
        import numpy as np
        import pandas as pd
        import os, time, sys, re, datetime
        import csv
        import scipy
        import smtplib
        from email.mime.text import MIMEText
        from email.MIMEMultipart import MIMEMultipart
         
        # 获取股票列表
        # code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
        # fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
        def Get_Stock_List():

                df = ts.get_stock_basics()

            return df
         
        # 修改了的函数，按照多个指标进行分析
        # 按照MACD，KDJ等进行分析
        def Get_TA(df_Code, Dist):

                operate_array1 = []

            operate_array2 = []
            operate_array3 = []
           
            count = 0
            for code in df_Code.index:
        # index,0 - 6 date：日期 open：开盘价 high：最高价 close：收盘价 low：最低价 volume：成交量 price_change：价格变动 p_change：涨跌幅
        # 7-12 ma5：5日均价 ma10：10日均价 ma20:20日均价 v_ma5:5日均量v_ma10:10日均量 v_ma20:20日均量
                df = ts.get_hist_data(code, start='2014-11-20')
                dflen = df.shape[0]
                count = count + 1       
                if dflen > 35:
                        try:
                                (df, operate1) = Get_MACD(df) 
                                (df, operate2) = Get_KDJ(df)
                                (df, operate3) = Get_RSI(df)
                            except Exception, e:
                                 Write_Blog(e, Dist)
                                 pass
                        operate_array1.append(operate1)    # round(df.iat[(dflen-1),16],2)
                        operate_array2.append(operate2)
                        operate_array3.append(operate3)
                        if count00 == 0:
                                Write_Blog(str(count), Dist)
                    df_Code['MACD'] = pd.Series(operate_array1, index=df_Code.index)
                    df_Code['KDJ'] = pd.Series(operate_array2, index=df_Code.index)
                    df_Code['RSI'] = pd.Series(operate_array3, index=df_Code.index)
                    return df_Code
                 
                # 通过MACD判断买入卖出
                def Get_MACD(df):

                          # 参数12,26,9
                        macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26,
                                                             signalperiod=9)
                                       
                        SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
                        SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
                        SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
                          # 13-15 DIFF  DEA  DIFF-DEA       
                        df['macd'] = pd.Series(macd, index=df.index)  # DIFF
                        df['macdsignal'] = pd.Series(macdsignal, index=df.index)  # DEA
                        df['macdhist'] = pd.Series(macdhist, index=df.index)  # DIFF-DEA
                        dflen = df.shape[0]
                        MAlen = len(SignalMA5)
                        operate = 0
                          # 2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
                          # 待修改
                        if df.iat[(dflen - 1), 13] > 0:
                                if df.iat[(dflen - 1), 14] > 0:
                                        if df.iat[(dflen - 1), 13] > df.iat[(dflen - 1), 14] and df.iat[
                                (dflen - 2), 13] <=
                                df.iat[(dflen - 2), 14]:
                                            operate = operate + 10  # 买入
                        else:
                            if df.iat[(dflen - 1), 14] < 0:
                                    if df.iat[(dflen - 1), 13]=df.iat[(dflen-2), 14]:
                                            operate = operate - 10  # 卖出
                           
                          # 3.DEA线与K线发生背离，行情反转信号。
                        if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[
                        (dflen - 1), 9]:  # K线上涨
                                if SignalMA5[MAlen - 1] <= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] <=
                                SignalMA20[
                                            MAlen - 1]:  # DEA下降
                                        operate = operate - 1
                         elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[
                        (dflen - 1), 9]:  # K线下降
                            if SignalMA5[MAlen - 1] >= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] >= SignalMA20[
                                MAlen - 1]:  # DEA上涨
                                    operate = operate + 1
                                   
                           
                          # 4.分析MACD柱状线，由负变正，买入信号。
                        if df.iat[(dflen - 1), 15] > 0 and dflen > 30:
                                for i in range(1, 26):
                                        if df.iat[(dflen - 1 - i), 15] <= 0:  #
                                                operate = operate + 5
                                    break
                                  # 由正变负，卖出信号   
                        if df.iat[(dflen - 1), 15] < 0 and dflen > 30:
                                for i in range(1, 26):
                                        if df.iat[(dflen - 1 - i), 15] >= 0:  #
                                                operate = operate - 5
                                    break
                                
                        return (df, operate)
                     
                    # 通过KDJ判断买入卖出
                    def Get_KDJ(df):

                              # 参数9,3,3
                            slowk, slowd = ta.STOCH(np.array(df['high']), np.array(df['low']), np.array(df['close']),
                                                    fastk_period=9, slowk_period=3, slowk_matype=0,
                                                    slowd_period=3, slowd_matype=0)
                           
                            slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
                            slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
                            slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
                            slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
                            slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
                            slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)
                              # 16-17 K,D      
                            df['slowk'] = pd.Series(slowk, index=df.index)  # K
                            df['slowd'] = pd.Series(slowd, index=df.index)  # D
                            dflen = df.shape[0]
                            MAlen = len(slowkMA5)
                            operate = 0
                              # 1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
                            if df.iat[(dflen - 1), 16] >= 90:
                                    operate = operate - 3
                             elif df.iat[(dflen - 1), 16] <= 10:
                                operate = operate + 3
                               
                            if df.iat[(dflen - 1), 17] >= 80:
                                    operate = operate - 3
                             elif df.iat[(dflen - 1), 17] <= 20:
                                operate = operate + 3
                               
                              # 2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号。#待修改
                            if df.iat[(dflen - 1), 16] > df.iat[(dflen - 1), 17] and df.iat[(dflen - 2), 16] <= df.iat[
                            (dflen - 2), 17]:
                                    operate = operate + 10
                              # 下跌趋势中，K小于D，K线向下跌破D线时，为卖出信号。#待修改
                             elif df.iat[(dflen - 1), 16] < df.iat[(dflen - 1), 17] and df.iat[(dflen - 2), 16] >=
                                                                                        df.iat[
                                                                                            (dflen - 2), 17]:
                                operate = operate - 10
                           
                               
                              # 3.当随机指标与股价出现背离时，一般为转势的信号。
                            if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >= df.iat[
                            (dflen - 1), 9]:  # K线上涨
                                    if (
                                    slowkMA5[MAlen - 1] <= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] <= slowkMA20[
                                    MAlen - 1]) or \
                                               (slowdMA5[MAlen-1] <= slowdMA10[MAlen-1] and slowdMA10[MAlen-1] <= slowdMA20[MAlen-1]):  # K,D下降
                                            operate = operate - 1
                             elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <= df.iat[
                            (dflen - 1), 9]:  # K线下降
                                if (
                                        slowkMA5[MAlen - 1] >= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] >=
                                    slowkMA20[MAlen - 1]) or \
                                           (slowdMA5[MAlen-1] >= slowdMA10[MAlen-1] and slowdMA10[MAlen-1] >= slowdMA20[MAlen-1]):  # K,D上涨
                                        operate = operate + 1
                                   
                            return (df, operate)
                         
                        # 通过RSI判断买入卖出
                        def Get_RSI(df):

                                  # 参数14,5
                                slowreal = ta.RSI(np.array(df['close']), timeperiod=14)
                                fastreal = ta.RSI(np.array(df['close']), timeperiod=5)
                            slowrealMA5 = ta.MA(slowreal, timeperiod=5, matype=0)
                                slowrealMA10 = ta.MA(slowreal, timeperiod=10, matype=0)
                                slowrealMA20 = ta.MA(slowreal, timeperiod=20, matype=0)
                                fastrealMA5 = ta.MA(fastreal, timeperiod=5, matype=0)
                                fastrealMA10 = ta.MA(fastreal, timeperiod=10, matype=0)
                                fastrealMA20 = ta.MA(fastreal, timeperiod=20, matype=0)
                                  # 18-19 慢速real，快速real      
                                df['slowreal'] = pd.Series(slowreal, index=df.index)  # 慢速real 18
                                df['fastreal'] = pd.Series(fastreal, index=df.index)  # 快速real 19
                                dflen = df.shape[0]
                                MAlen = len(slowrealMA5)
                                operate = 0
                                  # RSI>80为超买区，RSI<20为超卖区
                                if df.iat[(dflen - 1), 18] > 80 or df.iat[(dflen - 1), 19] > 80:
                                        operate = operate - 2
                                 elif df.iat[(dflen - 1), 18] < 20 or df.iat[(dflen - 1), 19] < 20:
                                    operate = operate + 2
                                   
                                  # RSI上穿50分界线为买入信号，下破50分界线为卖出信号
                                if (df.iat[(dflen - 2), 18] <= 50 and df.iat[(dflen - 1), 18] > 50) or (
                                            df.iat[(dflen - 2), 19] <= 50 and df.iat[(dflen - 1), 19] > 50):
                                        operate = operate + 4
                                 elif (df.iat[(dflen - 2), 18] >= 50 and df.iat[(dflen - 1), 18] < 50) or (
                                df.iat[(dflen - 2), 19] >= 50 and df.iat[(dflen - 1), 19] < 50):
                                    operate = operate - 4
                                   
                                  # RSI掉头向下为卖出讯号，RSI掉头向上为买入信号
                                if df.iat[(dflen - 1), 7] >= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] >=
                                    df.iat[
                                        (dflen - 1), 9]:  # K线上涨
                                        if (
                                        slowrealMA5[MAlen - 1] <= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] <=
                                    slowrealMA20[MAlen - 1]) or \
                                                   (fastrealMA5[MAlen-1] <= fastrealMA10[MAlen-1] and fastrealMA10[MAlen-1] <= fastrealMA20[MAlen-1]):  # RSI下降
                                                operate = operate - 1
                                 elif df.iat[(dflen - 1), 7] <= df.iat[(dflen - 1), 8] and df.iat[(dflen - 1), 8] <=
                                                                                           df.iat[
                                                                                               (dflen - 1), 9]:  # K线下降
                                    if (slowrealMA5[MAlen - 1] >= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] >=
                                slowrealMA20[MAlen - 1]) or \
                                               (fastrealMA5[MAlen-1] >= fastrealMA10[MAlen-1] and fastrealMA10[MAlen-1] >= fastrealMA20[MAlen-1]):  # RSI上涨
                                            operate = operate + 1
                               
                                
                            # 慢速线与快速线比较观察，若两线同向上，升势较强；若两线同向下，跌势较强；若快速线上穿慢速线为买入信号；若快速线下穿慢速线为卖出信号
                                
                            if df.iat[(dflen - 1), 19] > df.iat[(dflen - 1), 18] and df.iat[(dflen - 2), 19] <= df.iat[
                                (dflen - 2), 18]:
                                        operate = operate + 10
                                 elif df.iat[(dflen - 1), 19] < df.iat[(dflen - 1), 18] and df.iat[(dflen - 2), 19] >=
                                                                                            df.iat[
                                                                                                (dflen - 2), 18]:
                                    operate = operate - 10      
                                return (df, operate)

                            def Output_Csv(df, Dist):

                                    TODAY = datetime.date.today()

                                CURRENTDAY = TODAY.strftime('%Y-%m-%d')
                                reload(sys)
                                sys.setdefaultencoding("gbk")
                                df.to_csv(Dist + CURRENTDAY + 'stock.csv', encoding='gbk')  # 选择保存   
                             
                            def Close_machine():

                                    o = "c:\\windows\\system32\\shutdown -s"  #########

                                os.system(o)  #########
                               

                            # 日志记录
                            def Write_Blog(strinput, Dist):

                                    TODAY = datetime.date.today()

                                CURRENTDAY = TODAY.strftime('%Y-%m-%d')
                                TIME = time.strftime("%H:%M:%S")
                                  # 写入本地文件
                                fp = open(Dist + 'blog.txt', 'a') 
                                fp.write(
                                '------------------------------\n' + CURRENTDAY + " " + TIME + " " + strinput + '  \n')
                                fp.close()
                                time.sleep(1)       

                            df = Get_Stock_List()
                            Dist = 'E:\\08 python\\Output\\'
                            df = Get_TA(df, Dist)
                            Output_Csv(df, Dist)
                            time.sleep(1) 
                            Close_machine()
