# -*- coding: utf-8 -*-
'''
random.random()
随机生成0-1的随机浮点数0<=n<1

random.uniform(a,b)
随机生成一个指定范围内的随机浮点数，两个参数其中一个是上限，一个是下限
如果a>b，则生成的随机数n：a<=n<=b
如果a<b，则b<=n<=a

random.randint(a,b)
生成一个指定范围内的整数，其中参数a是下限，生成的随机数n:a<=n<=b
'''

import random

print(random.random())
print(random.uniform(10, 20))
print(random.randint(10, 20))
