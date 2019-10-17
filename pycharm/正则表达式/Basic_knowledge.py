# -*- coding: utf-8 -*-
"""
@author：日行小逻辑19950206
@usage：
正则表达式是一个特殊的字符系列，它能够帮助你方便地检查一个字符串是否与某种模式匹配
"""
"""
NO 1
re.match
尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回None
re.match(pattern,string,flags=0)
pattern:匹配的正则表达式
string:要匹配的字符串
"""
import re

print(re.match('www', 'www.runoob.com').span())
print(re.match('com', 'www.runoob.com'))

line = 'Cats are smarter than dogs'
match0bj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
if match0bj:
    print("match0bj.group():", match0bj.group())
    print("match0bj.group(1):", match0bj.group(1))
    print("match0bj.group(2):", match0bj.group(2))
else:
    print("no match!!")
"""
r'(.*) are (.*?) .*'
r表示字符串转换为非转译的原始字符串，让编译器忽略反斜杠
（.*)第一个匹配分组，.*代表匹配除换行符之外的所有字符
（.*?)第二个匹配分组，.*?后面多个？代表非贪婪模式，也就是说只能匹配符合条件的最少字符
.*没有括号包围，所以不是分组，匹配效果和第一个一样，但是不计入匹配结果中
match0jb.group()等同于match0bj.group(0)表示匹配到的完整文本字符
match0bj.group(1)得到第一组匹配结果，也就是(.*)匹配到的
match0bj.group(2)得到第二组匹配结果，也就是(.*?)匹配到的
"""
"""
NO 2
re.search扫描整个字符串并返回第一个成功的匹配
re.search(pattern,string,flags=0)
"""
print(re.search('www', 'www.runoob.com').span())
print(re.search('www', 'www.runoob..com').span())

search0bj = re.search(r'(.*) are (.*?) .*', line, re.M | re.I)
if search0bj:
    print("search0bj.group():", search0bj.group())
    print("search0bj.group(1):", search0bj.group(1))
    print("search0bj.group(2):", search0bj.group(2))
"""
NO 3
re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None
而re.search匹配整个字符串，直到找到一个匹配。
"""
match0bj2 = re.match(r"dogs", line, re.M | re.I)
if match0bj2:
    print("match-->match0bj.group():", match0bj.group())
else:
    print('No match!!')

search0bj2 = re.search(r'dogs', line, re.M | re.I)
if search0bj2:
    print("search-->search0bj2():", search0bj2.group())
else:
    print("No match!!")

"""
NO 4
检索和替换
Python的re模块提供了re.sub用于替换字符串中的匹配项
re.sub(pattern,repl,string,count=0,flags=0)
pattern:正则中的模式字符串
repl:替换的字符串，也可为一个函数
string:要被查找替换的原始字符串
count：模式匹配后替换的最大次数，默认0表示替换所以的匹配
"""
phone = "2004-959-559  # 这是一个国外电话号码"
num = re.sub(r'#.*$', "", phone)
print("电话号码是:", num)

num = re.sub(r'\D', "", phone)
print("电话号码是:", num)
