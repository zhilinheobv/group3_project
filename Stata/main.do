*-----------------------------------------------------------------------------*
* Stats 506, Fall 2020 
* Group Project, Stata Part
* 
*
*
*
*
*
*
*
*
* Author: Jialun Li, Chuwen Li, Zhilin He, Group 3
* Updated: November 11, 2020
*-----------------------------------------------------------------------------*
// 79: -----------------------------------------------------------------------*


// Set up --------------------------------------------------------------------*
import delimited NIFTY50_all.csv, clear


// Data Cleaning -------------------------------------------------------------*
gen date2 = date(date, "YMD")
format date2 %tdCCYY-nn-dd
drop date series
drop last trades turnover deliverablevolume deliverble
rename date2 date
label variable date "Date"

// Candle Chart --------------------------------------------------------------*
gen redgreen = cond(open > close, "r", "g")
label variable redgreen "RedorGreen"
graph twoway rbar open close date if redgreen == "g", color("green") barwidth(.8) by(symbol) || rbar open close date if redgreen == "r", color("red") barwidth(.8) by(symbol) || rspike high low date if redgreen == "g", color("green") lwidth("vthin")  by(symbol) || rspike high low date if redgreen == "r", color("red") lwidth("vthin") by(symbol)
graph export candlechart.png, width(1920) height(1080)
