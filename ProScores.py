import pandas as pd
import numpy as np

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData/2018-11-27 策划师 用户和专家 打分'
file_name = r'专家评审职业人上传照片的评分_数据_截止20181127.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)
data = data.loc[(data['评分人名称'] =='点点')|(data['评分人名称'] =='皮雳')|(data['评分人名称'] =='孙庆')]
df = pd.DataFrame(data[data['评分项类型 0=是否|1=10分制']==1])
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
#df = df.replace(nan,-99999,inplace=True)
df.to_excel(u'%sProScores_pivot.xlsx'%path_output)
#print(df.dropna(axis=1))

