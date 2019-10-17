# -*- coding: utf-8 -*-
"""
@author：日行小逻辑19950206
@usage：

"""
import re
regex=re.compile(r'\b\w{2}\b') # 匹配6个字符的单词
text=regex.search('My phone number is 421-2343-121')
print(text.group())

regex=re.compile(r'0\d{2}-\d{8}|0\d{3}-\d{7}')  # 注意分枝条件的使用
text=regex.search('My')
