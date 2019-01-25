import pandas as pd
import pymssql as ps
import numpy as np
import os,time,fnmatch,datetime
date_now = int(round(time.time() * 1000))
date_saved = "_" + time.strftime('%y%m%d', time.localtime(date_now / 1000))
mypath = r'C:\Users\t430\Desktop\Incentive\SQL'

def sqlextract():
    conn = ps.connect(host='121.42.61.195', user='test', password='tes@t123456#pwd2018&', charset='utf8')

    query = ("""SELECT [婚期],[酒店],[付款阶段],[顾问],[策划师],[策划师所在省]
                          ,[策划师所在市区县],[婚礼ID],[执行人员],[迎宾区],[仪式区],[灯光舞美]
                          ,[其它],[交通费],[婚礼人员] FROM [TOPN].[dbo].[婚礼方案报价明细数据表];""")

    query1 = ('SELECT [worker_name],[worker_id],[wedding_id],[方案首付金额(元)],[定策划师的时间],[方案报价提交时间]'
              ',[首付时间],[婚期],[尾款支付时间],[尾款支付金额],DATEDIFF(minute,[定策划师的时间],[尾款支付时间]) OverallSpeed,'
              'DATEDIFF(minute,[方案报价提交时间],[首付时间]) DownPMT_diff,'
              'DATEDIFF(minute,[定策划师的时间],[方案报价提交时间]) PlanSpeed,'
              'DATEDIFF(minute,[婚期],[尾款支付时间]) FinalPMT_diff FROM [TOPN].[dbo].[婚礼进程各阶段关键节点时间表] order by [婚期] asc;')

    query2 = ("""SELECT c.name as 职业人名称, c.id as 职业人id,a.user_wedding_id as 婚礼id
            ,a.operator_name as 评分人名称,b.tag as 评分项名称,b.measure_type as 评分项类型 ,
            (case when (b.measure_type = 0 and b.score = 1) then '是' when (b.measure_type = 0 and b.score = 0) then '否'
            else convert (varchar(10),b.score) end) as '分数' FROM [izhaowoDataCenter].[dbo].[tb_worker_scene_tag] a
            left join [izhaowoDataCenter].[dbo].[tb_worker_scene_tag_item] b on a.id = b.scene_tag_id
            left join [izhaowoDataCenter].[dbo].[tb_worker] c on a.worker_user_id = c.user_id
            inner join (SELECT id,wedding_date FROM [izhaowoDataCenter].[dbo].[tb_user_wedding] where
            broker_id NOT IN ( 'e7ed2c90-dc48-4595-a1bf-3725be1b1a68','70a0d230-2b6a-4f32-8afc-a4379bbfca41',
            '864a6295-828b-4e22-9989-bfc2962efc4d','aada4b53-d257-453f-848a-27869bad753a','b411ec25-c2d2-11e7-864b-7cd30ab79bd4',
            'bc4a7dc9-a1c6-460c-b370-ec3ab7d871a9')) d on a.user_wedding_id = d.id order by worker_user_id,user_wedding_id,operator_id,scene_tag_id,tag_id;""")

    query3 = ('SELECT [策划师名称],[worker_id]策划师id,[wedding_id]婚礼id,[婚期],[预算价格下限(元)]'
             ',[预算价格上限(元)],[完成订单总金额],[首付前满意度评分],[首付前出方案速度评分]'
             ',[尾款前整体打分],[尾款前服务意识分数],[尾款前审美能力分数],[尾款前效果还原度分数]'
             ',[尾款前控制预算分数],[尾款前形象气质分数],[首付前评价时间],[尾款前评价时间],[回单日期],[累计有效回单数量]'
             'FROM [TOPN].[dbo].[婚礼策划尾款前评分_策划师有效回单累计数据表] order by worker_id , 尾款前评价时间;')

    query4 = ("""select user_wedding_id 婚礼id, province_name,city_name 城市, 
                 case when province_name = '四川省' then 0
                 when province_name = '重庆市' then 1
                 when province_name = '江西省' then 2 end as 省份
                 from [tb_user_wedding_location]
                 where   (province_id IN ('7e60f6ed-4b54-4c80-8142-fcb5500320cf', 
                 '108a332c-d514-4d5c-960b-2da3f5c9f66f', '2f927671-449b-4807-80ff-32a5b623277f'))""")

    query5 = ("""select a.creator_id 策划师id,a.name 策划师名称,count(distinct a.number) 婚礼案例总数 from 
                (select t.id , t.number , t.creator_id,t1.name  from  tb_case t inner join (   
                 select id 策划师id,name from tb_worker where name not like '%测试%') t1 
                on t.creator_id  = t1.策划师id where t.[examine_status] = 1 AND t.[status] = 0) a
                inner join (select x.case_id,x.wedding_id,x.wedding_date from
                (select case_id,wedding_id,wedding_date from  tb_wedding_case
                where  wedding_date >= '2018-01-01') x inner join (
                SELECT id as wedding_id,wedding_date FROM dbo.tb_user_wedding 
                WHERE (status NOT IN (4, 5)) AND (broker_id NOT IN (
                'e7ed2c90-dc48-4595-a1bf-3725be1b1a68','70a0d230-2b6a-4f32-8afc-a4379bbfca41', 
                '864a6295-828b-4e22-9989-bfc2962efc4d', 'aada4b53-d257-453f-848a-27869bad753a', 
                'b411ec25-c2d2-11e7-864b-7cd30ab79bd4', 'bc4a7dc9-a1c6-460c-b370-ec3ab7d871a9'))) c on x.wedding_id = c.wedding_id) b 
                on a.id = b.case_id group by a.creator_id,a.name order by [婚礼案例总数]  desc;""")

    query6 = ("""select h.*,j.主页6个案例最高价,j.主页6个案例最低价,j.主页6个案例均价
                ,k.案例总数,k.所有案例最高价,k.所有案例最低价,k.所有案例均价 from
                (select id 策划师id, name 策划师,[浏览量],[评论数] from [TOPN].[dbo].[策划师浏览量和评论数]) h left join
                (SELECT t.worker_id,CAST((MAX(t.price) / 100) AS DECIMAL (10 , 2 )) AS [主页6个案例最高价],
                CAST((MIN(t.price) / 100) AS DECIMAL (10 , 2 )) AS [主页6个案例最低价],
                CAST((AVG(t.price) / 100) AS DECIMAL (10 , 2 )) AS [主页6个案例均价]
                from (select case_id,worker_id,worker_name,sort_time,ctime,wedding_id,price from (
                select case_id,worker_id,worker_name,sort_time,ctime,wedding_id,price
                ,row_number() over (partition by worker_id order by sort_time desc,ctime desc) as rn
                from [TOPN].[dbo].[策划师展示案例明细]) x where (x.rn between 2 and 7 )) t group by  t.worker_id
                ) j on h.策划师id = j.worker_id left join ( SELECT t.worker_id, COUNT(DISTINCT t.case_id) AS 案例总数,
                CAST((MAX(t.price) / 100) AS DECIMAL (10 , 2 )) AS 所有案例最高价, CAST((MIN(t.price) / 100) AS DECIMAL (10 , 2 )) AS 所有案例最低价,
                CAST((AVG(t.price) / 100) AS DECIMAL (10 , 2 )) AS 所有案例均价
                from  ( select case_id,worker_id,worker_name,sort_time,ctime,wedding_id,price
                from [TOPN].[dbo].[策划师展示案例明细] ) t group by t.worker_id ) k  on h.策划师id = k.worker_id
                order by k.案例总数 desc ,[浏览量] desc,[评论数] desc;""")

    def FileDateIdentify(fn):
        fnlist = []
        for file in os.listdir(mypath):
            if fnmatch.fnmatch(file, fn):
                fnlist.append(file)
        ftime = [str(t)[-11:-5] for t in fnlist]
        time_list = [int(t) for t in ftime]
        time_list.sort(reverse=True)

        ddiff = datetime.datetime.now().weekday()
        tday = datetime.datetime.now().date()
        wdop = int((tday - datetime.timedelta(days=ddiff)).strftime('%y%m%d'))
        wded = int((tday + datetime.timedelta(days=(6 - ddiff))).strftime('%y%m%d'))

        if time_list[0] < wdop and time_list[0] < wded:
            budget_compon = pd.read_sql(query, con=conn)
            budget_compon.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Budget_compon%s.xlsx' % date_saved)
        else:
            pass

    fn = 'Budget_compon_*.xlsx'

    FileDateIdentify(fn)
    fnlist = ['time_diff','Pro_score','Client_Score','weddingloc','casenum','webshowcase']
    Qlist = [query,query1,query2,query3,query4,query5,query6]
    for i in range(len(fnlist)):
        n = pd.read_sql(Qlist[i+1] ,con = conn)
        n.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\%s%s.xlsx'%(fnlist[i],date_saved))

