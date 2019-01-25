import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive'
file_name = r'权重配比得分.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)

corr = pd.DataFrame(data.corr())
x = data['首付前出方案速度评分']
x1 = data['WAA']/10000
#x2 = x ** 2
df = pd.concat([x,x1],axis =1 )
#df.columns = ['比例尺寸还原','有效回单']

a = KMeans(n_clusters=5, random_state=0).fit(df)
L = a.labels_
L0 = [i for i,v in enumerate(L) if v==0]
L1 = [i for i,v in enumerate(L) if v==1]
L2 = [i for i,v in enumerate(L) if v==2]
L3 = [i for i,v in enumerate(L) if v==3]
L4 = [i for i,v in enumerate(L) if v==4]
L5 = [i for i,v in enumerate(L) if v==5]
L6 = [i for i,v in enumerate(L) if v==6]
print("The Cluster centers are :%s"%a.cluster_centers_)
print("The total distance is %s"%a.inertia_)
print("The number of elements in cluster 1 is %s"%np.sum(L==0))
print("The number of elements in cluster 2 is %s"%np.sum(L==1))
print("The number of elements in cluster 3 is %s"%np.sum(L==2))
print("The number of elements in cluster 4 is %s"%np.sum(L==3))
print("The number of elements in cluster 5 is %s"%np.sum(L==4))
print("The number of elements in cluster 6 is %s"%np.sum(L==5))
print("The number of elements in cluster 7 is %s"%np.sum(L==6))

L = pd.DataFrame(L)
Var = pd.concat([data['策划师名称'],df,L],axis =1)
Var.to_excel(u'%sLabel.xlsx'%path_output)
#print(data.columns)

#print(data.iloc[L3,:])
#print(corr)