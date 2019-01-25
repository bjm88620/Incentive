import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from sklearn.cluster import KMeans

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
file_name = r'用户打分_婚礼信息(婚期,酒店,顾问)_订单金额_回单_截止2018-12-13.xlsx'
#file_name1 = '.xlsx'

data = read_file(path,file_name)

col_name = data.columns
list_name = col_name.tolist()
ditch1 = list_name.index('完成订单总金额')
ditch2 = list_name.index('策划师名称')
ditch3 = list_name.index('首付前满意度评分')
ditch4 = list_name.index('尾款前整体打分')
col1 = col_name[ditch4:(ditch4+6)].tolist() #locate final payment elements
col2 = col_name[ditch3:(ditch3+2)].tolist() #locate down payment elements
col3 = col_name[ditch2:(ditch2+1)].tolist()
col4 = col_name[ditch1:ditch1+1].tolist()
col =col3+col2+col1+col4

df = pd.pivot_table(data,values='完成订单总金额',index = ['策划师名称'],aggfunc=np.sum)
df = df.reset_index()
df.columns = ['策划师','Profit']


tb =data[col].merge(df, left_on='策划师名称', right_on='策划师', how='outer')
tb['占比'] = tb['完成订单总金额']/tb['Profit']
cl_name = ['首付前满意度评分_Ave','首付前出方案速度评分_Ave',
           '尾款前整体打分_Ave', '尾款前服务意识分数_Ave',
           '尾款前审美能力分数_Ave','尾款前效果还原度分数_Ave',
           '尾款前控制预算分数_Ave', '尾款前形象气质分数_Ave']
for i in range(len(cl_name)):
  tb[cl_name[i]] = tb.iloc[:,i+1] * tb['占比']
#tb.to_excel('%sT.xlsx'%path_output)
df = pd.concat([tb['策划师名称'],tb.iloc[:,-8:]],axis =1)
col = df.columns.tolist()
df1 = pd.pivot_table(df,index = '策划师名称',values = col[1 :],aggfunc = np.sum)
df1.reset_index()
df1.to_excel('%sClientScore_WAA.xlsx'%path_output)

df2 = data[['策划师名称','有效回单数']].drop_duplicates()
df2.columns = ['策划师','有效回单数']
#df2 = read_file(path,file_name1)
tabel_waa_order = df1.merge(df2,left_on = '策划师名称',right_on='策划师',how = 'outer')
tabel_waa_order.to_excel('%sClientScore_Order.xlsx'%path_output)
a = tabel_waa_order.drop(['策划师'],axis=1)

for i in range(len(a.columns)):
    col_list = a.columns.tolist()
    n = col_list[i]
    sub_a = pd.concat([a[n],a['有效回单数']],axis =1 )
    clf = KMeans(n_clusters=7, random_state=0).fit(sub_a)
    L = clf.labels_
    element_count = []
    for j in range(0,7):
        taimanle = np.sum(L==j)
        element_count.append(taimanle)
    tb = pd.concat([tabel_waa_order['策划师'],sub_a,pd.DataFrame(L)],axis =1 )
    tb.to_excel('%sLabel_%s.xlsx'%(path_output,n))
    CC = clf.cluster_centers_
    CC = pd.DataFrame(CC)
    CC1 = pd.DataFrame({'Group':[0,1,2,3,4,5,6]})
    CC = pd.concat([CC,CC1,pd.DataFrame(element_count)],axis =1)
    CC.columns =[n,'有效回单','簇标签','元素个数']
    CC.to_excel('%sClusterCenters_%s.xlsx'%(path_output,n))


