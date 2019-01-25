import pandas as pd

def orderspeed():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
    client_score = client_score.dropna()
    client_score = client_score.reset_index()
    od_l = ['婚礼id','策划师名称','回单日期','累计有效回单数量']
    shift_l = ['策划师名称','回单日期','累计有效回单数量']
    dd_l = ['策划师名称','累计有效回单数量']
    dd_tb = client_score[dd_l].drop_duplicates()
    dd_tb = client_score.loc[dd_tb.index,]


    ros_tb = client_score[od_l].sort_values(by=['策划师名称','回单日期'])
    #t2 = ros_tb[shift_l].shift(periods = -1)
    t2 = dd_tb[shift_l].shift(periods = -1)
    adj_tb = pd.concat([dd_tb[od_l],t2],axis = 1).reset_index()
    adj_tb.columns = ['index','婚礼id','n1','t1','o1','n2','t2','o2']
    Time_diff = []
    Order_diff = []
    Speed = []
    for i in range(len(adj_tb['n1'])):
        if adj_tb['n1'].loc[i] == adj_tb['n2'].loc[i]:
            n = adj_tb['o2'].loc[i] - adj_tb['o1'].loc[i]
            t = (pd.to_datetime(adj_tb['t2'].loc[i]) - pd.to_datetime(adj_tb['t1'].loc[i]))/pd.Timedelta(1, unit='d')
            speed = t/n
        else:
            speed = t = n ='N.a.'
        Time_diff.append(t)
        Order_diff.append(n)
        Speed.append(speed)
    Cal_tb = pd.concat([adj_tb,pd.DataFrame(Time_diff),pd.DataFrame(Order_diff),pd.DataFrame(Speed)],axis = 1 )
    Cal_tb.columns = adj_tb.columns.tolist()+['Time_diff','Order_diff','Turnover_Speed']
    Cal_tb = Cal_tb[(Cal_tb['Order_diff']!='N.a.')]
    Cal_tb.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Cal.xlsx')
    L1 = ['婚礼id','Turnover_Speed']
    return Cal_tb[L1]

def orderdelta():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
    client_score = client_score.dropna()
    client_score = client_score.reset_index()
    od_l = ['婚礼id','策划师名称','回单日期','累计有效回单数量']
    shift_l = ['策划师名称','回单日期','累计有效回单数量']
    dd_l = ['策划师名称','累计有效回单数量']
    #dd_tb = client_score[dd_l] #.drop_duplicates()
    #dd_tb = client_score.loc[dd_tb.index,]


    ros_tb = client_score[od_l].sort_values(by=['策划师名称','回单日期'])
    #t2 = ros_tb[shift_l].shift(periods = -1)
    t2 = client_score[shift_l].shift(periods = -1)
    adj_tb = pd.concat([client_score[od_l],t2],axis = 1).reset_index()
    adj_tb.columns = ['index','婚礼id','n1','t1','o1','n2','t2','o2']
    Time_diff = []
    Order_diff = []
    Speed = []
    for i in range(len(adj_tb['n1'])):
        if adj_tb['n1'].loc[i] == adj_tb['n2'].loc[i]:
            n = adj_tb['o2'].loc[i] - adj_tb['o1'].loc[i]
            t = (pd.to_datetime(adj_tb['t2'].loc[i]) - pd.to_datetime(adj_tb['t1'].loc[i]))/pd.Timedelta(1, unit='d')
            speed = t/n
        else:
            speed = t = n ='N.a.'
        Time_diff.append(t)
        Order_diff.append(n)
        Speed.append(speed)
    Cal_tb = pd.concat([adj_tb,pd.DataFrame(Time_diff),pd.DataFrame(Order_diff),pd.DataFrame(Speed)],axis = 1 )
    Cal_tb.columns = adj_tb.columns.tolist()+['Time_diff','Order_diff','Turnover_Speed']
    Cal_tb = Cal_tb[(Cal_tb['Order_diff']!='N.a.')]
    Cal_tb.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Cal.xlsx')
    L1 = ['婚礼id','Order_diff']
    return Cal_tb[L1]

def getrange(df):
    med = df.median().values
    std = df.std().values
    range1 = ([med + 3 * std, med - 3 * std],med + 6*std)
    up = df.quantile(0.75).values
    down = df.quantile(0.25).values
    std = df.std().values
    range2 = ([up + 1.5 * std, down - 1.5 * std],up-down+3*std)
    if range1[1] > range2[1]:
        range = range1[0]
    else:
        range = range2[0]
    return range

