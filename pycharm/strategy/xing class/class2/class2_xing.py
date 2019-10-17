# -*- coding: UTF-8 -*

# 注意：函数参数为股票名，在引用函数时需要调用dict中的股票名字
def buy_stock_or_not(stock_name):
    """
    此程序用于决定某个股票是否购买。运行期间程序有50%的概率报错。
    """
    import random
    random = random.random()
    if random >= 0.75:
        return '买入' + stock_name
    elif random >= 0.5:
        return '不买入' + stock_name
    else:
        raise ValueError('程序报错！')

# dict 的key为股票代码，value为股票名字
stock_code_dict = {
    '600000.sh': '浦发银行',
    '600004.sh': '白云机场',
    '000005.sz': '世纪星源',
    '000006.sz': '深振业Ａ',
    '600005.sh': '武钢股份',
    '600006.sh': '东风汽车',
    '600007.sh': '中国国贸',
    '000001.sz': '平安银行',
    '000002.sz': '万科Ａ',
    '000004.sz': '国农科技',
}

# 调用股票代码并且定义为一个list
stock_key = list(stock_code_dict.keys())
# 对股票代码进行转化：小写转大写字母&字母在前
new_sort_key = [key.split('.')[1].upper()+key.split('.')[0] for key in stock_key]
# 对转换后的股票代码进行排序。如果先排序再进行转化，那么SZ会在SH之前，不符合最后的输出要求
new_sort_key.sort()

for temp_key in new_sort_key:
    try:
        print(temp_key + ' ' + buy_stock_or_not(stock_code_dict[key]))
    except:
        print(temp_key + ' ' + '程序报错！')
