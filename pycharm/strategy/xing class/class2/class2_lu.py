# -*- coding: utf-8 -*-
def get_data():
    '''
    读取股票数据，并将相关股票格式进行修正
    :return: 以dataframe格式的数据，index为code，name为名称
    '''
    import pandas as pd
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
        '000004.sz': '国农科技', }
    sf = pd.Series(stock_code_dict)
    code = []
    for stock in sf.index:
        a = str(stock[7:9]).upper() + str(stock[0:6])
        code.append(a)
    df = pd.DataFrame(sf, columns=['name'])
    df.index = code
    return df


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


def test(stocks_name, stocks_code):
    """
    :param stocks_name:
    :param stocks_code:
    :return:
    """
    for code, name in zip(stocks_code, stocks_name):  # 多变量的for循环
        try:
            back = buy_stock_or_not(name)
            print(code, back)
        except:
            print(code, '程序报错！')


if __name__ == '__main__':
    df = get_data()
    test(df['name'], df.index)
