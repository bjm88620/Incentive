import matplotlib.pyplot as plt
import math
import pandas as pd
import os
import time

#返回[E（X）,标准差，E（X^3）]
def calc(data):
    n = len(data)
    niu = 0.0
    niu2 = 0.0
    niu3 = 0.0
    for a in data:
        niu += a
        niu2 += a**2
        niu3 += a**3
    niu/= n   #这是求E(X)
    niu2 /= n #这是E(X^2)
    niu3 /= n #这是E(X^3)
    sigma = math.sqrt(niu2 - niu*niu) #这是D（X）的开方，标准差
    return [niu,sigma,niu3]
#返回了均值，标准差，偏度，峰度
def calc_stat(data):
    [niu,sigma,niu3] = calc(data)
    n = len(data)
    niu4 = 0.0
    for a in data:
        a -= niu
        niu4 += a ** 4
    niu4 /= n
    skew = (niu3 - 3*niu*sigma**2 - niu**3)/(sigma**3)
    kurt =  niu4/(sigma**2)-3
    return [niu,sigma,skew,kurt]
#残差正太分布图生成和保存
def draw_hist(myList, Title, Xlabel, Ylabel, Xmin, Xmax, Ymin, Ymax):
    plt.hist(myList, 100)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin, Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin, Ymax)
    plt.title(Title)
    path = u"C:/Users/t430/Desktop/Incentive/Chart"
    count = 0
    for fn in os.listdir(path):  # fn 表示的是文件名
          count = count + 1
    date_now = int(round(time.time() * 1000))
    date_saved = "_"+time.strftime('%y%m%d', time.localtime(date_now / 1000))
    fn = "Residual Hist_%s%s.png" % (count + 1,date_saved)
    plt.savefig(u"C:/Users/t430/Desktop/Incentive/Chart/%s"%fn)
    plt.show()


if __name__== "__main__":
    datat = pd.read_excel(u'C:/Users/t430/Desktop/Incentive/csv/ResCheck.xlsx')
    df = pd.DataFrame(datat)
    x = df[df.columns[0]]


    [niu,sigma,skew,kurt] = calc_stat(x)

    list = [niu,sigma,skew,kurt]
    Index = ['E(X)','E(X^2)','Skewness','Kurtosis']
    Tabel = {'Data_Name':Index,'Value':list}
    tabel = pd.DataFrame(Tabel)
    tabel.to_excel(u'C:/Users/t430/Desktop/Incentive/Output/残差分布数值.xlsx')
    print(tabel)

    draw_hist(df[df.columns[1]], 'Residual Hist', 'Residual', 'number', -8, 8, 0.0, 60)