def client1():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score%s.xlsx'%date_saved)
    client_score = client_score.dropna()
    time_diff = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\time_diff%s.xlsx'%date_saved)
    time_diff = time_diff.dropna()
    l = client_score.columns.tolist()
    l_var = ['策划师名称', '策划师id', '婚礼id','首付前满意度评分', '首付前出方案速度评分',
             '尾款前整体打分', '尾款前服务意识分数', '尾款前审美能力分数', '尾款前效果还原度分数', '尾款前控制预算分数', '尾款前形象气质分数', '完成订单总金额']
    allinfo = client_score[l_var]
    tl = ['wedding_id', 'OverallSpeed', 'PlanSpeed', 'DownPMT_diff', 'FinalPMT_diff']
    tl1 = ['OverallSpeed', 'PlanSpeed', 'DownPMT_diff', 'FinalPMT_diff']
    time_diff[tl1] = time_diff[tl1] / 1440
    time_speed = time_diff[tl]
    df1 = client_score['预算价格下限(元)']
    df2 = client_score['预算价格上限(元)']
    X = pd.DataFrame(abs(df2 - df1))

    new_table = pd.concat([client_score['婚礼id'], df1, df2, X, X], axis=1)
    new_table.columns = ['婚礼id', '预算价格下限(元)', '预算价格上限(元)', 'Range', 'Budget']

    for i in range(0, len(new_table['Budget']) - 1):
        if new_table.iloc[i, 3] > 9000:
            new_table.iloc[i, 4] = max(new_table.iloc[i, 1], new_table.iloc[i, 2])
        else:
            new_table.iloc[i, 4] = 0.5 * (new_table.iloc[i, 1] + new_table.iloc[i, 2])
    allinfo = allinfo.merge(time_speed, left_on='婚礼id', right_on='wedding_id', how='inner')
    allinfo = allinfo.merge(new_table, left_on='婚礼id', right_on='婚礼id', how='inner')
    temp_l = allinfo.columns.tolist()
    if '完成订单总金额' in temp_l: temp_l.remove('完成订单总金额')
    temp_l += ['完成订单总金额']
    allinfo = allinfo[temp_l]
    allinfo.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表.xlsx')
    df = allinfo[(allinfo['首付前满意度评分'] > 0) & (allinfo['尾款前效果还原度分数'] > 0)]
    df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(去零).xlsx')
    df = df.drop(['wedding_id'], axis=1)
    df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(Ratio_Adj).xlsx')
    return df

