import pandas as pd
from datetime import datetime,timedelta


def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive/RawData'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
file_name_time = r'确定定策划师,方案报价提交,婚期,尾款付清时间_截止2018-12-17.xlsx'


data_time = read_file(path,file_name_time)

data_time = data_time.drop(['酒店','worker_id'],axis =1)
data_time['尾款支付时间'].fillna('unpaid',inplace = True)
data_time['尾款支付金额'].fillna('unpaid',inplace = True)

date_timestamp = datetime.now() - timedelta(days=0)

DownPMT_Speed = (pd.to_datetime(data_time['首付款项支付时间']) - pd.to_datetime(data_time['方案报价提交时间'])) /pd.Timedelta(1, unit='d')
FinalPMT_Speed=[]
for i in range(0,len(data_time['尾款支付时间'])):
    if data_time['尾款支付时间'].loc[i] == 'unpaid':
        n = 'unpaid'
    else :
        n = (pd.to_datetime(data_time['尾款支付时间'].loc[i]) - pd.to_datetime(data_time['婚期'].loc[i])) /pd.Timedelta(1, unit='d')
    FinalPMT_Speed.append(n)
Speed_tb = pd.concat([data_time['wedding_id'],data_time['方案首付金额(元)'],pd.DataFrame(DownPMT_Speed),pd.DataFrame(FinalPMT_Speed)],axis =1 )
Speed_tb.columns = ['wedding_id','方案首付金额','首付速度','结尾款速度']
Speed_tb.to_excel('%s付款速度.xlsx'%path_output)

