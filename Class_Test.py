import pandas as pd
from datetime import datetime,timedelta

def ReturnOrderSpeed(path,filename):

    #path = u'C:/Users/t430/Desktop/Incentive/RawData'
    #file_name = r'策划师用户打分&对应的有效回单累计数据_截止2018-12-17 13点53分.xlsx'

    file_name1 = r'确定定策划师,方案报价提交,婚期,尾款付清时间_截止2018-12-17.xlsx'


    data_raw =  pd.read_excel(u'%s/%s'%(path,filename))
    data_time = pd.read_excel(u'%s/%s'%(path,file_name1))

    data = data_raw.merge(data_time,left_on = 'wedding_id', right_on ='wedding_id' , how = 'inner')
    data = data.dropna()
    agent_name = data['策划师名称_x'].drop_duplicates().tolist()
    l = ['策划师名称_x','婚期_x','尾款支付时间','累计有效回单数量']
    df = data[l]
    df = df.sort_values(by=['策划师名称_x','尾款支付时间'])
    start_time = pd.DataFrame(df['尾款支付时间'])
    end_time = pd.DataFrame(df['尾款支付时间']).shift(periods = -1)
    end_time = pd.DataFrame(end_time.dropna())
    start_time = start_time.iloc[0:len(end_time),0]
    name = pd.DataFrame(df['策划师名称_x'])
    name_shift = name.shift(periods = -1)
    name = name.iloc[0:len(end_time),0]
    xbg = pd.concat([name,name_shift,start_time,end_time],axis =1)
    xbg.columns = ['n1','n2','t1','t2']
    xbg = xbg.reset_index()
    xbg = xbg.drop('index',axis =1)
    #xbg.to_excel(r'C:\Users\t430\Desktop\Incentive\RawData\xbg.xlsx')
    td = []
    for i in range(0,len(xbg)):
      if xbg['n1'].loc[i] == xbg['n2'].loc[i]:
        n = (pd.to_datetime(xbg['t2'].loc[i]) - pd.to_datetime(xbg['t1'].loc[i]))/pd.Timedelta(1, unit='d')
      else :
        n = 'NA'
      td.append(n)

    fxbg = pd.concat([xbg,pd.DataFrame(td)],axis = 1)

    fxbg.columns = ['n1','n2','t1','t2','td']

    fxbg.to_excel(u'C:/Users/t430/Desktop/Incentive/RawData/FXBG.xlsx')

    tb_speed = pd.concat([data_raw,pd.DataFrame(fxbg['td'])],axis = 1)

    tb_speed.to_excel(u'C:/Users/t430/Desktop/Incentive/RawData/TotalInfo.xlsx')

    return tb_speed

