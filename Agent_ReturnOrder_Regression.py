import numpy as np
import pandas as pd
import collections,pylab
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import izhaowoDataprocessing as idata
import os,time
date_now = int(round(time.time() * 1000))
date_saved = "_" + time.strftime('%y%m%d', time.localtime(date_now / 1000))
client_score = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Client_Score%s.xlsx'%date_saved)

y,x1,all = idata.client2()
y = y.reset_index()
y.columns = ['策划师名称','策划师id','完成订单总金额_sum','累计有效回单数量_sum','完成订单总金额_max','累计有效回单数量_max']
x = collections.Counter(client_score['策划师id'])
df = pd.DataFrame.from_dict(x, orient='index').reset_index()
df.columns = ['策划师id','OrderNum']
y= y.join(df.set_index('策划师id'),on='策划师id')
y = y.drop('累计有效回单数量_sum',axis = 1)
y.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\AgentInfo%s.xlsx'%date_saved)
x1 = x1.reset_index()
x1 = x1.drop('累计有效回单数量',axis = 1)
x1 = x1.join(y.set_index('策划师id'),on='策划师id',rsuffix='_y')
x1 = x1.drop('策划师名称_y',axis = 1)
temp_l = x1.columns.tolist()
if '累计有效回单数量_max' in temp_l: temp_l.remove('累计有效回单数量_max')
temp_l += ['累计有效回单数量_max']
x1 = x1[temp_l]
#x1 = x1.drop(['完成订单总金额_sum'],axis = 1)
x2 = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\casenum%s.xlsx'%date_saved)
x1 = x1.join(x2.set_index('策划师id'),on='策划师id',rsuffix = '_y')
x1 = x1.drop('策划师名称_y',axis = 1)
x1.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\AgentInfo1%s.xlsx'%date_saved)
x1 = x1.dropna()
X = x1.drop(['策划师名称','策划师id','累计有效回单数量_max','婚礼案例总数','完成订单总金额_sum','完成订单总金额_max','完成订单总金额'],axis = 1)    ###### Regression with Client Score only
y = x1['累计有效回单数量_max']                                            ###### Regression with Client Score only
X = sm.add_constant(X)                                                  ###### Regression with Client Score only
model = sm.OLS(y,X).fit()                                               ###### Regression with Client Score only
print(model.summary())                                                  ###### Regression with Client Score only
#
#
# x2 = idata.pro2()                                                                   ###### Regression with Pro Score
# y = x1.merge(x2,left_on ='策划师名称',right_on = '职业人名称',how ='inner')         ###### Regression with Pro Score
# y.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\AgentInfo_final.xlsx')             ###### Regression with Pro Score
# y = y.drop(['职业人id','职业人名称'],axis = 1)                                        ###### Regression with Pro Score
# X = y.drop(['策划师名称','策划师id','累计有效回单数量_max','婚礼案例总数','完成订单总金额_sum','完成订单总金额_max','完成订单总金额'],axis = 1)                 ###### Regression with Pro Score
# Y = y['累计有效回单数量_max']                                                         ###### Regression with Pro Score
# X = sm.add_constant(X)                                                              ###### Regression with Pro Score
# model = sm.OLS(Y,X).fit()                                                           ###### Regression with Pro Score
# print(model.summary())                                                              ###### Regression with Pro Score
#x = model.resid
#y = model.predict()
# stats.probplot(x,dist = 'norm',plot = pylab)
# pylab.show()
#plt.hist(x,60)
#plt.show()