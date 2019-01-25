import matplotlib.pyplot as plt
import math
import os
import time
import pandas as pd
from statsmodels.formula.api import ols
from datetime import datetime,timedelta
from statsmodels.stats.anova import anova_lm
import numpy as np


def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

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

#读取excel文件
path = u'C:/Users/t430/Desktop/Incentive/RawData'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
file_name = r'用户打分_婚礼信息(婚期,酒店,顾问)_订单金额_回单_截止2018-12-13.xlsx'
file_name_time = r'确定定策划师时间,方案报价提交,婚期,尾款付清时间_截止2018-12-24.xlsx'

data= read_file(path,file_name)
data_time = read_file(path,file_name_time)

########## Time Diff
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
Speed_tb = Speed_tb[(Speed_tb['首付速度'])>1]


# Budget Adj
df1 = data['预算价格下限(元)']
df2 = data['预算价格上限(元)']
X=pd.DataFrame(abs(df2 -df1))

new_table = pd.concat([df1,df2,X,X],axis = 1)
new_table.columns = ['预算价格下限(元)','预算价格上限(元)','Range','Budget']

for i in range(0,len(new_table['Budget'])-1):
    if new_table.iloc[i,2] > 9000:
       new_table.iloc[i,3] = max(new_table.iloc[i,0],new_table.iloc[i,1])
    else:
       new_table.iloc[i,3] = 0.5*(new_table.iloc[i,0]+new_table.iloc[i,1])


#增加所需要变量
# data['Gender'] = data.sex.apply(lambda x: 1 if 'female' in x else 0)
# data['Age'] = data['年龄'].apply(lambda x: 1 if x>25 else 0)
# dummies_Gender = pd.get_dummies(data['Gender'],prefix='Gender',prefix_sep="")
# dummies_Age = pd.get_dummies(data['Age'],prefix='Age',prefix_sep="")
# dummies_combine = pd.concat([dummies_Gender,dummies_Age],axis= 1)
allinfo = pd.concat([new_table['Budget'],data],axis=1)
allinfo = allinfo.merge(Speed_tb,left_on ='婚礼id' , right_on ='wedding_id' , how = 'outer')
allinfo = allinfo.dropna(axis = 0)
#拼接Column名形成因子变量表
col_name = allinfo.columns
list_name = col_name.tolist()
ditch1 = list_name.index('完成订单总金额')
ditch2 = list_name.index('婚礼id')
ditch3 = list_name.index('首付前满意度评分')
ditch4 = list_name.index('尾款前整体打分')
ditch5 = list_name.index('Budget')
ditch6 = list_name.index('首付速度')
col1 = col_name[ditch4:(ditch4+6)].tolist() #locate final payment elements
col2 = col_name[ditch3:(ditch3+2)].tolist() #locate down payment elements
col3 = col_name[(ditch2):ditch2+1].tolist() #locate dummies
col4 = col_name[ditch1:ditch1+1].tolist() # locate Output
col5 = col_name[ditch5:ditch5+1].tolist() # locate budget
col6 = col_name[ditch6:ditch6+2].tolist() # locate time differ data
col =col3+col5+col6+col2+col1+col4

df = allinfo[col]
df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表.xlsx')
df = df[(df['Budget']>2000)&(df['首付前满意度评分']>0)&(df['尾款前效果还原度分数']>0)]
df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(去零).xlsx')

T = pd.DataFrame(df['完成订单总金额']/df['Budget'])
T.columns = ['Ratio']
df = pd.concat([df,T],axis = 1)
df = df[(df['Ratio']>get_range(T)[1][0])&(df['Ratio']<get_range(T)[0][0])]
df.to_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(Ratio_Adj).xlsx')


list = df.columns.tolist()
list.remove('婚礼id')
xx = list[0:(len(list)-2)]
xx1 = "+".join(xx)
model = ols('完成订单总金额~%s'%xx1, data=df).fit()
#anovat = anova_lm(model)

#输出残值表
residual1 = pd.DataFrame(model.resid)
residual2 = pd.DataFrame(model.resid_pearson)
residual = pd.concat([residual1,residual2],axis =1)
resid_table = pd.DataFrame(residual).to_excel(u'C:/Users/t430/Desktop/Incentive/csv/ResCheck.xlsx')
#key_word = pd.DataFrame(dir(model)).to_excel(u'C:/Users/t430/Desktop/Incentive/关键字.xlsx')

rfdf1 = pd.DataFrame(model.params)
rfdf2 = pd.DataFrame(model.bse)
rfdf3 = pd.DataFrame(model.tvalues)
rfdf4 = pd.DataFrame(model.pvalues)

#coeff/stderr/tvalue/pvalue
rfdf_raw = pd.concat([rfdf1,rfdf2,rfdf3,rfdf4],axis = 1)
rfdf = pd.DataFrame(rfdf_raw)
rfdf.columns=['Coeff','Stdev err','t Value','p Value']
print(type(rfdf))
print(rfdf)
rfdf.to_excel(u'%sSummary2_Table.xlsx'%path_output)

d = {"Item":['Df Residuals','Df Models','R^2','Adj.R^2','F Statistic','Prob(F)','Log Likehood','AIC','BIC'],
     "Value":[model.df_resid,model.df_model,model.rsquared,model.rsquared_adj,model.fvalue,model.f_pvalue,model.llf,model.aic,model.bic]}
d1 = pd.DataFrame(d)

d1.to_excel(u'%sSummary_Table.xlsx'%path_output)




#print(model.bse)
print(model.summary())
#print(anovat)
#print(dir(model))




