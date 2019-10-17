# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：小甲鱼课程第38课
"""
import random as r


class Fish:
    def __init__(self):
        self.x = r.randint(0, 10)
        self.y = r.randint(0, 10)

    def move(self):
        self.x -= 1
        print("我的位置是：", self.x, self.y)


class Goldfish(Fish):
    pass


class Garp(Fish):
    pass


class Shark(Fish):
    def __init__(self):
        # Fish.__init__(self)  # 调用基类的方法
        super(Shark, self).__init__()
        """
        super(Shark, self)首先找到Shark的父类(即类Fish)，然后把类Shark的对象转换为
        类Fish的对象，
        
        """
        self.hungry = True

    def eat(self):
        if self.hungry:
            print("吃货的梦想就是天天有的吃")
            self.hungry = False
        else:
            print('太撑了，吃不下了')


# 多重继承
class Base1:
    def fool(self):
        print("我是foo1")


class Base2:
    def foo2(self):
        print("我是foo2")


class C(Base1, Base2):
    pass


if __name__ == "__main__":
    fish = Fish()
    fish.move()
    goldfish = Goldfish()
    goldfish.move()
    shark = Shark()
    shark.eat()
    shark.eat()
    shark.move()

    c = C()
    c.foo1()
    c.foo2()  # 多重继承尽可能不用，容易导致混乱
