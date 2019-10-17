import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
# plot是matplot.pyplot中的特殊函数
# 导入图像的两三种方式
# 一：
plt.subplot(111)

# 二：
# 先创建figure，而后再figure中添加subplot
fig = plt.figure()
fig.add_subplot(111)

# 图像创建万后就是画线了，用到的最主要的方式就是plt.plot(x,y)

# 如果直接建立图像也是可能的。
x = DataFrame(np.random.randn(10, 4), columns=['a', 'b', 'c', 'd'], index=np.arange(0, 100, 10))
x.plot()
plt.show()