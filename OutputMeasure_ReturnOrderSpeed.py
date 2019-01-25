import pandas as pd
import numpy as np
from datetime import datetime,timedelta

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
file_name = r'策划师用户打分&对应的有效回单累计数据_截止2018-12-17 13点53分.xlsx'
file_name1 = r'确定定策划师,方案报价提交,婚期,尾款付清时间_截止2018-12-17.xlsx'

data_raw = read_file(path,file_name)
data_time = read_file(path,file_name1)

data = data_raw.merge(data_time,left_on = 'wedding_id', right_on ='wedding_id' , how = 'inner')
data = data.dropna()
agent_name = data['策划师名称_x'].drop_duplicates().tolist()
l = ['wedding_id','策划师名称_x','婚期_x','尾款支付时间','累计有效回单数量']
df = data[l]
df = df.sort_values(by=['策划师名称_x','尾款支付时间'])
df.to_excel(u'C:/Users/t430/Desktop/Incentive/RawData/df.xlsx')
start_time = pd.DataFrame(df['尾款支付时间'])
end_time = pd.DataFrame(df['尾款支付时间']).shift(periods = -1)
end_time = pd.DataFrame(end_time.dropna())
start_time = start_time.iloc[0:len(end_time),0]
id = pd.DataFrame(df['wedding_id'])
num_order = pd.DataFrame(df['累计有效回单数量'])
num_shift = num_order.shift(periods = -1)
name = pd.DataFrame(df['策划师名称_x'])
name_shift = name.shift(periods = -1)
name = name.iloc[0:len(end_time),0]
xbg = pd.concat([id,name,name_shift,start_time,end_time,num_order,num_shift],axis =1)

xbg.columns = ['id','n1','n2','t1','t2','num1','num2']
xbg = xbg.reset_index()
xbg = xbg.drop('index',axis =1)
#xbg.to_excel(r'C:\Users\t430\Desktop\Incentive\RawData\xbg.xlsx')
td = []
od = []
for i in range(0,len(xbg)):
  if xbg['n1'].loc[i] == xbg['n2'].loc[i]:
    n = (pd.to_datetime(xbg['t2'].loc[i]) - pd.to_datetime(xbg['t1'].loc[i]))/pd.Timedelta(1, unit='d')
    m = xbg['num2'].loc[i]-xbg['num1'].loc[i]
  else :
    m = 'NA'
    n = 'NA'

  td.append(n)
  od.append(m)
fxbg = pd.concat([xbg,pd.DataFrame(td),pd.DataFrame(od)],axis = 1)

fxbg.columns = ['id','n1','n2','t1','t2','num1','num2','td','od']

#fxbg.to_excel(u'C:/Users/t430/Desktop/Incentive/RawData/FXBG.xlsx')


#tb_speed.to_excel(u'C:/Users/t430/Desktop/Incentive/RawData/TotalInfo.xlsx')

