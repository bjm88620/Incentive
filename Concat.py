import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
file_name = r'付款速度.xlsx'
file_name1 = '用户打分_婚礼信息(婚期,酒店,顾问)_订单金额_回单_截止2018-12-13.xlsx'

data = read_file(path_output,file_name)
data1 = read_file(path,file_name1)

data1 = data1.merge(data,left_on ='婚礼id' , right_on = 'wedding_id', how ='outer')
col = ['婚礼id','首付速度','结尾款速度']
data = data1.dropna()

df1 = data['预算价格下限(元)']
df2 = data['预算价格上限(元)']
X=pd.DataFrame(abs(df2 -df1))

new_table = pd.concat([df1,df2,X,X],axis = 1)
new_table.columns = ['预算价格下限(元)','预算价格上限(元)','Range','Budget']

for i in range(0,len(new_table['Budget'])-1):
    if new_table.iloc[i,2] > 9000:
       new_table.iloc[i,3] = max(new_table.iloc[i,0],new_table.iloc[i,1])
    else:
       new_table.iloc[i,3] = 0.5*(new_table.iloc[i,0]+new_table.iloc[i,1])

# data['Gender'] = data.sex.apply(lambda x: 1 if 'female' in x else 0)
# data['Age'] = data['年龄'].apply(lambda x: 1 if x>25 else 0)
# dummies_Gender = pd.get_dummies(data['Gender'],prefix='Gender',prefix_sep="")
# dummies_Age = pd.get_dummies(data['Age'],prefix='Age',prefix_sep="")
# dummies_combine = pd.concat([dummies_Gender,dummies_Age],axis= 1)
allinfo = pd.concat([new_table['Budget'],data],axis=1)

allinfo.to_excel('%sAllInfo.xlsx'%path_output)
print(allinfo[(allinfo['首付速度']>1)]['首付速度'].describe())
print(pd.DataFrame(allinfo[(allinfo['首付速度']>1)]['首付速度']).info())
