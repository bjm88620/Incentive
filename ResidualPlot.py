import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
data = pd.read_excel(u'C:/Users/t430/Desktop/Incentive/Variable/因子变量表(Ratio_Adj).xlsx')
df = data[(data['Budget'] < 100000)]
#sns.lmplot(x="尾款前形象气质分数", y="Profit", col="金额梯度", data=df, sharey=False)
sns.residplot(x="Budget", y="完成订单总金额", data=df)
sns.jointplot('Budget', '完成订单总金额', data=df,kind='reg')
plt.show()