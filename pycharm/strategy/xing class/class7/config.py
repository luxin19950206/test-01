# coding=utf-8
import os

# 获取当前程序的地址
current_file = __file__
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class/class7/config.py
"""

# 程序根目录地址，即程序上一级目录的地址
root_path = os.path.abspath(os.path.join(current_file, os.pardir))
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class/class7
"""

# 输入数据根目录地址，即程序上一级目录的地址加上后面的后缀
input_data_path = os.path.abspath(os.path.join(root_path, os.pardir, 'input_data'))
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class/input_data
"""

# 输出数据根目录地址
output_data_path = os.path.abspath(os.path.join(root_path, os.pardir, 'output_data'))
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class/output_data
"""

# # 当前路径
# print(os.path.abspath('.'))
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class/class7
"""

# # 父辈路径
# print(os.path.abspath('..'))
"""
/Users/ShiRuo/PycharmProjects/untitled2/xing_class
"""
