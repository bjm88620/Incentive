import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from tempfile import NamedTemporaryFile

df = pd.read_csv(u'C:/Users/t430/Desktop/Output/Dev.csv', sep=",", encoding="gbk")
#col1 = pd.DataFrame(df['首付前满意度评分'])
#col2 = col1.drop_duplicates().reset_index().drop(['index'],axis=1)



#dummies = pd.get_dummies(df,columns=['首付前满意度评分'],prefix =['首付前满意度评分'],prefix_sep="_",dummy_na=
                         #False, drop_first = False)
dummies1 = pd.get_dummies(df['首付前满意度评分'],prefix='D1',prefix_sep="")
dummies2 = pd.get_dummies(df['首付前出方案速度评分'],prefix='D2',prefix_sep="")
dummies3 = pd.get_dummies(df['尾款前整体打分'],prefix='D3',prefix_sep="")
dummies4 = pd.get_dummies(df['尾款前服务意识分数'],prefix='D4',prefix_sep="")
dummies5 = pd.get_dummies(df['尾款前审美能力分数'],prefix='D5',prefix_sep="")
dummies6 = pd.get_dummies(df['尾款前效果还原度分数'],prefix='D6',prefix_sep="")
dummies7 = pd.get_dummies(df['尾款前控制预算分数'],prefix='D7',prefix_sep="")
dummies8 = pd.get_dummies(df['尾款前形象气质分数'],prefix='D8',prefix_sep="")

#fit3 = sm.GLM(df['Profit'], dummies1).fit()
dummiesall = pd.concat([dummies1,dummies2,dummies3,dummies4,dummies5,dummies6,dummies7,dummies8],axis=1)

#model = sm.GLM(df['Profit'],dummiesall).fit()
pro = pd.DataFrame(df['Profit'])

dataset = pd.concat([dummiesall,pro],axis=1)

df1 = pd.DataFrame(dataset)

list = df1.columns
x = list[1:(len(list)-1)]
x1 = "+".join(x)

model = ols('Profit~%s'%x1, data=df1).fit()
anovat = anova_lm(model)
print (model.summary())
print(anovat)
print(type(anovat))
print(type(model.summary))