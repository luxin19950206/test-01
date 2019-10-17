# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""


class Person:
    def __init__(self, name, job=None, pay=0):
        """
        constructor 构造函数
        :param name: 
        :param job: 
        :param pay: 
        :return: 
        """
        self.name = name
        self.job = job  # 通过self.job＝job把本地的变量复赋值给self.job属性
        self.pay = pay

    def lastName(self):
        return self.name.split()[-1]

    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

    def __str__(self):
        '''
        运算符重载
        每一次实例转换为其打印字符串的时候，__str__都会自动运行
        :return: 
        '''
        return '[Person: %s, %s]' % (self.name, self.pay)


# 直接复制贴贴giveRaise的方法会使得未来得维护工作倍增
# class Manager(Person):
#     def giveRaise(self, percent, bonus=.10):
#         self.pay=int(self.pay*(1+percent+bonus))

class Manager(Person):
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)


if __name__ == '__main__':
    bob = Person('Bob Smith', 'def')
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(bob)  # [Person: Bob Smith, 0]
    print(sue)  # [Person: Sue Jones, 100000]
    print(bob.lastName(), sue.lastName())
    sue.giveRaise(.10)
    print(sue)  # [Person: Sue Jones, 110000]
    tom = Manager('Tom Jones', 'doctor', 50000)
    tom.giveRaise(.10)
    print(tom)  # [Person: Tom Jones, 60000]
    print("--ALL THREE")
    for name in (bob, sue, tom):
        name.giveRaise(.10)
        print(name)