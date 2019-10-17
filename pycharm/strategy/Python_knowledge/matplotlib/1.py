# -*- coding: utf-8 -*-
"""
@author：横纵19950206
@usage：
不错的讲解网站
https://www.jianshu.com/p/78ba36dddad8
https://www.cnblogs.com/jasonzeng888/p/6256040.html
"""
import matplotlib.pyplot as plt
import numpy as np


# 创建sub画布来编写
def plotdemo():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)  # 在figure图表上增加多个子图
    # 接下来在子图上建立绘制点和线
    fig.suptitle('figure title demo', fontsize=14, fontweight='bold')
    """
    fontsize设置字体大小，默认12，可选参数 ['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']
    fontweight设置字体粗细，可选参数 ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
    fontstyle设置字体类型，可选参数[ 'normal' | 'italic' | 'oblique' ]，italic斜体，oblique倾斜
    verticalalignment设置水平对齐方式 ，可选参数 ： 'center' , 'top' , 'bottom' ,'baseline' 
    horizontalalignment设置垂直对齐方式，可选参数：left,right,center
    rotation(旋转角度)可选参数为:vertical,horizontal 也可以为数字
    alpha透明度，参数值0至1之间
    backgroundcolor标题背景颜色
    
    
    --------------------- 
    作者：开码牛 
    来源：CSDN 
    原文：https://blog.csdn.net/helunqu2017/article/details/78659490 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    """
    ax.set_title('axes title')
    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    x = np.arange(0, 6)
    y = x * x
    # 绘制第一张图，x,y需要在前期步骤中赋予一定的值，这步是为了在图形中导入相关的值
    ax.plot(x, y)
    # 绘制第二张图
    # ax.plot(y,x)

    # 选取图形中的某个点进行绘制,type是[],X代表横轴位置,Y代表纵轴位置
    plt.scatter([2],[4],s=10,color='red') # 这代表着对(2,4)这个坐标点进行标注，s代表size

    # 对(2,4)进行标注，下方代表着在(2.5,3.5)的位置标注(2,4)
    plt.annotate('(2,4)',xy=(2.5,3.5),fontsize=16)

    # 对某个点进行文字说明，1，2代表的是x，y，后面的'string'代表的是添加的文本
    plt.text(1, 2, 'string')
    """
    第一个参数是x轴坐标
    第二个参数是y轴坐标
    第三个参数是要显式的内容
    alpha 设置字体的透明度
    family 设置字体
    size 设置字体的大小
    style 设置字体的风格
    wight 字体的粗细
    bbox 给字体添加框，alpha 设置框体的透明度， facecolor 设置框体的颜色
    作者：有一种宿命叫无能为力 
    来源：CSDN 
    原文：https://blog.csdn.net/You_are_my_dream/article/details/53455256 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    """

    plt.show()

# 用主画布来画图
def plotdemo2():
    # 接下来在子图上建立绘制点和线
    plt.title('figure title demo', fontsize=14, fontweight='bold')
    """
    fontsize设置字体大小，默认12，可选参数 ['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']
    fontweight设置字体粗细，可选参数 ['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']
    fontstyle设置字体类型，可选参数[ 'normal' | 'italic' | 'oblique' ]，italic斜体，oblique倾斜
    verticalalignment设置水平对齐方式 ，可选参数 ： 'center' , 'top' , 'bottom' ,'baseline' 
    horizontalalignment设置垂直对齐方式，可选参数：left,right,center
    rotation(旋转角度)可选参数为:vertical,horizontal 也可以为数字
    alpha透明度，参数值0至1之间
    backgroundcolor标题背景颜色


    --------------------- 
    作者：开码牛 
    来源：CSDN 
    原文：https://blog.csdn.net/helunqu2017/article/details/78659490 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    """
    plt.title('axes title')
    plt.xlabel('x label')
    plt.ylabel('y label')
    x = np.arange(0, 6)
    y = x * x
    # 绘制第一张图，x,y需要在前期步骤中赋予一定的值，这步是为了在图形中导入相关的值
    plt.plot(x, y)
    # 绘制第二张图
    # ax.plot(y,x)

    # 选取图形中的某个点进行绘制,type是[],X代表横轴位置,Y代表纵轴位置
    plt.scatter([2], [4], s=10, color='red')  # 这代表着对(2,4)这个坐标点进行标注，s代表size

    # 对(2,4)进行标注，下方代表着在(2.5,3.5)的位置标注(2,4)
    plt.annotate('(2,4)', xy=(2.5, 3.5), fontsize=16)

    # 对某个点进行文字说明，1，2代表的是x，y，后面的'string'代表的是添加的文本
    plt.text(1, 2, 'string')
    """
    第一个参数是x轴坐标
    第二个参数是y轴坐标
    第三个参数是要显式的内容
    alpha 设置字体的透明度
    family 设置字体
    size 设置字体的大小
    style 设置字体的风格
    wight 字体的粗细
    bbox 给字体添加框，alpha 设置框体的透明度， facecolor 设置框体的颜色
    作者：有一种宿命叫无能为力 
    来源：CSDN 
    原文：https://blog.csdn.net/You_are_my_dream/article/details/53455256 
    版权声明：本文为博主原创文章，转载请附上博文链接！
    """

    plt.show()


plotdemo()
