
# coding: utf-8

# In[10]:

get_ipython().magic(u'matplotlib inline')
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import tushare as ts
import statsmodels.api as sm
import seaborn as sns


# In[34]:

def find_cointegrated_pairs(dataframe):
    # 得到DataFrame长度
    n = dataframe.shape[1]
    # 初始化p值矩阵
    pvalue_matrix = np.ones((n, n))
    # 抽取列的名称
    keys = dataframe.keys()
    # 初始化强协整组
    pairs = []
    # 对于每一个i
    for i in range(n):
        # 对于大于i的j
        for j in range(i+1, n):
            # 获取相应的两只股票的价格Series
            stock1 = dataframe[keys[i]]
            stock2 = dataframe[keys[j]]
            # 分析它们的协整关系
            result = sm.tsa.stattools.coint(stock1, stock2)
            # 取出并记录p值
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            # 如果p值小于0.05
            if pvalue < 0.08:
                # 记录股票对和相应的p值
                pairs.append((keys[i], keys[j], pvalue))
    # 返回结果
    return pvalue_matrix, pairs


# In[35]:

#list = ['601988','600016','601169','601398','601939','601818','600036','600015','601166']


# In[42]:

list =['601988','600016','601169','601997','600926','601818','600919','600000','601288','601128','600908','601328','601398','600036','601939','600015','601166','601009','601229']


# In[43]:

df = ts.get_k_data(list[0])[['date','close']].set_index('date')
df.columns=[list[0]]
for i in list[1:]:
    ds =ts.get_k_data(i)[['date','close']].set_index('date')
    ds.columns=[i]
    df=df.merge(ds,right_index=True,left_index=True)


# In[44]:

pvalues, pairs = find_cointegrated_pairs(df)


# In[45]:

df1=pd.DataFrame(pairs,columns=['stock1','stock2','pvalues'])


# In[46]:

df1.sort_values(by='pvalues').head(5)


# In[14]:

sns.heatmap(1-pvalues, xticklabels=list, yticklabels=list, cmap='RdYlGn_r', mask = (pvalues == 1))


# In[53]:

stock_sample1 = df['601988']
stock_sample2 = df['601328']
x = stock_sample1
y = stock_sample2
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())


# In[54]:

diff=y-1.8470*x
mean=np.mean(diff)
std=np.std(diff)
print(std)
up=mean+std
down=mean-std
time=diff.index
mean_line=pd.Series(mean,index=time)
up_line=pd.Series(up,index=time)
down_line=pd.Series(down,index=time)
set=pd.concat([diff,mean_line,up_line,down_line],axis=1)
set.plot(figsize=(10,5))


# In[47]:

stock_sample1 = df['601169']
stock_sample2 = df['600000']
x = stock_sample1
y = stock_sample2
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())


# In[48]:

diff=y-1.6996*x
mean=np.mean(diff)
std=np.std(diff)
print(std)
up=mean+std
down=mean-std
time=diff.index
mean_line=pd.Series(mean,index=time)
up_line=pd.Series(up,index=time)
down_line=pd.Series(down,index=time)
set=pd.concat([diff,mean_line,up_line,down_line],axis=1)
set.plot(figsize=(10,5))


# In[50]:

stock_sample1 = df['600926']
stock_sample2 = df['600919']
x = stock_sample1
y = stock_sample2
X = sm.add_constant(x)
result = (sm.OLS(y,X)).fit()
print(result.summary())


# In[51]:

diff=y-0.2534*x
mean=np.mean(diff)
std=np.std(diff)
print(std)
up=mean+std
down=mean-std
time=diff.index
mean_line=pd.Series(mean,index=time)
up_line=pd.Series(up,index=time)
down_line=pd.Series(down,index=time)
set=pd.concat([diff,mean_line,up_line,down_line],axis=1)
set.plot(figsize=(10,5))

