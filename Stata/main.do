*-----------------------------------------------------------------------------*
* Stats 506, Fall 2020 
* Group Project, Stata Part
* 
* ///TODO
* Brief Introductions
* Brief Introductions
* Brief Introductions
* Brief Introductions
* Brief Introductions
* Brief Introductions
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
drop prevclose last trades turnover deliverablevolume deliverble
rename date2 date
label variable date "Date"

save NIFTY_clean, replace

// Data Visualization --------------------------------------------------------*
/// May split the symbol to 2 parts by the volume/vwap

* Numerical summaries
use NIFTY_clean, clear
/// TODO: The line below is too long
collapse (mean) open_mean = open (sd) open_sd = open (mean) high_mean = high (sd) high_sd = high (mean) low_mean = low (sd) low_sd = low (mean) close_mean = close (sd) close_sd = close (mean) vwap_mean = vwap (sd) vwap_sd = vwap, by(symbol)
export excel using summary.xlsx, firstrow(variables) replace

* Graph for high / low stock price
use NIFTY_clean, clear
graph twoway line high low date, by(symbol)
graph export highlow.png, width(1920) height(1080)

* Graph for open / close stock price
graph twoway line open close date, by(symbol)
graph export openclose.png, width(1920) height(1080)

* Candle Charts
gen redgreen = cond(open > close, "r", "g")
label variable redgreen "RedorGreen"
/// TODO: The line below is too long
graph twoway rbar open close date if redgreen == "g", color("green") barwidth(.8) by(symbol) || rbar open close date if redgreen == "r", color("red") barwidth(.8) by(symbol) || rspike high low date if redgreen == "g", color("green") lwidth("vthin")  by(symbol) || rspike high low date if redgreen == "r", color("red") lwidth("vthin") by(symbol)
graph export candlechart.png, width(1920) height(1080)

// Model Selection (Mainly focus on 'vwap')

* compute the autocorrelation and partial autocrrelation plots

levelsof(symbol), local(stocksymbols)

foreach sym of local stocksymbols {
	use NIFTY_clean, clear
	display "`sym'"
	keep if symbol == "`sym'"
	tsset date
	ac vwap
	graph export acf_`sym'.png
	pac vwap
	graph export pacf_`sym'.png
	* Try three different models and show their AICs and BICs
	arima vwap, ar(1)
	estat ic
	mat l1 = r(S)
	arima vwap, ar(2)
	estat ic
	mat l2 = r(S)
	arima vwap, ar(1) ma(1)
	estat ic
	mat l3 = r(S)
	putexcel set model_selection_`sym', replace
	putexcel A1 = "Model Description"
	putexcel A2 = "AR(1) Model"
	putexcel A3 = "AR(2) Model"
	putexcel A4 = "ARMA(1,1) Model"
	putexcel B2 = l1
	putexcel B3 = l2
	putexcel B4 = l3
	putexcel clear
}

* Select ARIMA(1,0,1) model and plot the fitted value against original ones

use NIFTY_clean, clear

levelsof(symbol), local(stocksymbols)

foreach sym of local stocksymbols {
	use NIFTY_clean, clear
	keep if symbol == "`sym'"
	tsset date
	arima vwap, ar(1) ma(1)
	outreg2 using arimaout_`sym'.docx
	predict vwap_p
	/// TODO: The line below is too long
	graph twoway line vwap date, lwidth("vthin") color("blue") || line vwap_p date, lwidth("vthin") color("red") lpattern("dash")
	graph export fitted_`sym'.png
}