def pro():
    import pymssql as ps
    import pandas as pd
    import numpy as np
    conn = ps.connect(host='121.42.61.195', user='test', password='tes@t123456#pwd2018&', charset='utf8')

    query = ("""SELECT c.name as 职业人名称, a.worker_user_id as 职业人id,a.user_wedding_id as 婚礼id
    ,a.operator_name as 评分人名称,b.tag as 评分项名称,b.measure_type as 评分项类型 ,
    (case when (b.measure_type = 0 and b.score = 1) then '是'
           when (b.measure_type = 0 and b.score = 0) then '否'
      else convert (varchar(10),b.score) end) as '分数' FROM
     [izhaowoDataCenter].[dbo].[tb_worker_scene_tag] a
      left join [izhaowoDataCenter].[dbo].[tb_worker_scene_tag_item] b
      on a.id = b.scene_tag_id
      left join [izhaowoDataCenter].[dbo].[tb_worker] c
      on a.worker_user_id = c.user_id
       inner join (
      SELECT id,wedding_date FROM [izhaowoDataCenter].[dbo].[tb_user_wedding] where
    broker_id NOT IN ( 'e7ed2c90-dc48-4595-a1bf-3725be1b1a68',
                       '70a0d230-2b6a-4f32-8afc-a4379bbfca41',
                       '864a6295-828b-4e22-9989-bfc2962efc4d',
                       'aada4b53-d257-453f-848a-27869bad753a',
                       'b411ec25-c2d2-11e7-864b-7cd30ab79bd4',
                       'bc4a7dc9-a1c6-460c-b370-ec3ab7d871a9')
      ) d on a.user_wedding_id = d.id
    order by worker_user_id,user_wedding_id,operator_id,scene_tag_id,tag_id;""")

    pro_score = pd.read_sql(query, con=conn)
    pro_score.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score.xlsx')
    pro_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score.xlsx')
    pro_score = pro_score.dropna()
    pro_score = pro_score[(pro_score['评分项类型'] == 1)]
    pro_score['分数'] = pro_score.分数.apply(lambda x: int(x))
    pro_score.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score1.xlsx')
    pro_ave = pd.pivot_table(pro_score, index='婚礼id', columns='评分项名称', values='分数', aggfunc=np.mean)
    pro_ave = pro_ave.dropna(axis=1)
    pro_ave.reset_index()
    pro_ave.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_ave.xlsx')
    return pro_ave

def client():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
    client_score = client_score.dropna()
    L1 = ['婚礼id', '策划师名称', '策划师id', '首付前满意度评分', '首付前出方案速度评分', '尾款前整体打分', '尾款前服务意识分数',
          '尾款前审美能力分数', '尾款前效果还原度分数', '尾款前控制预算分数', '尾款前形象气质分数']
    client_score = client_score[L1]
    return client_score

def orderdiff():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
    client_score = client_score.dropna()
    client_score = client_score.reset_index()
    od_l = ['婚礼id', '策划师名称', '回单日期', '累计有效回单数量']
    shift_l = ['策划师名称', '回单日期', '累计有效回单数量']
    dd_l = ['策划师名称', '累计有效回单数量']
    # dd_tb = client_score[dd_l] #.drop_duplicates()
    # dd_tb = client_score.loc[dd_tb.index,]

    ros_tb = client_score[od_l].sort_values(by=['策划师名称', '回单日期'])
    t2 = ros_tb[shift_l].shift(periods = -1)
    #t2 = client_score[shift_l].shift(periods=-1)
    adj_tb = pd.concat([ros_tb[od_l], t2], axis=1).reset_index()
    adj_tb.columns = ['index', '婚礼id', 'n1', 't1', 'o1', 'n2', 't2', 'o2']
    Time_diff = []
    Order_diff = []
    Speed = []
    for i in range(len(adj_tb['n1'])):
        if adj_tb['n1'].loc[i] == adj_tb['n2'].loc[i]:
            n = adj_tb['o2'].loc[i] - adj_tb['o1'].loc[i]
            t = (pd.to_datetime(adj_tb['t2'].loc[i]) - pd.to_datetime(adj_tb['t1'].loc[i])) / pd.Timedelta(1, unit='d')
            speed = t / n
        else:
            speed = t = n = 'N.a.'
        Time_diff.append(t)
        Order_diff.append(n)
        Speed.append(speed)
    Cal_tb = pd.concat([adj_tb, pd.DataFrame(Time_diff), pd.DataFrame(Order_diff), pd.DataFrame(Speed)], axis=1)
    Cal_tb.columns = adj_tb.columns.tolist() + ['Time_diff', 'Order_diff', 'Turnover_Speed']
    Cal_tb = Cal_tb[(Cal_tb['Order_diff'] != 'N.a.')]
    Cal_tb.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Cal.xlsx')
    L1 = ['婚礼id', 'Order_diff']

    return Cal_tb[L1]