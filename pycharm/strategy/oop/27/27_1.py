# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
p688
"""


class SharedData:
    spam = 2


x = SharedData()
y = SharedData()
print(x.spam, y.spam)  # 2 2
SharedData.spam = 3
print(x.spam, y.spam)  # 3 3
x.spam = 2
print(x.spam, y.spam, SharedData.spam)  # 2 3 3


class MixedNames:
    data = 'spam'

    def __init__(self, value):
        self.data = value  # 将def括号中的value赋值给self.data

    def display(self):
        print(self.data, MixedNames.data)


x = MixedNames(1)  # 1代表init构造函数中的value，
y = MixedNames(2)  # x,y代表self, 方法的第一个参数总数接收调用的隐形主体，也就是实例对象
x.display()  # 1 spam, instance.method(args...)会自动翻译成class.method(instance, args)
MixedNames.display(x)  # 1 spam
"""
即调用可以采用两种方式：instance.method(arg) 或者 class.method(instance,arg) 
"""
y.display()  # 2 spam
print(x.data)  # 输出x.data为1
print(MixedNames.data)  # spam
print('______')