def client2():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score%s.xlsx'%date_saved)
    client_score = client_score.dropna()
    time_diff = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\time_diff%s.xlsx'%date_saved)
    time_diff = time_diff.dropna()
    l = client_score.columns.tolist()
    l_var = ['策划师名称', '策划师id', '婚礼id',
             '首付前满意度评分', '首付前出方案速度评分',
             '尾款前整体打分', '尾款前服务意识分数', '尾款前审美能力分数', '尾款前效果还原度分数', '尾款前控制预算分数', '尾款前形象气质分数', '完成订单总金额','累计有效回单数量']
    allinfo = client_score[l_var]
    tl = ['wedding_id', 'OverallSpeed', 'PlanSpeed', 'DownPMT_diff', 'FinalPMT_diff']
    tl1 = ['OverallSpeed', 'PlanSpeed', 'DownPMT_diff', 'FinalPMT_diff']
    time_diff[tl1] = time_diff[tl1] / 1440
    time_speed = time_diff[tl]
    #allinfo = allinfo.merge(time_speed, left_on='婚礼id', right_on='wedding_id', how='inner')
    allinfo = allinfo.join(time_speed.set_index('wedding_id'), on = '婚礼id')
    temp_l = allinfo.columns.tolist()
    if '完成订单总金额' in temp_l: temp_l.remove('完成订单总金额')
    temp_l += ['完成订单总金额']
    allinfo = allinfo[temp_l]
    df = allinfo[(allinfo['首付前满意度评分'] > 0) & (allinfo['尾款前效果还原度分数'] > 0)]
    df = df.drop(['婚礼id'], axis=1)
    df1 = pd.pivot_table(df,index = ['策划师名称','策划师id'],values = ['完成订单总金额','累计有效回单数量'],aggfunc = [np.sum,np.max])
    df2 = pd.pivot_table(df,index = ['策划师名称','策划师id'],aggfunc=np.mean)
    return df1,df2,df

