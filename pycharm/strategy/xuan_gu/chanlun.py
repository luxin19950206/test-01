# -*- coding: utf-8 -*-
# 第三方函数库
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import matplotlib.patches as patches
import talib


def get_k_series(security, start_date, end_date, n=30):
    #
    # 获取k线序列，默认为30分钟级别
    # 输入：n是级别，单位是分钟
    # 输出：pandas, k线序列
    one_min_data = get_price(
        security,
        start_date=start_date,
        end_date=end_date,
        frequency='1m',
        fields=['open', 'close', 'high', 'low']
    )
    n_min_data = pd.DataFrame()
    for i in range(n, len(one_min_data) + 1, n):
        interval = one_min_data[i - n:i]
        interval_open = interval.open[0]
        interval_high = max(interval.high)
        interval_low = min(interval.low)
        interval_k = pd.DataFrame(interval[-1:])  # 新建DataFrame，否则会报SettingWithCopyWarning
        interval_k.open = interval_open
        interval_k.high = interval_high
        interval_k.low = interval_low
        n_min_data = pd.concat([n_min_data, interval_k], axis=0)
    return n_min_data


def get_binary_positions(k_data):
    #
    # 计算k线序列的二分位值，所有k线的中间值
    # 输入：k线序列
    # 输出：list, k线序列对应的二分位值
    binary_positions = []
    for i in xrange(len(k_data)):
        temp_y = (k_data.high[i] + k_data.low[i]) / 2.0
        binary_positions.append(temp_y)
    return binary_positions


def adjust_by_cintainment(k_data):
    # 判断k线的包含关系，便于寻找顶分型和底分型
    # 输入：k线序列
    # 输出：adjusted_k_data, 处理后的k线序列
    trend = [0]
    adjusted_k_data = pd.DataFrame()
    temp_data = k_data[:1]
    for i in xrange(len(k_data)):

        is_equal = temp_data.high[-1] == k_data.high[i] and temp_data.low[-1] == k_data.low[i]  # 第1根等于第2根

        # 向右包含
        if temp_data.high[-1] >= k_data.high[i] and temp_data.low[-1] <= k_data.low[i] and not is_equal:
            if trend[-1] == -1:
                temp_data.high[-1] = k_data.high[i]
            else:
                temp_data.low[-1] = k_data.low[i]

        # 向左包含
        elif temp_data.high[-1] <= k_data.high[i] and temp_data.low[-1] >= k_data.low[i] and not is_equal:
            if trend[-1] == -1:
                temp_data.low[-1] = k_data.low[i]
            else:
                temp_data.high[-1] = k_data.high[i]

        elif is_equal:
            trend.append(0)

        elif temp_data.high[-1] > k_data.high[i] and temp_data.low[-1] > k_data.low[i]:
            trend.append(-1)
            temp_data = k_data[i:i + 1]

        elif temp_data.high[-1] < k_data.high[i] and temp_data.low[-1] < k_data.low[i]:
            trend.append(1)
            temp_data = k_data[i:i + 1]

        # 调整收盘价和开盘价
        if temp_data.open[-1] > temp_data.close[-1]:
            if temp_data.open[-1] > temp_data.high[-1]:
                temp_data.open[-1] = temp_data.high[-1]
            if temp_data.close[-1] < temp_data.low[-1]:
                temp_data.close[-1] = temp_data.low[-1]
        else:
            if temp_data.open[-1] < temp_data.low[-1]:
                temp_data.open[-1] = temp_data.low[-1]
            if temp_data.close[-1] > temp_data.high[-1]:
                temp_data.close[-1] = temp_data.high[-1]

        adjusted_data = k_data[i:i + 1]
        adjusted_data.open[-1] = temp_data.open[-1]
        adjusted_data.close[-1] = temp_data.close[-1]
        adjusted_data.high[-1] = temp_data.high[-1]
        adjusted_data.low[-1] = temp_data.low[-1]
        adjusted_k_data = pd.concat([adjusted_k_data, adjusted_data], axis=0)

    return adjusted_k_data


