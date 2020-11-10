# ------------------------------------
# Stats 506 midterm project
# ARIMA model for time series data
# Author: Zhilin he, Group 3
# Updated: November 9, 2020
# ------------------------------------

## Import data
import pandas as pd
df = pd.read_csv('../NIFTY50_all.csv')

## Data cleaning
from datetime import datetime
from sklearn.impute import SimpleImputer
# Drop redundant variables and variables with too many missing values
df1 = df.drop(['Trades', 'Deliverable Volume', 'Series'], axis=1)
df1['Symbol'] = pd.Categorical(df1['Symbol'])
df1['Date'] = [datetime.strptime(x, '%Y-%m-%d') for x in df1['Date']]
df1['Date']=df1['Date'].map(datetime.toordinal)
df2 = pd.get_dummies(data=df1, drop_first=True)
# Impute missing values
imp = SimpleImputer()
p = imp.fit_transform(df2)
df1['%Deliverble'] = p[:, 10]

## Fit the main models

