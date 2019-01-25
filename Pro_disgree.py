import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df



path = u'C:/Users/t430/Desktop/Incentive/RawData/2018-11-27 策划师 用户和专家 打分'
file_name = r'专家评审职业人上传照片的评分_数据_截止20181127.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)
data = data.loc[(data['评分人名称'] =='点点')|(data['评分人名称'] =='皮雳')|(data['评分人名称'] =='孙庆')]
df = pd.DataFrame(data[data['评分项类型 0=是否|1=10分制']==1])

df1 = pd.pivot_table(df,values = '分数',index = ['婚礼id','职业人名称'],columns= ['评分项名称'],aggfunc=np.mean)
df1 = df1.reset_index()
df1=df1.fillna(-999)

col_name = df.columns
list_name = col_name.tolist()
ditch1 = list_name.index('评分项类型 0=是否|1=10分制')
ditch2 = list_name.index('婚礼id')
ditch3 = list_name.index('职业人id')
col1 = col_name[:ditch1].tolist()
col2 = col_name[ditch1+1:ditch1+4].tolist()
col3 = col_name[ditch3:ditch2+1].tolist()
col = col3+col1+col2

df = df[col]

new_colname = df['评分项名称'].drop_duplicates()

df = pd.pivot_table(df,values = '分数',index = ['婚礼id','职业人名称','评分人名称'],columns= ['评分项名称'],aggfunc=np.mean)
df = df.reset_index()

df=df.fillna(-999)
weddingID = df['婚礼id'].tolist()

Var = []
for i in range(0,len(df['婚礼id'])):
  id = weddingID[i]
  new_df = df.loc[(df['婚礼id'] == id)].drop(['评分人名称','婚礼id','职业人名称'],1)


  a = KMeans(n_clusters=1, random_state=0).fit(new_df)
  #print(a.inertia_,a.cluster_centers_)
  Var.append(a.inertia_)
Var=pd.DataFrame(Var)
var_table = pd.concat([df['婚礼id'],Var],axis =1 )
var_table = var_table.drop_duplicates()
print(var_table)
#Var = pd.DataFrame(Var)
#var_table = pd.concat([df['婚礼id'],Var],axis = 1)
#var_table.columns = ['婚礼id','方差和']
#var_table = var_table.drop_duplicates()


var_table.to_excel(r'C:\\Users\\t430\\Desktop\\Incentive\\Output\\Pro_EuDis.xlsx')


#  print(dis)
 # Distance.append(dis)
 # Distance.append(n)
#print(max(Distance),min(Distance))
  #print(dis1+dis2)
  #print("The distance is %s"%dis)



#Dis = pd.DataFrame(Distance)
#tb = pd.concat([df['婚礼id'],df['职业人名称'],Dis],axis=1)
#tb = tb.drop_duplicates()
#print(tb.head())

#tb.to_excel(u'%sProScores_Distance.xlsx'%path_output)
