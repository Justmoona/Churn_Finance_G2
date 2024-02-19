
import opendatasets as od
import pandas as pd

# "username": "marytraore", "key": "58ad6fa7ead6f6a289cbba6fb47c0da6"}"
od.download("https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers?select=churn.csv")
df=pd.read_csv("/content/churn-for-bank-customers/churn.csv")
df.head()
df.tail()   
df.shape
df.dtypes
# df.info()

