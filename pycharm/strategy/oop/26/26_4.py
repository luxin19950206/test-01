# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
"""
from classtools import AttrDisplay


class Person(AttrDisplay):
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


class Manager(Person):
    def __init__(self):
        Person.__init__(self, name, 'mgr', pay)

    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus)
