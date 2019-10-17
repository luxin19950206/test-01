# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""
import random as r


# P632
class Firstclass:
    def setdata(self, value):
        self.data = value

    def display(self):
        print(self.data)


x = Firstclass()
y = Firstclass()
x.setdata('King Arthur')  # self指的就是X, self.data =x.data= value =King Arthur
y.setdata('3.1415')
x.display()  # king Arthur
y.display()  # 3.1415
x.data = "new value"  # x指的就是self
x.display()  # new value
print('____')


# p635
class Secondclass(Firstclass):
    def display(self):
        print('Current value=%s' % self.data)


z = Secondclass()
z.setdata(42)
z.display()  # Current value=42


# p639
class Thirdclass(Secondclass):
    def __init__(self, value):
        '''
        constructor 构造函数
        :param value: 
        '''
        self.data = value

    def __add__(self, other):
        return Thirdclass(self.data + other)

    def __str__(self):
        return '[Thirdclass: %s]' % self.data

    def mul(self, other):
        self.data *= other


a = Thirdclass('abc')  # value=self.data='abc'
print(a.display())  # Current value=abc


# p690
class NextClass:
    def printer(self, text):
        self.message = text
        print(self.message)


x = NextClass()
x.printer(3)  # 3 instance.method(args...)
print(x.message)  # 3
NextClass.printer(x, 3)  # 3 class.method(instance, args...)
# NextClass.printer(3) 会报错
print('_____')


# 继承
# 案例1
class Fish():
    def __init__(self):
        self.x = r.randint(0, 10)
        self.y = r.randint(0, 10)

    def move(self):
        self.x -= 1
        print('hhh:', self.x, self.y)


class Shark(Fish):
    def __init__(self):
        # 子类有同样名称的方法会覆盖父类中的方法，例如这里的init初始化方法,处理这个可以调用未绑定的父类方法
        Fish.__init__(self)
        # 第二种可以使用super函数，即Super.__init__(self)
        # Super.__init__(self),super函数的特殊之处在于不用给定任何父类的名字，系统会自动找出一层层的方法，如果要改，只需要改class()内的
        self.hungry = True

    def eat(self):
        if self.hungry:
            print('吃货的梦想就是fuck')
            self.hungry = False
        else:
            print('TM')


shark = Shark()
shark.move()  # 从而能够导致输出的结果为hhh:3,4


# 案例2
class Super:
    def __init__(self, x):
        pass


class Sub(Super):
    def __init__(self, x, y):
        Super.__init__(self, x)
        pass


# 方法名不要和类变量名一样，要用不同词性的名字命名，例如方法用v，属性要n
class C:
    def x(self):
        print('x-man')


c = C()
c.x()  # x-man
# c.x=1
# c.x()  #这里会得到错误提示
