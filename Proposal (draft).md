# Group 3 Project Proposal

## Topic: Splines Functions in Time Series Regression

- De-trend
- Polynomial Regression vs Cubic Spline vs ARIMA
- Graphic

## Group members and languages

 - Zhilin He (Python)
 - Chuwen Li (R)
 - Jialun Li (Stata)

## Data

### Dataset

Volumes of Microsoft Traded (6M):
[Link](https://www.nasdaq.com/api/v1/historical/MSFT/stocks/2020-05-02/2020-11-02)

### Source

Nasdaq: [Link](https://www.nasdaq.com/market-activity/stocks/msft/historical)

### Variable descriptions

| Variables Name   |Variable Description     |
| ------------- |:-------------:|
| Date   | Date               |
| Close/Last | Close/Last traded price of day |
| Volume | Volume |
| Open | Open price of day |
| High | Highest price in day |
| Low | Lowest price in day |
 
 
## Question
 
 **What’re the differences among Polynomial Regression, Cubic Spline, 
 and ARIMA in terms of the data fitting and forecasting?**
 
## Packages used
 
 - Python: numpy, pandas, matplotlib, scipy, sklearn
 - R: dplyr, forecast, astsa, splinef, ggplot2, 
 - Stata: outreg2, 

## Models

 - 3 models for comparison: 
   - Polynomial Regression
   - Cubic Spline
   - Autoregressive integrated moving average model (ARIMA)

## Outline

 - Data cleaning. Handling Missing values (If the attribute(s) contains missing
 values)
 - Plot the data to view the trend and determine de-trend stategy
 - Construct 3 models and plot them together
   - A sample model can be expressed as: y<sub>t</sub> =
2X<sub>t-1</sub>-X<sub>t-2</sub>, where X is the matrix containing the
predictors **Prev Close** and **Volume**.
 - Model comparison: AICs, residual plots


 
## References
 
A modern Time Series tutorial:
[Link](https://www.kaggle.com/rohanrao/a-modern-time-series-tutorial)
 
ARIMA model in Wikipedia:
[Link](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average)