def get_fx(adjusted_k_data):

    # 寻找顶分型和底分型
    # 1）连续分型选择最极端值
    # 2）分型之间保证3根k线
    # 输入：调整后的k线序列
    # 输出：顶分型和底分型的位置

    temp_num = 0  # 上一个顶或底的位置
    temp_high = 0  # 上一个顶的high值
    temp_low = 0  # 上一个底的low值
    temp_type = 0  # 上一个记录位置的类型

    fx_type = []  # 记录分型点的类型，1为顶分型，-1为底分型
    fx_time = []  # 记录分型点的时间
    fx_plot = []  # 记录点的数值，为顶分型取high值，为底分型取low值
    fx_data = pd.DataFrame()  # 记录分型
    fx_offset = []

    # 加上线段起点
    fx_type.append(0)
    fx_offset.append(0)
    fx_time.append(adjusted_k_data.index[0].strftime("%Y-%m-%d %H:%M:%S"))
    fx_data = pd.concat([fx_data, adjusted_k_data[:1]], axis=0)
    fx_plot.append((adjusted_k_data.low[0] + adjusted_k_data.high[0]) / 2)

    i = 1
    while (i < len(adjusted_k_data) - 1):

        top = adjusted_k_data.high[i - 1] <= adjusted_k_data.high[i] \
              and adjusted_k_data.high[i] > adjusted_k_data.high[i + 1]  # 顶分型
        bottom = adjusted_k_data.low[i - 1] >= adjusted_k_data.low[i] \
                 and adjusted_k_data.low[i] < adjusted_k_data.low[i + 1]  # 底分型

        if top:
            if temp_type == 1:
                # 如果上一个分型为顶分型，则进行比较，选取高点更高的分型
                if adjusted_k_data.high[i] <= temp_high:
                    i += 1
                else:
                    temp_high = adjusted_k_data.high[i]
                    temp_low = adjusted_k_data.low[i]
                    temp_num = i
                    temp_type = 1
                    i += 2  # 两个分型之间至少有3根k线
            elif temp_type == -1:
                # 如果上一个分型为底分型，则记录上一个分型，用当前分型与后面的分型比较，选取同向更极端的分型
                if temp_low >= adjusted_k_data.high[i]:
                    # 如果上一个底分型的底比当前顶分型的顶高，则跳过当前顶分型。
                    i += 1
                else:
                    fx_type.append(-1)
                    fx_time.append(adjusted_k_data.index[temp_num].strftime("%Y-%m-%d %H:%M:%S"))
                    fx_data = pd.concat([fx_data, adjusted_k_data[temp_num:temp_num + 1]], axis=0)
                    fx_plot.append(temp_low)
                    fx_offset.append(temp_num)
                    temp_high = adjusted_k_data.high[i]
                    temp_low = adjusted_k_data.low[i]
                    temp_num = i
                    temp_type = 1
                    i += 2  # 两个分型之间至少有3根k线
            else:
                temp_high = adjusted_k_data.high[i]
                temp_low = adjusted_k_data.low[i]
                temp_num = i
                temp_type = 1
                i += 2

        elif bottom:
            if temp_type == -1:
                # 如果上一个分型为底分型，则进行比较，选取低点更低的分型
                if adjusted_k_data.low[i] >= temp_low:
                    i += 1
                else:
                    temp_low = adjusted_k_data.low[i]
                    temp_high = adjusted_k_data.high[i]
                    temp_num = i
                    temp_type = -1
                    i += 3
            elif temp_type == 1:
                # 如果上一个分型为顶分型，则记录上一个分型，用当前分型与后面的分型比较，选取同向更极端的分型
                if temp_high <= adjusted_k_data.low[i]:
                    # 如果上一个顶分型的底比当前底分型的底低，则跳过当前底分型。
                    i += 1
                else:
                    fx_type.append(1)
                    fx_time.append(adjusted_k_data.index[temp_num].strftime("%Y-%m-%d %H:%M:%S"))
                    fx_data = pd.concat([fx_data, adjusted_k_data[temp_num:temp_num + 1]], axis=0)
                    fx_plot.append(temp_high)
                    fx_offset.append(temp_num)
                    temp_low = adjusted_k_data.low[i]
                    temp_high = adjusted_k_data.high[i]
                    temp_num = i
                    temp_type = -1
                    i += 2
            else:
                temp_low = adjusted_k_data.low[i]
                temp_high = adjusted_k_data.high[i]
                temp_num = i
                temp_type = -1
                i += 2
        else:
            i += 1

    # 加上最后一个分型（上面的循环中最后的一个分型并未处理）
    if temp_type == -1:
        fx_type.append(-1)
        fx_time.append(adjusted_k_data.index[temp_num].strftime("%Y-%m-%d %H:%M:%S"))
        fx_data = pd.concat([fx_data, adjusted_k_data[temp_num:temp_num + 1]], axis=0)
        fx_plot.append(temp_low)
        fx_offset.append(temp_num)
    elif temp_type == 1:
        fx_type.append(1)
        fx_time.append(adjusted_k_data.index[temp_num].strftime("%Y-%m-%d %H:%M:%S"))
        fx_data = pd.concat([fx_data, adjusted_k_data[temp_num:temp_num + 1]], axis=0)
        fx_plot.append(temp_high)
        fx_offset.append(temp_num)

    # 加上线段终点
    fx_type.append(0)
    fx_offset.append(len(adjusted_k_data) - 1)
    fx_time.append(adjusted_k_data.index[-1].strftime("%Y-%m-%d %H:%M:%S"))
    fx_data = pd.concat([fx_data, adjusted_k_data[-1:]], axis=0)
    fx_plot.append((adjusted_k_data.low[-1] + adjusted_k_data.high[-1]) / 2)

    return fx_type, fx_time, fx_data, fx_plot, fx_offset


