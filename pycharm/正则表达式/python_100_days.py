# -*- coding: utf-8 -*-
"""
@author：日行小逻辑19950206
@usage：

"""
import re


def main():
    username = input('请输入用户名：')
    qq = input('请输入QQ号:')
    # match函数的第一个参数是正则表达式字符串或者正则表达式对象
    # 第二个参数是要跟正则表达式做匹配的字符串对象
    m1 = re.match(r'^[0-9a-zA-Z]{6,20}$', username)
    if not m1:
        print('请输入有效的用户名。')
    m2 = re.match(r'^[1-9]\d{4,11}$', qq)
    if not m2:
        print('请输入有效的QQ号。')
    if m1 and m2:
        print('你输入的信息是有效的！')


if __name__ == "__main__":
    main()