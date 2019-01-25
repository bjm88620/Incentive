from izhaowoDataprocessing import *
from functools import reduce
import statsmodels.api as sm
import numpy as np
pro = pro1()
client = client1()
client = client.drop(['策划师名称', '策划师id','预算价格下限(元)','预算价格上限(元)','Range','Budget'],axis = 1)
orderdiff = orderdiff()
#orderspeed = orderspeed()

df = [client,pro,orderdiff]

df_final = reduce(lambda left,right: pd.merge(left,right,on='婚礼id'), df)
df_final.to_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Widetable.xlsx')
X = df_final.drop(['婚礼id','完成订单总金额','Order_diff'],axis = 1)
# X_l = X.columns.tolist()
# n = len(X['性价比'])
# X = np.array(X).reshape(n,len(X_l))
Y = df_final['完成订单总金额']

X = sm.add_constant(X)
model = sm.OLS(Y,X).fit()
print(model.summary())