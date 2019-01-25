import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

data = pd.read_csv(u'C:/Users/t430/Desktop/Incentive/Output/Dev.csv', sep=",", encoding="gbk")
df = pd.DataFrame(data)

model = ols('Profit~尾款前形象气质分数',data).fit()
#model = ols('Profit~首付前满意度评分+首付前出方案速度评分+尾款前整体打分+尾款前服务意识分数+尾款前审美能力分数+尾款前效果还原度分数+尾款前控制预算分数+尾款前形象气质分数', data).fit()
anovat = anova_lm(model)
summ = model.summary()
print(model.summary())
print(anovat)