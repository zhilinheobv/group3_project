# ------------------------------------
# Stats 506 midterm project
# ARIMA model for time series data
# Author: Zhilin he, Group 3
# Updated: November 12, 2020
# ------------------------------------

## Import data

import pandas as pd
import numpy as np
df = pd.read_csv('../NIFTY50_all.csv')

## Data cleaning and visualization

from datetime import datetime
from sklearn.impute import SimpleImputer
# Drop redundant variables and variables with too many missing values
df['Date'] = [datetime.strptime(x, '%Y-%m-%d') for x in df['Date']]
df1 = df.drop(['Trades', 'Deliverable Volume', 'Series'], axis=1)
ls1 = ['MUNDRAPORT', 'UTIBANK', 'BAJAUTOFIN', 'BHARTI', 'HEROHONDA',
       'HINDALC0', 'HINDLEVER', 'INFOSYSTCH', 'JSWSTL', 'KOTAKMAH', 'TELCO',
       'TISCO', 'UNIPHOS', 'SESAGOA', 'SSLT', 'ZEETELE']
ls2 = ['ADANIPORTS', 'AXISBANK', 'BAJFINANCE', 'BHARTIARTL', 'HEROMOTOCO',
       'HINDALCO', 'HINDUNILVR', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'TATAMOTORS',
       'TATASTEEL', 'UPL', 'VEDL', 'VEDL', 'ZEEL']
df1['Symbol'] = df1['Symbol'].replace(ls1, ls2)
df1['Symbol'] = pd.Categorical(df1['Symbol'])
# Impute missing values
df2 = pd.get_dummies(data=df1, drop_first=True)
df2['Date']=df2['Date'].map(datetime.toordinal)
imp = SimpleImputer()
p = imp.fit_transform(df2)
df1['%Deliverble'] = p[:, 10]
df1.to_csv('cleaned.csv')
# Data visualization
import matplotlib.pyplot as plt
names = df1['Symbol'].cat.categories
example = df1[df1['Symbol'] == names[0]]
fig, ax = plt.subplots(3, 1, figsize=(15, 15))
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
ax[0].set_title('Time series plots of stock %s' % names[0])
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
fig, ax = plt.subplots(1, 4, figsize=(15, 5))
# Take the first 4 stocks as a sample
for i in range(4):
    subdf = df1[df1['Symbol'] == names[i]]
    plot_pacf(subdf['VWAP'].diff().dropna(), ax=ax[i])
    ax[i].set_title('PACF plot for stock %s' % names[i])
plt.savefig('p2.png')
# Lag 1 is at least borderline significant for all stocks.
# We can choose 1 as the order of AR term.

## Determine the order of the MA term

# Take the stocks 5-8 as a sample
fig, ax = plt.subplots(1, 4, figsize=(15, 5))
for i in range(4):
    subdf = df1[df1['Symbol'] == names[i+4]]
    plot_acf(subdf['VWAP'].diff().dropna(), ax=ax[i])
    ax[i].set_title('ACF plot for stock %s' % names[i+4])
plt.savefig('p3.png')
# Lag 1 is again significant for most stocks but lag 2 is often not.
# We can choose 1 as the order of MA term.

## Fit the models

mlist = []
flist = []
for i in names:
    subdf = df1[df1['Symbol'] == i]
    m = ARIMA(list(subdf['VWAP']), order=(1, 1, 1))
    mlist.append(m)
    flist.append(m.fit(disp=0))
for i in range(5):
    print(flist[i].summary())
# For the first 3 stocks, the model fit is not good.
# Consider removing the MA part.
mlist0 = []
flist0 = []
for i in names:
    subdf = df1[df1['Symbol'] == i]
    m = ARIMA(list(subdf['VWAP']), order=(1, 1, 0))
    mlist0.append(m)
    flist0.append(m.fit(disp=0))
# The AIC decreases for the first three stocks, and increases for the 4th and
# 5th, indicating different stocks need different models.
includema = []
for i in range(50):
    includema.append(flist0[i].aic > flist[i].aic)
pd.value_counts(includema)

## Model diagnostics and improvements

# Use the in-sample lagged values to predict the time series
fig, ax = plt.subplots(10, 5, figsize=(15, 20))
for i in range(50):
    if(includema):
        flist[i].plot_predict(dynamic=False, ax=ax[i // 5, i % 5])
    else:
        flist0[i].plot_predict(dynamic=False, ax=ax[i // 5, i % 5])
    ax[i // 5, i % 5].set_title(names[i])
fig.tight_layout()
plt.savefig('p4.png')

# Future forecast examples
fig, ax = plt.subplots(10, 5, figsize=(15, 20))
for i in range(50):
    if(includema):
        forecast, b, ci = flist[i].forecast(200, alpha=0.05)
    else:
        forecast, b, ci = flist0[i].forecast(200, alpha=0.05)
    subdf = df1[df1['Symbol'] == names[i]]
    ax[i // 5, i % 5].plot(list(subdf['VWAP']))
    idx = range(len(subdf['VWAP']), 200+len(subdf['VWAP']))
    ax[i // 5, i % 5].plot(idx, forecast)
    ax[i // 5, i % 5].fill_between(idx, ci[:, 0], ci[:, 1], 
                 alpha=0.15)
    ax[i // 5, i % 5].set_title(names[i])
    ax[i // 5, i % 5].set_xticks([])
fig.tight_layout()
plt.savefig('p5.png')

# Model improvement example
import pmdarima as paim
subdf = df1[df1['Symbol'] == names[0]]
m1 = paim.auto_arima(subdf['VWAP'], start_p=1, start_q=1, test='adf',
                     max_p=3, max_q=3)
m1.summary() # The chosen model was ARIMA(1, 0, 1), which is a good fit.
ls0[0] # Indeed, differencing is not needed for the stock 'ADANIPORTS'.
subdf = df1[df1['Symbol'] == names[1]]
m2 = paim.auto_arima(subdf['VWAP'], start_p=1, start_q=1, test='adf',
                     max_p=3, max_q=3)
m2.summary() # The chosen model was ARIMA(0, 1, 0), which is a good fit.
# For 'ASIANPAINT', the 1-order difference series is close to a constant.
subdf = df1[df1['Symbol'] == names[7]]
m3 = paim.auto_arima(subdf['VWAP'], start_p=1, start_q=1, test='adf',
                     max_p=3, max_q=3, error_action='ignore')
m3.summary() # The chosen model was ARIMA(1, 1, 2), which is a good fit.
# For 'BPCL' second order MA term is needed.
# We can improve each of the models invidivually.
