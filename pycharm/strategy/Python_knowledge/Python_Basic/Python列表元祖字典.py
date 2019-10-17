# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
Python变量类型描述
"""
'''列表相关特征：
1，list［］
2，允许更新以及修改
3，有序对象集合
'''
list = [1, 2, 3, 4]
list2 = ['x', 'i', 'n', 'l', 'u']
list[0] = 4
print(list)
'''
[4,2,3,4]
'''

'''元组相关特征：
1，tuple()
2，元组不能被2次负值，只能用于只读
'''
Tuple = (1, 2, 'x', 'i')
# Tuple[0] = 4，不被允许
print(Tuple)

'''字典相关特征
1，Dictionary{key:value}
2，无序的对象合集
'''
dict = {}
dict[1] = 'this is one'
dict['2'] = 'this is 2'
print(dict)
