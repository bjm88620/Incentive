import quandl, math,datetime,pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
quandl.ApiConfig.api_key = "YCVGyaZS1XysGwGxxBAs" #set quandl api
df = quandl.get("WIKI/DIS") #Get data from quandl
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True) #set extreme value so na value will become outlier
forecast_out = int(math.ceil(0.01 * len(df))) #shift value
print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)
print(df.head())
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X) #Center to the mean and component wise scale to unit variance
X_lately = X[-forecast_out:] #predit against
X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df['label'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = LinearRegression(n_jobs=-1) #Algorithm
#clf = svm.SVR()
clf.fit(X_train, y_train)
with open('linearregression.pickle','wb') as f:
    pickle.dump(clf,f)

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)
confidence = clf.score(X_test, y_test)

forecast_set = clf.predict(X_lately)


print(forecast_set,confidence)


df['Forecast'] = np.nan #Create new column with nan value in in it

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix+ one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i] #.loc will reference the index of 'next_date'

print(df.tail())
df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc = 4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()