def orderdiff():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score%s.xlsx'%date_saved)
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
    Cal_tb.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\OrderDiff.xlsx')
    L1 = ['婚礼id', 'Order_diff']

    return Cal_tb[L1]

def pro1():
    pro_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score%s.xlsx'%date_saved)
    pro_score = pro_score.dropna()
    pro_score = pro_score[(pro_score['评分项类型'] == 1)]
    pro_score['分数'] = pro_score.分数.apply(lambda x: int(x))
    pro_score.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score1.xlsx')
    pro_ave = pd.pivot_table(pro_score, index='婚礼id', columns='评分项名称', values='分数', aggfunc=np.mean)
    pro_ave = pro_ave.dropna(axis=1)
    pro_ave.reset_index()
    pro_ave.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro1.xlsx')
    pro_ave = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro1.xlsx')
    return pro_ave

def pro2():
    pro_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score%s.xlsx'%date_saved)
    pro_score = pro_score.dropna()
    pro_score = pro_score[(pro_score['评分项类型'] == 1)]
    pro_score['分数'] = pro_score.分数.apply(lambda x: int(x))
    pro_score.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro_Score1.xlsx')
    pro_ave = pd.pivot_table(pro_score, index=['职业人名称','职业人id'], columns='评分项名称', values='分数', aggfunc=np.mean)
    pro_ave = pro_ave.dropna(axis=1)
    pro_ave.reset_index()
    pro_ave.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro2.xlsx')
    pro_ave = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Pro2.xlsx')
    return pro_ave


def orderspeed():
    client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score%s.xlsx'%date_saved)
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
    Cal_tb.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\OrderSpeed.xlsx')
    L1 = ['婚礼id','Turnover_Speed']
    return Cal_tb[L1]


def get_range(df):
  med = df.median().values
  std = df.std().values
  range =[med+3*std,med-3*std]
  return range

def get_range1(df):
  up = df.quantile(0.75).values
  down = df.quantile(0.25).values
  std = df.std().values
  range =[up+1.5*std,down-1.5*std]
  return range
t1 = time.time()
sqlextract()
print(time.time()-t1)