def get_pivot(fx_plot, fx_offset, fx_observe):
    #
    # 计算最近的中枢
    # 注意：一个中枢至少有三笔
    # fx_plot 笔的节点股价
    # fx_offset 笔的节点时间点（偏移）
    # fx_observe 所观测的分型点

    if fx_observe < 1:
        # 处理边界
        right_bound = 0
        left_bount = 0
        min_high = 0
        max_low = 0
        pivot_x_interval = [left_bount, right_bound]
        pivot_price_interval = [max_low, min_high]
        return pivot_x_interval, pivot_price_interval

    right_bound = (fx_offset[fx_observe] + fx_offset[fx_observe - 1]) / 2
    # 右边界是所观察分型的上一笔中位
    left_bount = 0
    min_high = 0
    max_low = 0

    if fx_plot[fx_observe] >= fx_plot[fx_observe - 1]:
        # 所观察分型的上一笔是往上的一笔
        min_high = fx_plot[fx_observe]
        max_low = fx_plot[fx_observe - 1]
    else:  # 所观察分型的上一笔是往下的一笔
        max_low = fx_plot[fx_observe]
        min_high = fx_plot[fx_observe - 1]

    i = fx_observe - 1
    cover = 0  # 记录走势的重叠区，至少为3才能画中枢
    while (i >= 1):
        if fx_plot[i] >= fx_plot[i - 1]:
            # 往上的一笔
            if fx_plot[i] < max_low or fx_plot[i - 1] > min_high:
                # 已经没有重叠区域了
                left_bount = (fx_offset[i] + fx_offset[i + 1]) / 2
                break
            else:
                # 有重叠区域
                # 计算更窄的中枢价格区间
                cover += 1
                min_high = min(fx_plot[i], min_high)
                max_low = max(fx_plot[i - 1], max_low)

        elif fx_plot[i] < fx_plot[i - 1]:
            # 往下的一笔
            if fx_plot[i] > min_high or fx_plot[i - 1] < max_low:
                # 已经没有重叠区域了
                left_bount = (fx_offset[i] + fx_offset[i + 1]) / 2
                break
            else:
                # 有重叠区域
                # 计算更窄的中枢价格区间
                cover += 3
                min_high = min(fx_plot[i - 1], min_high)
                max_low = max(fx_plot[i], max_low)
        i -= 1

    if cover < 3:
        # 不满足中枢定义
        right_bound = 0
        left_bount = 0
        min_high = 0
        max_low = 0

    pivot_x_interval = [left_bount, right_bound]
    pivot_price_interval = [max_low, min_high]
    return pivot_x_interval, pivot_price_interval


