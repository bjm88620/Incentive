import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pylab import mpl
import os,time
mpl.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

data = pd.read_excel(r'C:\Users\t430\Desktop\Incentive\SQL\AgentInfo_final.xlsx')
y = data.drop(['职业人id','职业人名称'],axis = 1)
X = y.drop(['策划师名称','策划师id','累计有效回单数量_max'],axis = 1)
Y = y['累计有效回单数量_max']
X = sm.add_constant(X)
xx = X.columns.tolist()
model = sm.OLS(Y,X).fit()
count = 0
for i in range(1,len(xx)):
    plt.xlabel(xx[i])
    plt.ylabel('累计回单')
    plt.scatter(X[xx[i]],Y)

    path = u"C:/Users/t430/Desktop/Incentive/Chart"
    for fn in os.listdir(path):  # fn 表示的是文件名
        count += 1
    date_now = int(round(time.time() * 1000))
    date_saved = "_" + time.strftime('%y%m%d', time.localtime(date_now / 1000))
    fn = "Resid Scatter_%s%s.png" % (count + 1, date_saved)
    plt.savefig(u"C:/Users/t430/Desktop/Incentive/Chart/%s" % fn)
    plt.close()


print(model.summary())