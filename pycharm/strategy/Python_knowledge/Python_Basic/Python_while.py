# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
关于while循环语句中的continue，break，return等的相关用法及解释
关于for循环语句中
"""

'''continue'''
i = 1
while i < 10:
    i += 1
    if i % 2 > 0:  # 非双数时跳过
        print(i, i % 2)
        continue  # continue用于跳过该次循环
    print(i)

'''break'''
i = 1
while i:
    print(i)
    i += 1
    if i > 10:
        break  # break用于退出循环

'''return
return语句用于退出函数，通常不带参数的return语句返回的是None
'''
def reg(a, b):
    total = a + b
    return total


print(reg(1, 3))

print('--------')

def reg1(a, b):
    total = a + b
    print(total)
    return
print(reg1(1, 2))  # 这里print的时候就会出现none

reg1(1, 2)  # 得到3