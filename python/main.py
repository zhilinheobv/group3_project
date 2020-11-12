# ------------------------------------
# Stats 506 midterm project
# ARIMA model for time series data
# Author: Zhilin he, Group 3
# Updated: November 9, 2020
# ------------------------------------

## Import data

import pandas as pd
import numpy as np
df = pd.read_csv('../NIFTY50_all.csv')

## Data cleaning and visualization

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
# Data visualization
import matplotlib.pyplot as plt
example = df[df['Symbol'] == 'MUNDRAPORT']
fig, ax = plt.subplots(3, 1, figsize=(15,15))
ax[0].plot(example['Date'], example['VWAP'])
ax[0].set_xticks([])
ax[0].set_xlabel('Date')
ax[0].set_ylabel('Volume weighted average price')
ax[1].plot(example['Date'], example['Volume'])
ax[1].set_xticks([])
ax[1].set_xlabel('Date')
ax[1].set_ylabel('Volume')
ax[2].plot(example['Date'], example['Turnover'])
ax[2].set_xticks([])
ax[2].set_xlabel('Date')
ax[2].set_ylabel('Turnover')
plt.savefig('p1.png')

## Determine the order of differencing for the data

from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima.utils import ndiffs
names = df1['Symbol'].cat.categories
ls0 = []
for i in names:
    subdf = df1[df1['Symbol'] == i]
    ls0.append(ndiffs(subdf['VWAP'], test='adf'))
ls0  # Most values are 1
max(ls0) # We only need 1st order differencing

## Determine the order of the AR term

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
fig, ax = plt.subplots(1, 3, figsize=(15,5))
# Take the first 3 stocks as a sample
for i in range(3):
    subdf = df1[df1['Symbol'] == names[i]]
    plot_pacf(subdf['VWAP'].diff().dropna(), ax=ax[i])
    ax[i].set_title('PACF plot for stock %d' % (i+1))
plt.savefig('p2.png')
# Lag 1 is at least borderline significant for all 3 stocks.
# We can choose 1 as the order of AR term.

## Determine the order of the MA term

fig, ax = plt.subplots(1, 3, figsize=(15,5))
# Take the stocks 4-6 as a sample
for i in range(3):
    subdf = df1[df1['Symbol'] == names[i+3]]
    plot_acf(subdf['VWAP'].diff().dropna(), ax=ax[i])
    ax[i].set_title('ACF plot for stock %d' % (i+4))
plt.savefig('p3.png')
# The plots are similar to the PACF plots, so we also 
