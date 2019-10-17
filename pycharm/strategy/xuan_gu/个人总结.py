# 1文档保存路径
import tushare as ts
df = ts.get_sina_dd('600848', date='2016-8-16') #默认400手
m=df.to_excel('/Users/ShiRuo/Documents/Tushare')

# 3类、实例
class Person(object):
    def __init__(self, name): #跟在self后面的name是变量
        self.name = name
        self._title = 'Mr' #这里的这个是定量
        self.__job = 'Student'
p = Person('Bob')
print(p.name)
=> Bob
print(p._title)
=> Mr

# 4Python列表操作的函数和方法
# 列表操作包含以下函数:
# 1、cmp(list1, list2)：比较两个列表的元素
# 2、len(list)：列表元素个数
# 3、max(list)：返回列表元素最大值
# 4、min(list)：返回列表元素最小值
# 5、list(seq)：将元组转换为列表

# 列表操作包含以下方法:
# 1、list.append(obj)：在列表末尾添加新的对象
# 2、list.count(obj)：统计某个元素在列表中出现的次数
# 3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
# 4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
# 5、list.insert(index, obj)：将对象插入列表
# 6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# 7、list.remove(obj)：移除列表中某个值的第一个匹配项
# 8、list.reverse()：反向列表中元素
# 9、list.sort([func])：对原列表进行排序

# list:有序的集合,可以随时添加或者删除其中的元素,其中len()表示list元素的个数
# tuple:元组,一旦初始化就不能改变
# dict:python中内置的字典,使用key-value储存,具有极快的查找速度
# set是一组key的集合,但不储存,set可以看成是数学上的无序的和无重复元素的集合

# python3中饿input输出的是str格式,如果想得到int格式的话需要用xx=int(input())

# int:取整函数
# %r:rper()
# %s:str()

# 各种指标回测的意义：
# 基准收益:大盘的收益率
# 策略收益:个人制定的策略回测后的收益
# Alpha:阿尔法：（策略年华收益－无风险收益）－beta＊（基准年华收益率－无风险收益），阿尔法越高代表超额风险额度收益越大
# Beta：贝塔，投资的系统风险系数，Beta越高，代表相对于大盘的系统风险越高
# Max Drawdown：最大回撤，描述策略可能出现的最糟糕的情况，见图
# Sharpe Ratio：夏普比率，每承受一单位总风险，会产生多少的超额回报酬；夏普比率越高，相当于每承担一份风险获得的收益越高

# 函数：
# abs：取绝对值  eg：abs（－20）＝20
# cmp：比较函数
# int：数据换为整数  eg：int（12.34）＝12
# str：将其他数据类型换为str  eg：str（123）＝‘123’
# type()：type就是指出指定对象的类型  ；eg：a = 'ABC'  >>> type(a)  >>><type 'str'

# XSHG是上交所，XSHE是深交所

# 定义参数时例如def(x,n)中作为必选参数在前,而n作为默认参数在后,同时默认参数可以考虑传入具体的数字,如下
# 如何设置默认参数?当函数有多个参数时,把变化大的参数放前面,比那话小的参数放后面,变化小的参数可以作为默认参数。
# 函数体内部的语句在执行时,一旦执行到return时,函数就执行完毕,并将结果返回,因此,函数内部通过条件判断和循环可以实现非常复杂的逻辑。
# 如果没有return语句,函数执行完毕也会返回结果,只是结果为None
def power(x,n=3):
    s=1
    while n>0:
        n=n-1
        s=s*x
    return s
print(power(5))

def power(x,n):
    s=1
    while n>0:
        n=n-1
        s=s*x
    return s
print(power(5,3))

D = {'a': 1, 'c': 3, 'b':2}
m = list(D.keys())
m.sort()
for key in m:
    print(key,'=>',D[key])

for key in sorted(D):
    print(key, '=>', D[key])

a=[1,3,5,6,2,4]
a.sort()
print(a)

m=[]
for c in [1,2,3,4]:
    m.append(c*2)
print(m)

import os
os.getcwd() ＃能够获取当前文件的文件位置