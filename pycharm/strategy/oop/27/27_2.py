# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
p690
"""


class NextClass():
    def printer(self, text):
        self.message = text
        print(self.message)


x = NextClass()  # 创建实例
x.printer('instance call')
print(x.message)

y=NextClass()
NextClass.printer(y, 'class call')
print(y.message)

