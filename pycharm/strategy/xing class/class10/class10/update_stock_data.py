# coding=utf-8
import pandas as pd
import config
import numpy as np
import Functions
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# 神奇的链接http://hq.sinajs.cn/list=sh600000

# 本程序的作用是，从新浪网上，将所有股票最新的数据抓取下来并且保存。
# 可以每天定期运行，然后就能得到每天的数据了。

# 总体的思路

# ===读取所有股票代码列表
s_list = pd.read_hdf(config.input_data_path + '/base/stock_code_list_store.h5', 'table')
all_code_list = list(s_list)

# ===20个一组遍历股票
chunk_len = 50
for code_list in np.array_split(all_code_list, len(all_code_list) / chunk_len + 1):
    Functions.save_stock_data_from_sina_to_h5(code_list)

# ===从h5文件中中读取数据
code = 'sh600000'
df = pd.read_hdf(config.output_data_path + '/all_stock_data_h5.h5', code)
