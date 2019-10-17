# -*- coding: utf-8 -*-

import os
import pandas as pd  # 导入pandas，我们一般为pandas去一个别名叫做pd
import config

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import random
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score

# ===导入数据
df = pd.read_hdf(config.output_data_path + '/stock_data_h5.h5', 'stock_data')
print(df)
exit()
df = df[['交易日期', '股票代码', '总市值', '市盈率TTM', '下月涨幅']]
df.dropna(how='any', inplace=True)
df = df.sample(1000)
df.loc[df['下月涨幅'] >= 0, 'Y'] = 1
df['Y'].fillna(value=0, inplace=True)

# ===准备原始数据
x = df.loc[:, ['总市值', '市盈率TTM']].values
y = df.loc[:, 'Y'].values

# ===对原始数据进行预处理：归一化等
x = preprocessing.scale(x)

# ===挑选训练数据、测试数据
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=random.randint(0, 100))
print(x_train.shape)
print(x_test.shape)

# ===特征选择
# 一般此步骤会对特征进行处理。
# 比如把多个相关性比较高的特征进行组合。
# 将多维度降低为低纬度，PCA等方法

# ===GridSearch
pipeline = Pipeline([
    ('SVM', svm.SVC(kernel='rbf', class_weight='auto'))
])
parameters = {
    'SVM__gamma': [2 ** -15, 2 ** -13, 2 ** -11, 2 ** -9, 2 ** -7, 2 ** -5, 2 ** -3, 2 ** -1, 2 ** 1, 2 ** 3],
    'SVM__C': [2 ** -5, 2 ** -3, 2 ** -1, 2 ** 1, 2 ** 3, 2 ** 5, 2 ** 7, 2 ** 9, 2 ** 11, 2 ** 13, 2 ** 15]
}
# print '开始训练'
grid_search = GridSearchCV(pipeline, parameters, n_jobs=1, pre_dispatch='2*n_jobs')
grid_search.fit(x_train, y_train)
# print '结束训练'

# 对结果进行预测
y_pred = grid_search.predict(x_test)
# print y_test.shape
# print y_pred.shape
# 判断准确率
# print precision_score(y_test, y_pred, average='macro')
