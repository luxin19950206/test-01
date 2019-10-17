# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""
X = 11  # 模块属性


def f():
    print(X)


def g():
    X = 22  # 模块内的本地变量
    print(X)


class C:
    X = 33  # 类属性

    def m(self):
        X = 44  # 方法中的本地变量
        self.X = 55  # 实例属性


if __name__ == '__main__':
    print(X)  # 11
    f()  # 11
    g()  # 22
    print(X)  # 11
    obj = C()  # 创建实例
    print(obj.X)  # 33
    obj.m()
    print(obj.X)  # 55
    print(C.X)  # 33
    # print(C.m.X)  报错
    # print(g.X)  报错
