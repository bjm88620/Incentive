import pymssql as ps
import pandas as pd
import datetime

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
# def get_range(df):
#   med = df.median().values
#   std = df.std().values
#   range =[med+3*std,med-3*std]
#   return range
#
# def get_range1(df):
#   up = df.quantile(0.75).values
#   down = df.quantile(0.25).values
#   std = df.std().values
#   range =[up+1.5*std,down-1.5*std]
#   return range

t1 = datetime.datetime.now()

conn = ps.connect(host='121.42.61.195',user='test',password='tes@t123456#pwd2018&',charset='utf8')

query = ('SELECT [策划师名称],[worker_id]策划师id,[wedding_id]婚礼id,[婚期],[预算价格下限(元)]'
         ',[预算价格上限(元)],[完成订单总金额],[首付前满意度评分],[首付前出方案速度评分]'
         ',[尾款前整体打分],[尾款前服务意识分数],[尾款前审美能力分数],[尾款前效果还原度分数]'
         ',[尾款前控制预算分数],[尾款前形象气质分数],[首付前评价时间],[尾款前评价时间],[回单日期],[累计有效回单数量]'
         'FROM [TOPN].[dbo].[婚礼策划尾款前评分_策划师有效回单累计数据表] order by worker_id , 尾款前评价时间;')

query1 = ('SELECT [worker_name],[worker_id],[wedding_id],[方案首付金额(元)],[定策划师的时间],[方案报价提交时间]'
          ',[首付时间],[婚期],[尾款支付时间],[尾款支付金额],DATEDIFF(minute,[定策划师的时间],[尾款支付时间]) OverallSpeed,'
          'DATEDIFF(minute,[方案报价提交时间],[首付时间]) DownPMT_diff,'
          'DATEDIFF(minute,[定策划师的时间],[方案报价提交时间]) PlanSpeed,'
          'DATEDIFF(minute,[婚期],[尾款支付时间]) FinalPMT_diff FROM [TOPN].[dbo].[婚礼进程各阶段关键节点时间表] order by [婚期] asc;')

client_score = pd.read_sql(query, con=conn)
client_score.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score.xlsx')
client_score = client_score.dropna()

#Amount as output measurement
############################################################################################
time_diff = pd.read_sql(query1, con=conn)
time_diff.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\time_diff.xlsx')
time_diff = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\time_diff.xlsx')
time_diff = time_diff.dropna()

t2 = datetime.datetime.now()
l = client_score.columns.tolist()
l_var = ['策划师名称', '策划师id', '婚礼id',
         '首付前满意度评分', '首付前出方案速度评分',
         '尾款前整体打分', '尾款前服务意识分数', '尾款前审美能力分数', '尾款前效果还原度分数', '尾款前控制预算分数', '尾款前形象气质分数','完成订单总金额']

df1 = client_score['预算价格下限(元)']
df2 = client_score['预算价格上限(元)']
temp_table = pd.concat([df1,df2,df1],axis = 1)
temp_table.columns = ['预算价格下限(元)','预算价格上限(元)','Budget']
X=pd.DataFrame(abs(df2 -df1))
new_table = pd.concat([df1,df2,X,X],axis = 1)
new_table.columns = ['预算价格下限(元)','预算价格上限(元)','Range','Budget']

for i in range(0,len(new_table['Budget'])-1):
    if new_table.iloc[i,2] > 9000:
       new_table.iloc[i,3] = max(new_table.iloc[i,0],new_table.iloc[i,1])
    else:
       new_table.iloc[i,3] = 0.5*(new_table.iloc[i,0]+new_table.iloc[i,1])

allinfo = pd.concat([client_score[l_var],new_table['Budget']],axis=1)

tl = ['wedding_id','OverallSpeed','PlanSpeed','DownPMT_diff','FinalPMT_diff']
tl1 = ['OverallSpeed','PlanSpeed','DownPMT_diff','FinalPMT_diff']
time_diff[tl1] = time_diff[tl1] / 1440
time_speed = time_diff[tl]

allinfo = allinfo.merge(time_speed,left_on ='婚礼id' ,right_on ='wedding_id' , how = 'inner')
temp_l = allinfo.columns.tolist()
if '完成订单总金额' in temp_l: temp_l.remove('完成订单总金额')

temp_l += ['完成订单总金额']
allinfo = allinfo[temp_l]
allinfo.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表.xlsx')
df = allinfo[(allinfo['Budget']>2000)&(allinfo['首付前满意度评分']>0)&(allinfo['尾款前效果还原度分数']>0)]
df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(去零).xlsx')

T = pd.DataFrame(df['完成订单总金额']/df['Budget'])
T.columns = ['Ratio']
df = pd.concat([df,T],axis = 1)
df = df[(df['Ratio']>getrange(T)[1][0])&(df['Ratio']<getrange(T)[0][0])]
df = df.drop(['wedding_id'],axis =1)
df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(Ratio_Adj).xlsx')

t3 =datetime.datetime.now()
print("SQL extracting : %s sec."%(t2-t1).seconds)
print("Other : %s sec."%(t3-t2).seconds)
############################################################################################

# Returning Order Speed as output measurement

od_l = ['婚礼id','策划师名称','回单日期','累计有效回单数量']

ros_tb = client_score[od_l].sort_values(by=['策划师名称','回单日期'])

print(ros_tb)