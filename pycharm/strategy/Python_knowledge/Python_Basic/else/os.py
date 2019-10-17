# -*- coding: UTF-8 -*-
import os

"""
os.walk(top, topdown=True, onerror=None, followlinks=False)
top:
    需要遍历的目录树的路径, 产生3个tupple
    dirpath:目录／文件夹路径,
    dirnames:dirpath下所有文件夹的名字,
    filenames:所有文件名（包括path文件夹下相关文件夹下的文件名字）
topdown--默认”True”
    表示首先返回目录树下的文件，然后再遍历目录树的子目录.
    为”False”时，表示先遍历目录树的子目录，返回子目录下的文件，最后返回根目录下的文件
onerror--默认”None”
    表示忽略文件遍历时产生的错误.如果不为空，则提供一个自定义函数提示错误信息后继续遍历或抛出异常中止遍历
"""

for root, dirs, files in os.walk("/Users/ShiRuo/PycharmProjects/untitled2/group"):
    print(root)  # 文件夹
    """
    /Users/ShiRuo/PycharmProjects/untitled2/group
    /Users/ShiRuo/PycharmProjects/untitled2/group/123
    """
    print('-------')
    print(dirs)  # root下所有的文件夹名字
    """
    ['123']
    []
    """
    print('-------')
    print(files)  # root下所有的文件名字，包括相关文件夹下的文件名
    """
    ['.DS_Store', '__init__.py', 'group_act.py', 'sz300424.csv', 'sz300425.csv', 'sz300426.csv', 'sz300427.csv', 'sz300428.csv', 'sz300429.csv', 'sz300430.csv', 'sz300431.csv', 'sz300432.csv', 'sz300433.csv']
    ['__init__.py']
    """
    print('-------')
    for name in files:
        print(os.path.join(root, name))  # 打印文件名
    """
    /Users/ShiRuo/PycharmProjects/untitled2/group/.DS_Store
    /Users/ShiRuo/PycharmProjects/untitled2/group/__init__.py
    /Users/ShiRuo/PycharmProjects/untitled2/group/group_act.py
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300424.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300425.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300426.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300427.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300428.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300429.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300430.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300431.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300432.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/sz300433.csv
    /Users/ShiRuo/PycharmProjects/untitled2/group/123/__init__.py
    """
    for name in dirs:
        print(os.path.join(root, name))  # 打印文件夹名
    """
    /Users/ShiRuo/PycharmProjects/untitled2/group/123
    """

stock_list = []
# 系统自带函数os.walk，用于遍历文件夹中的所有文件
for root, dirs, files in os.walk('/Users/ShiRuo/PycharmProjects/untitled2/group'):
    # root输出文件夹，dirs输出root下所有的文件夹，files输出root下的所有的文件
    print(root, dirs, files)
    if files:  # 当files不为空的时候
        for f in files:
            if f.endswith('.csv'):
                stock_list.append(f[:8])
                # stock_list.append(os.path.join(root, f))
