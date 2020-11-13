*-----------------------------------------------------------------------------*
* Stats 506, Fall 2020 
* Group Project, Stata Part
* 
* Author: Jialun Li, Chuwen Li, Zhilin He, Group 3
* Updated: November 11, 2020
*-----------------------------------------------------------------------------*
// 79: -----------------------------------------------------------------------*


// Load Data------------------------------------------------------------------*
import delimited NIFTY50_all.csv, clear


// Data Cleaning -------------------------------------------------------------*
gen date2 = date(date, "YMD")
format date2 %tdCCYY-nn-dd
drop date series
drop trades deliverablevolume
rename date2 date
label variable date "Date"

* Replace Symbol Names
replace symbol = "ADANIPORTS" if symbol == "MUNDRAPORT"
replace symbol = "AXISBANK" if symbol == "UTIBANK"
replace symbol = "BAJFINANCE" if symbol == "BAJAUTOFIN"
replace symbol = "BHARTIARTL" if symbol == "BHARTI"
replace symbol = "HEROMOTOCO" if symbol == "HEROHONDA"
replace symbol = "HINDALCO" if symbol == "HINDALC0"
replace symbol = "HINDUNILVR" if symbol == "HINDLEVER"
replace symbol = "INFY" if symbol == "INFOSYSTCH"
replace symbol = "JSWSTEEL" if symbol == "JSWSTL"
replace symbol = "KOTAKBANK" if symbol == "KOTAKMAH"
replace symbol = "TATAMOTORS" if symbol == "TELCO"
replace symbol = "TATASTEEL" if symbol == "TISCO"
replace symbol = "UPL" if symbol == "UNIPHOS"
replace symbol = "VEDL" if symbol == "SESAGOA"
replace symbol = "VEDL" if symbol == "SSLT"
replace symbol = "ZEEL" if symbol == "ZEETELE"


save NIFTY_clean, replace

// Data Visualization --------------------------------------------------------*

use NIFTY_clean, clear

* Take the stock "ADANIPORTS" as an example

keep if symbol == "ADANIPORTS"

graph twoway line vwap date, color("blue") xtitle("Days") ytitle("Volume weighted average price")
graph export vwap_data.png, replace
graph twoway line volume date, color("blue") xtitle("Days") ytitle("Volume")
graph export vwap_data.png, replace
graph twoway line turnover date, color("blue") xtitle("Days") ytitle("Turnover")
graph export vwap_data.png, replace


// Model Selection (Mainly focus on 'vwap')


* Augmented Dickey-Fuller Test for all stocks

use NIFTY_clean, clear

levelsof(symbol), local(sbls)

global stocksymbols "EICHERMOT INFOSYSTCH NESTLEIND SHREECEM"

foreach sym of local sbls {
	use NIFTY_clean, clear
	keep if symbol == "`sym'"
	tsset date
	dfuller d1.vwap
}

* Compute the autocorrelation and partial autocrrelation plots

use NIFTY_clean, clear

levelsof(symbol), local(sbls)

local sbls_f8 = "ADANIPORTS ASIANPAINT AXISBANK BAJAJ-AUTO BAJAJFINSV BAJFINANCE BHARTIARTL BPCL"

foreach sym of local sbls_f8 {
	use NIFTY_clean, clear
	keep if symbol == "`sym'"
	tsset date
	ac vwap
	graph export acf_`sym'.png
	pac vwap
	graph export pacf_`sym'.png
}

* Fit ARIMA(1,1,1) model and ARIMA(1,1,0) model, and predict using the model 
* with lower AICs

use NIFTY_clean, clear

local sbls_f5 = "ADANIPORTS ASIANPAINT AXISBANK BAJAJ-AUTO BAJAJFINSV"

foreach sym of local sbls_f5 {
	use NIFTY_clean, clear
	keep if symbol == "`sym'"
	tsset date
	arima vwap, arima(1,1,1)
	estat ic
	mat l_aim = r(S)
	scalar aic_aim = l_aim[1,5]
	arima vwap, arima(1,1,0)
	estat ic
	mat l_ai = r(S)
	scalar aic_ai = l_aim[1,5]
	if aic_aim > aic_ai {
		arima vwap, arima(1,1,0)
		predict vwap_p
		gen vwap_p = vwap_pd + vwap
		graph twoway line vwap date, lwidth("vthin") color("blue") || line vwap_p date, lwidth("vthin") color("red") lpattern("dash")
		graph export fitted_`sym'.png
	} 
	else {
		arima vwap, arima(1,1,1)
		predict vwap_pd
		gen vwap_p = vwap_pd + vwap
		graph twoway line vwap date, lwidth("vthin") color("blue") || line vwap_p date, lwidth("vthin") color("red") lpattern("dash")
		graph export fitted_`sym'.png
	}
}