def plot_k_series(k_data):
    # 画k线
    num_of_ticks = len(k_data)
    fig, ax = plt.subplots(figsize=(num_of_ticks, 20))
    fig.subplots_adjust(bottom=0.2)
    dates = k_data.index
    # print dates
    ax.set_xticks(np.linspace(1, num_of_ticks, num_of_ticks))
    ax.set_xticklabels(list(dates))
    mpf.candlestick2(
        ax,
        list(k_data.open), list(k_data.close), list(k_data.high), list(k_data.low),
        width=0.6, colorup='r', colordown='b', alpha=0.75
    )
    plt.grid(True)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)
    return ax


def plot_lines(ax, fx_plot, fx_offset):
    # 绘制笔和线段
    # ax 绘图区域
    # fx_plot
    plt.plot(fx_offset, fx_plot, 'k', lw=1)
    plt.plot(fx_offset, fx_plot, 'o')


def plot_pivot(ax, pivot_date_interval, pivot_price_interval):
    #
    # 绘制中枢
    start_point = (pivot_date_interval[0], pivot_price_interval[0])
    width = pivot_date_interval[1] - pivot_date_interval[0]
    height = pivot_price_interval[1] - pivot_price_interval[0]
    ax.add_patch(
        patches.Rectangle(
            start_point,  # (x,y)
            width,  # width
            height,  # height
            linewidth=8,
            edgecolor='g',
            facecolor='none'
        )
    )
    return


def check_deviating(scode, fastperiod=11, slowperiod=26, signalperiod=9):
    #
    # 日线级别，计算昨天收盘是否发生顶或底背离，利用快慢线金、死叉判断
    # scode，证券代码
    # fastperiod，fastperiod，signalperiod：MACD参数，默认为11,26,9
    # 返回 dev_type, 0：没有背离，1：发生顶背离，-1：发生底背离

    rows = (fastperiod + slowperiod + signalperiod) * 5
    close = attribute_history(security=scode, count=rows, unit='1d', fields=['close']).dropna()
    dif, dea, macd = talib.MACD(close.values, fastperiod, slowperiod, signalperiod)

    if macd[-1] > 0 > macd[-2]:
        # 底背离
        # 昨天金叉
        # idx_gold: 各次金叉出现的位置
        idx_gold = np.where((macd[:-1] < 0) & (macd[1:] > 0))[0] + 1  # type: np.ndarray
        if len(idx_gold) > 1:
            if close[idx_gold[-1]] < close[idx_gold[-2]] and dif[idx_gold[-1]] > dif[idx_gold[-2]]:
                dev_type = -1

    elif macd[-1] < 0 < macd[-2]:
        # 顶背离
        # 昨天死叉
        # idx_dead: 各次死叉出现的位置
        idx_dead = np.where((macd[:-1] > 0) & (macd[1:] < 0))[0] + 1  # type: np.ndarray
        if len(idx_dead) > 1:
            if close[idx_dead[-1]] > close[idx_dead[-2]] and dif[idx_dead[-1]] < dif[idx_dead[-2]]:
                dev_type = 1
    else:
        # 不发生背离
        dev_type = 0

    return dev_type


start_date = datetime.datetime(2017, 11, 6, 9, 0, 0)
end_date = datetime.datetime(2017, 11, 10, 15, 30, 0)
k_series = get_k_series('000100.XSHE', start_date, end_date, 30)
plot_k_series(k_series)  # 原始k线图

adjusted_k_data = adjust_by_cintainment(k_series)
ax = plot_k_series(adjusted_k_data)  # 调整后的k线图

fx_type, fx_time, fx_data, fx_plot, fx_offset = get_fx(adjusted_k_data)
print fx_type, fx_time
plot_lines(ax, fx_plot, fx_offset)

pivot_x_interval, pivot_price_interval = get_pivot(fx_plot, fx_offset, len(fx_offset) - 2)
plot_pivot(ax, pivot_x_interval, pivot_price_interval)

