# -*- coding: utf-8 -*-
"""
lambda argument1, argument2,...argument N:expression using arguements
lambda表达式起到一个函数速写的功能
"""


def func(x, y, z): print(x + y + z)


func(2, 3, 4)

f = lambda x, y, z: x + y + z
print(f(2, 3, 4))
