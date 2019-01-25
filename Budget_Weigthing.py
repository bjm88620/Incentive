import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

def read_file(path,name):
  df = pd.read_excel('%s/%s'%(path,name))
  return df

Scores_knn_train = []
Scores_knn_test = []
Scores_logistic_train = []
Scores_logistic_test = []
Coef = []
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
for i in range(1):
    path = u'C:/Users/t430/Desktop/Incentive/RawData'
    data = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\Budget_compon.xlsx')
    file_name1 = r'用户打分_婚礼信息(婚期,酒店,顾问)_订单金额_回单_截止2018-11-27.xlsx'

    df = read_file(path,file_name1)

    ########## Budget list re-organise
    col_name = data.columns
    list_name = col_name.tolist()
    ditch1 = list_name.index('策划师')
    ditch2 = list_name.index('付款阶段')
    ditch3 = list_name.index('婚礼ID')
    col1 = col_name[ditch1:ditch1+1].tolist() #get 策划师
    col2 = col_name[ditch2:ditch2+1].tolist()#get 付款阶段
    col3 = col_name[ditch3:len(col_name)+1].tolist()#get 婚礼ID&all
    col4 = col_name[ditch3+1:len(col_name)+1].tolist()#get 变量 without ID
    col = col1+col2+col3
    data_sum = data[col4]
    data_sum = data_sum.cumsum(axis =1)
    data_sum.columns = ['1','2','3','4','5','6','Total_Budget']
    #data_sum['Total_Budget'] = data_sum.cumsum(axis=1)
    data1 = data[col3].iloc[:,1:].div(data_sum.Total_Budget, axis=0)
    #data = pd.concat([data[col],data_sum['Total_Budget']],axis = 1)
    data = pd.concat([data[col1+col2],data['婚礼ID'],data1],axis =1 )
    data.to_excel('%sBudget_Weigthing.xlsx'%path_output)

    ######## Client Scoer re-organise
    df = pd.concat([df['婚礼id'],df['策划师名称'],df['完成订单总金额']],axis = 1)

    data_allinfo = data.merge(df,left_on = '婚礼ID',right_on= '婚礼id',how = 'outer')
    data_allinfo.dropna().to_excel('%sBudget_Profit.xlsx'%path_output)
    data_avail = data_allinfo.dropna()

    ######## Add Budget data to calculate Ratio
    bg = pd.read_excel('%sBudget.xlsx'%path_output)
    bg.columns = ['ID','Agent','Budget','Amount']

    data_all = data_avail.merge(bg,left_on = '婚礼ID',right_on = 'ID',how='outer')
    #print(data_all.columns)
    data_all['Ratio'] = data_all['Budget']/data_all['Amount']
    data_all = data_all.drop(['策划师名称','婚礼id','付款阶段','婚礼ID','策划师','Agent','完成订单总金额','ID','Amount'],axis =1)


    data_all = data_all.dropna()
    data_all['label'] = np.where(data_all['Ratio']>=1, 1, 0)
    data_all.to_excel('%sBudgetRatio.xlsx'%path_output)
    X = np.array(data_all.drop(['Ratio','label','交通费','执行人员','仪式区','灯光舞美','其它'],axis = 1))
    y = np.array(data_all['label'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = KNeighborsClassifier(n_neighbors = 7)
    clf.fit(X_train,y_train)
    #print(clf.score(X_train,y_train),clf.score(X_test,y_test))
    Scores_knn_train.append(clf.score(X_train,y_train))
    Scores_knn_test.append(clf.score(X_test,y_test))

    #logit = sm.Logit(y, sm.add_constant(X)).fit()
    #print(logit.summary())

    model = LogisticRegression(penalty = 'l2',C=1).fit(X_train,y_train)
    #print(model.score(X_train,y_train),model.score(X_test,y_test))
    #print(dir(model))
    #print("The coefs are %s "%model.coef_)
    #print("The intercept is %s "%model.intercept_)
    #print(model.predict(X_test))
    Coef.append(model.coef_)
    Scores_logistic_train.append(model.score(X_train,y_train))
    Scores_logistic_test.append(model.score(X_test, y_test))
#print(Scores_knn_train)
#print(Scores_knn_test)
#print(Scores_logistic_train)
#print(Scores_logistic_test)
output = {'KNN_Train_Score':Scores_knn_train,'KNN_Test_Score':Scores_knn_test,
          'Logistic_Train_Score':Scores_logistic_train,'Logistic_Test_Score':Scores_logistic_test}
output = pd.DataFrame(output)
output.to_excel('%sBudget_KNN_Scores_1.xlsx'%path_output)
#Coef = pd.DataFrame(Coef)
#Coef.to_excel('%sCoef.xlsx'%path_output)
print(output)
print(Coef)