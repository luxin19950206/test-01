# -*- coding: UTF-8 -*-
"""
@author：日行小逻辑19950206
@usage：关于循环语句for的用法

"""

for letter in 'python':
    print (letter)

for letter in ['p', 'y', 't', 1, 2]:
    print(letter)

for letter in ('p', 'y', 't', 1, 2):
    print(letter)

'''
利用序列进行索引迭代
'''
list = ['p', 'y', 't', 3, 4]
print(len(list))
print(range(len(list)))
for i in range(len(list)):
    print(list[i])

'''
break语句
break语句在for/while循环中用来终止循环语句，即循环条件没有False条件或者序列还没被完全递归完，也会停止执行循环语句。
break是跳出整个循环

continue语句是跳出当前的循环
continue 语句用来告诉Python跳过当前循环的剩余语句，然后继续进行下一轮循环。

pass语句
pass是空语句，是为了保持程序结构的完整性。它不做任何事情，一般用做占位语句。
'''

# break例子
for x in 'python':
    if x is 'h':
        break
    print('current situation:', x)

var = 10
while var > 0:
    print('current situation:', var)
    var -= 1
    if var == 5:
        break
print('good bye')
print('-------')

# continue例子
for x in 'python':
    if x is 'h':
        continue
    print('current situation:', x)

var = 10
while var > 0:
    var -= 1
    if var == 5:
        continue
    print('current situation:', var)
print('good bye')
print('-------')

# pass例子
for letter in 'Python':
    if letter == 'h':
        pass
        print('这是 pass 块')
    print('current situation', letter)

print("good bye!")
