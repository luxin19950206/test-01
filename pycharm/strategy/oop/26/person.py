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


if __name__ == '__main__':
    bob = Person('Bob Smith', 'def')
    sue = Person('Sue Jones', job='dev', pay=100000)
    print(bob.name, bob.job, bob.pay)
    print(sue.name, sue.job, sue.pay)
    print(bob.lastName(), sue.lastName())
    sue.giveRaise(.10)
    print(sue.pay)
