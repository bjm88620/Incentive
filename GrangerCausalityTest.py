from statsmodels.tsa.stattools  import   grangercausalitytests
import pandas as pd
import pandas as pd
from statsmodels.tsa.stattools  import   grangercausalitytests
path = u'C:/Users/t430/Desktop/Incentive/Input_Python'
path_output = u'C:/Users/t430/Desktop/Incentive/Output/'
df = pd.read_excel(u'%s/Granger.xlsx'%path)
data = pd.DataFrame(df)
i = 1
n = len(data.columns)
print(n)

for i in range(1,20):
 d = pd.concat([ data[data.columns[i]],data[data.columns[n-1]]],axis =1 )
 print("The Variable and Dependent testing now are %s and %s"%(d.columns[0],d.columns[1]))
 model = grangercausalitytests(d, maxlag=5, addconst=True, verbose=True)
 print("")
 print("")

