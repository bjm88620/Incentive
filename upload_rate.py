import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from sklearn.preprocessing import scale
import statsmodels.api as sm

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

path = u'C:/Users/t430/Desktop/Incentive'
file_name = r'X1214_R2.xlsx'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
data= read_file(path,file_name)
colname = data.columns.tolist()
data = data[colname[2:]]
data.columns = ['整体打分','速度','Upload','有效回单数']
model1 = ols('有效回单数~整体打分', data=data).fit()
model2 = ols('有效回单数~速度', data=data).fit()
model3 = ols('有效回单数~Upload', data=data).fit()
l = [model1.rsquared,model2.rsquared,model3.rsquared]
x1 = scale(np.array(data['整体打分']))
x2 = scale(np.array(data['速度']))
x3 = scale(np.array(data['Upload']))
y = scale(np.array(data['有效回单数']))
model4 = sm.OLS(y,x1).fit()
model5 = sm.OLS(y,x2).fit()
model6 = sm.OLS(y,x3).fit()
print(model4.rsquared,model5.rsquared,model6.rsquared)

print(scale(np.array(l)))




