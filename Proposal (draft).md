# Group 3 Project Proposal

## Topic: Regression topics for time series data

- Data manipulation: importing, formatting, or otherwise working with dates
and/or date-times
- Estimating regression coefficients
- I/O related topics: web-scraping or otherwise working with data from markup
languages (html, xml, json, etc)

## Group Members and Languages

 - Zhilin He (Python)
 - Chuwen Li (R)
 - Jialun Li (Stata)

## Data

### Dataset

Nifty 50 time series data:
[Link](https://www.kaggle.com/rohanrao/nifty50-stock-market-data)

### Source

NSE India: [Link](https://www.nseindia.com/)

### Variable descriptions

| Variables Name   |Variable Description     |
| ------------- |:-------------:|
| Date   | Date               |
| Symbol | Symbol of the stock (name, identifier)  |
| Series | Type of security (“EQ” for all rows)   |
| Prev Close | Previous day's close price |
| Open | Open price of day |
| High | Highest price in day |
| Low | Lowest price in day |
| Last | Last traded price in day |
| Close | Close price of day |
| VWAP | Volume Weighted Average Price |
| Volume | Volume |
| Turnover | Turnover |
| Trades | Number of Trades (Half missing) |
| Deliverable Volume | Amount of deliverable volume (7\% missing) |
| \%Deliverable | Percent of deliverable volume (7\% missing) |
 
## Collaboration plan
 
 - Communicate using Google Docs and the GitHub repository
 
## Question
 
 **What’s the seasonal trend for prices and turnovers of the nifty 50 stocks?**
 
## Packages used
 
 - Python: numpy, pandas, matplotlib, scipy, sklearn
 - R:
 - Stata:

## Models

 - Handling Missing Values: Variable deletion and linear interpolation
 - Main model for interpretation and prediction: Autoregressive integrated
 moving average model

## Outline

 - Determining which dataset(s) to use and which attributes to use.
 - Data cleaning. Handling Missing values (If the attribute(s) contains missing
 values)
 - Plot the data and construct the model (Which attributes we want to use, like
 which one is the output/response and which one(s) are the input.
 - A sample model can be expressed as: y<sub>t</sub> =
2X<sub>t-1</sub>-X<sub>t-2</sub>, where X is the matrix containing the
predictors **Prev Close** and **Volume**.
 - Model selection can be done by selecting by AICs or BICs.
 - Estimate the model coefficients by various methods like MLE and LR ratio,
 and construct confidence intervals.
 - Re-evaluate the model by statistical tests.
 
## References
 
A modern Time Series tutorial:
[Link](https://www.kaggle.com/rohanrao/a-modern-time-series-tutorial)
 
ARIMA model in Wikipedia:
[Link](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)

