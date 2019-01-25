import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

def get_range(df):
  med = df.median().values
  std = df.std().values
  range =[med+3*std,med-3*std]
  return range

def get_range1(df):
  up = df.quantile(0.75).values
  down = df.quantile(0.25).values
  std = df.std().values
  range =[up+1.5*std,down-1.5*std]
  return range

path = u'C:/Users/t430/Desktop/Incentive/RawData'
file_name = r'用户打分_婚礼信息(婚期,酒店,顾问)_订单金额_回单_截止2018-11-27.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)

df1 = data['预算价格下限(元)']
df2 = data['预算价格上限(元)']
X=pd.DataFrame(abs(df2 -df1))

new_table = pd.concat([df1,df2,X,X],axis = 1)
new_table.columns = ['预算价格下限(元)','预算价格上限(元)','Range','Budget']

for i in range(0,len(new_table['Budget'])-1):
    if new_table.iloc[i,2] > 8500:
       new_table.iloc[i,3] = max(new_table.iloc[i,0],new_table.iloc[i,1])
    else:
       new_table.iloc[i,3] = 0.5*(new_table.iloc[i,0]+new_table.iloc[i,1])

NewTable = pd.concat([data['婚礼id'],data['策划师名称'],new_table['Budget'],data['完成订单总金额']],axis =1 )

i = NewTable[(NewTable.Budget<1000)].index.tolist()
df_new = NewTable.drop(i)
T = pd.DataFrame(df_new['完成订单总金额']/df_new['Budget'])
T.columns = ['Ratio']

x3 = T[(T.Ratio > get_range1(T)[0][0])].index.tolist() #Index out of range
x4 = T[(T.Ratio < get_range1(T)[1][0])].index.tolist() #Index out of range

data_new = df_new.drop(x3)
data4 = data_new.drop(x4)
data4.index = range(0,len(data4['Budget']))
#print(len(data4['Budget']),data4)

name = 'Budget.xlsx'
data4.to_excel(u'%s%s'%(path_output,name))

