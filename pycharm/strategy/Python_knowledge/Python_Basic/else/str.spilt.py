import pandas as pd

"""
str.split(str="",num=string.count(str))[n]
拆分字符串，通过指定分隔符对字符串进行切片，并返回分割后的字符串列表（list）

str：分隔符，默认为空格，若字符串中没有分隔符，则把整个字符串作为列表的一个元素
num：分割次数，
n：取第几个变量

"""

code = '600000.sh.浦发银行'
print(code.split())  # 若字符串中没有分隔符，则把整个字符串作为列表的一个元素
# ['600000.sh.浦发银行']
print(code.split('.'))  # 以.为分隔符
# ['600000', 'sh', '浦发银行']
print(code.split('.', 0))  # 以.为分隔符，分割0次
# ['600000.sh.浦发银行']
print(code.split('.', 1))  # 以.为分隔符，分割1次
# ['600000', 'sh.浦发银行']
print(code.split('.', 2))  # 以.为分隔符，分割2次
# ['600000', 'sh', '浦发银行']
print(code.split('.', 2)[0])  # 以.为分隔符，分割2次，并且取第一个
print(type(code.split('.', 2)[0]))  # 字符串格式
# 600000
print(code.split('.', -1))  # 分割最多次
# ['600000', 'sh', '浦发银行']
u1, u2, u3 = code.split('.', 2)
print(u1, u2, u3)  # 分割两次，并把分割后的三个部分保存到三个文件
# 600000 sh 浦发银行
print(code.split('.'))

df = pd.read_csv('sz000002.csv', skiprows=1)
print(df['新浪概念'].str.split(';'))  # 切片后返回分割后的字符串列表
print(df['新浪概念'].str.split(';', expand=True))  # 该操作将数据分割后并且将数据分列
print(df['新浪概念'].str.split(';', expand=True)[1])

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

stock_key = list(stock_code_dict.keys())
new_sort_key = [key.split('.')[1].upper() + key.split('.')[0] for key in stock_key]
print(stock_key)
