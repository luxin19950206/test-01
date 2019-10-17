# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
类变量又称静态变量
定义在类中且在函数体之外，通常不作为实例变量使用，类变量是在整个实例化对象中公用的
在类内部和外部，类变量都用"类名.类变量"的形势访问，在类内部，也可以用self.类变量来访问类变量，但此时它的
含义已经变了，实际上它已经成为了一个实例变量。在实例变量没有被重新赋值时，用self.类变量才能访问到正确的值。
简单点说就是实例变量会屏蔽掉类变量的值，就像局部变量屏蔽掉全局变量的值一样。所以一般情况下是不将类变量作为
实例变量使用的

实例变量又称非静态变量
定义在方法中的变量，用self绑定到实例上，只作用于当前实例的类
在类内部，实例变量用self.实例变量的形式访问；在类外部，用实例名.实例变量的形式访问，实例变量是绑定到一个
实例上的变量

实际上，实例变量就是一个用self修饰的变量，self将一个变量绑定到一个特定的实例上，这样它就属于这实例自己。
"""


class A(object):
    va = 10

    def foo(self):
        print(A.va)  # 10
        print(self.va)  # 10
        self.va = 40
        print(A.va)  # 10 当self.类变量被重新赋值时，它的值就发生类变化，但类变量的值不会随之变化
        print(self.va)  # 40
        A.va = 15
        print(A.va)  # 15
        print(self.va)  # 40


obj1 = A()
obj2 = A()
obj1.foo()
print(A.va)  # 15 类变量是所有实例共享的
print(obj1.va)  # 40
print(obj2.va)  # 15

# 实例变量则是以为self.开头,必须在实例化该类后使用
class Test(object):
    def __init__(self):
        self.a = "Hello world!"

    def test(self):
        # 在内部Test.a是不能访问类变量的
        print(self.a)


A = Test()
A.test()  # Hello world!

# 类变量定义在类的定义之后，实例化前后都可以使用
class Test(object):
    a = "Hello world!"

    def __init__(self): pass

    def test(self):
        # 在内部self.a和Test.a都可以访问实例变量
        print(self.a)
        print(Test.a)


print(Test.a)
A = Test()
A.test()
