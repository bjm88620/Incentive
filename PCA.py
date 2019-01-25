from sklearn.decomposition import pca
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive'
file_name = r'变量提取.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)

data =  data.as_matrix()

#data = data.values #得到values的ndarry
data = np.array(data) #直接原样转换，加上索引值


model = pca.PCA(n_components=3).fit(data)
Z = pd.DataFrame(model.transform(data))
Ureduce = model.components_
Z.to_excel(u'%sPCA_result.xlsx'%path_output)
#print(Ureduce)
#print(data.iloc[:,0])