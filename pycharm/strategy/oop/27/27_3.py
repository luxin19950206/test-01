# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
p693
子类可以继承父类的任何属性和方法
若子类中定义与父类同名的方法或者属性会自动覆盖父类对应的方法或者属性
"""


class Super:  # 超类
    def method(self):
        print('in Super.method')


class Sub(Super):  # 实例从类中继承、类从超类中继承
    def method(self):
        print('starting Sub.method')
        Super.method(self)
        print('ending Sub.method')


x = Super()
x.method()  # in Super.method
y = Sub()
y.method()  # starting Sub.method, in Super.method, ending Sub.method
print('_____')
