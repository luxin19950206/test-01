# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：讲述下划线的作用
"""

"""
object  #public
__object__  # special,python system use, user should not define it
    对python而言有特殊的含义，对于普通的变量应当避免这种风格
    常见的比如__init__()代表的类的构造函数
_object  # obey python coding convention, consider it as private 
    _object被看作是私有的，在模块或类外不可以使用，不能用from module import* 导入
    单下划线开始的成员叫做保护变量，意思是只有类对象和子类对象自己能访问到这个数据
__object  # private(name mangling during runtime)
    双下划线开始的是私有成员，意思是只有类对象自己能访问，连子类对象也不能访问到这个数据
"""


class Foo():
    def __init__(self):
        pass

    def public_method(self):
        print('this is public method')

    def __fullprivate_method(self):
        print('This is double underscore leading method')

    def _halfprivate_method(self):
        print('This is one undersocre leading method')


if __name__ == "__main__":
    f = Foo()
    f.public_method()
    f._halfprivate_method  # 使用单下划线类,子类对象能够访问这个属性
    #  f.__fullprivate_method  # error 使用双下划线，子类对象也不能够访问
    f._Foo__fullprivate_method()  # 可以采用_class__object()的方法访问
    # f._Foo_halfprivate_method()  # error
