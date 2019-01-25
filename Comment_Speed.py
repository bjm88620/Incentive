import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
file_name = r'Comment_Increment.xlsx'
data = read_file(path,file_name)
data = data.sort_values(by=['wedding_date','ctime'])

data_star = pd.pivot_table(data,values = 'star',index ='wedding_id',aggfunc = np.mean)
data_len= pd.pivot_table(data,values='content_length',index = ['wedding_id'],aggfunc=np.sum)
data_star.reset_index()
data_len.reset_index()
wdt = pd.concat([data['wedding_id'],data['wedding_date']],axis = 1)
wdt = wdt.drop_duplicates()
df = wdt.merge(data_len,left_on ='wedding_id',right_on = 'wedding_id',how = 'outer')
df = df.merge(data_star,left_on ='wedding_id',right_on='wedding_id',how = 'outer')

dft=pd.to_datetime(df['wedding_date'], format='%Y.%m.%d')
dft1 = dft.drop([0])
test = df['wedding_date'].shift(periods=-1, freq=None, axis=0)
time_diff = (pd.to_datetime(test) - pd.to_datetime(df['wedding_date']))/pd.Timedelta(1, unit='d')
time_diff = pd.DataFrame(time_diff)
time_diff.columns = ['time_diff']
tb = pd.concat([df,time_diff],axis = 1)
tb.to_excel('%sComm_Speed.xlsx'%path_output)
Kmeans_tb = tb.drop(['wedding_id','wedding_date'],axis =1)
cor_matrix = tb.corr()


clf = KMeans(n_clusters=3, random_state=0).fit(Kmeans_tb)
L = clf.labels_
print("The Cluster centers are :%s"%clf.cluster_centers_)

#######################################################################################
# import pandas as pd
# import numpy as np
# from sklearn.cluster import KMeans
#
# data = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\Output\Comm_Speed.xlsx')
# Kmeans_tb = data.drop(['wedding_id','wedding_date','star'],axis =1)
#
# clf = KMeans(n_clusters=9, random_state=0).fit(Kmeans_tb)
# L = clf.labels_
# element_count = []
# for j in range(0, 5):
#     taimanle = np.sum(L == j)
#     element_count.append(taimanle)
# CC = clf.cluster_centers_
# CC = pd.DataFrame(CC)
# CC1 = pd.DataFrame({'Group': [0, 1, 2, 3, 4, 5, 6,7,8]})
# CC = pd.concat([CC, CC1, pd.DataFrame(element_count)], axis=1)
# print(CC)
