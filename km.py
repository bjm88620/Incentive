import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
file_name = r'策划师用户打分_个人信息_婚礼信息_订单金额_回单数据_截止2018-11-14.xlsx'
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

df = pd.concat([data['婚礼id'],data['策划师名称'],new_table['Budget'],data['完成订单总金额']],axis =1 )
X = pd.concat([df['Budget'],df['完成订单总金额']],axis =1)
a = KMeans(n_clusters=7, random_state=0).fit(X)
L = a.labels_
L0 = [i for i,v in enumerate(L) if v==0]
L1 = [i for i,v in enumerate(L) if v==1]
L2 = [i for i,v in enumerate(L) if v==2]
L3 = [i for i,v in enumerate(L) if v==3]
L4 = [i for i,v in enumerate(L) if v==4]
L5 = [i for i,v in enumerate(L) if v==5]
L6 = [i for i,v in enumerate(L) if v==6]
#AgentName = pd.DataFrame(df['婚礼id'])

#df.loc[L0,['婚礼id','策划师名称','尾款前整体打分']].to_excel(u'%s/L0.xlsx'%path_output)
#df.loc[L1,['婚礼id','策划师名称','尾款前整体打分']].to_excel(u'%s/L1.xlsx'%path_output)
#df.loc[L2,['婚礼id','策划师名称','尾款前整体打分']].to_excel(u'%s/L2.xlsx'%path_output)
print("The Cluster centers are :%s"%a.cluster_centers_)
print("The total distance is %s"%a.inertia_)
print("The number of elements in cluster 1 is %s"%np.sum(L==0))
print("The number of elements in cluster 2 is %s"%np.sum(L==1))
print("The number of elements in cluster 3 is %s"%np.sum(L==2))
print("The number of elements in cluster 4 is %s"%np.sum(L==3))
print("The number of elements in cluster 5 is %s"%np.sum(L==4))
print("The number of elements in cluster 6 is %s"%np.sum(L==5))
print("The number of elements in cluster 7 is %s"%np.sum(L==6))
