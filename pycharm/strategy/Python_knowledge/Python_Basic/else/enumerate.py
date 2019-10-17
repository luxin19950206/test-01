# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""
list = ['这', '是', '一个', '测试']
for i in range(len(list)):
    print(i, list[i])
"""
0 这
1 是
2 一个
3 测试
"""
print("--------")
for index, item in enumerate(list):
    print(index,item)
"""
0 这
1 是
2 一个
3 测试
"""
for index, item in enumerate(list,1):
    print(index,item)
"""
1 这
2 是
3 一个
4 测试

"""