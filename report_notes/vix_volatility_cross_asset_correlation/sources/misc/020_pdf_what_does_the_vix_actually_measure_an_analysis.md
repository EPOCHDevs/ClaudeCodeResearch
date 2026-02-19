---
url: https://www.acrn-journals.eu/resources/jfrp201402f.pdf
title: [PDF] WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF ...
domain: misc
crawled_at: 2026-02-04T08:07:27.067753+00:00
source: exa_search
author: Merav Ozair
chart_count: 0
image_links:
outbound_links:
---

ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
83
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS 
OF THE CAUSATION OF SPX AND VIX
Merav Ozair†
† Department of Finance and Risk Engineering, Polytechnic Institute at NYU, USA
Abstract. We examine the causality relationship between the S&P500 (SPX) and the 
VIX. Our contention that a circular mechanism which “feeds” itself that can be 
explained by “cause and effect”, is supported by the empirical findings on the 
intraday, minute bar, time series of the SPX and the VIX. The findings are supported 
across different samples and estimation models and show that: (1) the SPX shock to 
the VIX time series is not only significant but also persistent; (2) the VIX follows a 
serial pattern of significant reversal (in the first lag) followed by momentum in the 
subsequent lags (and beyond the first 10 minutes); (3) the VIX endures a 
“permanent” market impact, while the SPX sustains a “transitory” one; and (4) the 
SPX shock on the VIX system remains in the system long enough to account for 70% 
of the variance of the VIX, suggesting a predictive power of the SPX to the current 
movement of the VIX. 
Keywords: causality, Vector Autoregressive (VAR), Volatility Index (VIX), S&P500 
Index (SPX), shocks, market impact, reversal, momentum, autocorrelation, 
cointegration
JEL Classifications: C58; C55; G02; G19
Introduction
Understanding market volatility has long been a quest of both researchers and practitioners. In 
1993, the Chicago Board Options Exchange (CBOE) introduced the CBOE Volatility Index 
(VIX), originally designed to measure the market’s expectation of 30-day volatility, implied by 
at-the-money S&P 100 Index option prices. In 2003, the VIX was updated to reflect a new way 
to measure volatility, based on the S&P500 Index (SPX) and estimates expected volatility by 
weight- averaging a wide range of strike prices of put and call options on the SPX. Principally, 
the VIX supposed to capture the future volatility of the SPX, and hence predict the future
movement of the S&P500. However, does the VIX actually represent the future direction of the 
SPX in current market conditions? This is the primary question that we attempt to answer in this 
study.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
84
It has well been documented that implied volatility is a reasonable forecast of future realized 
volatility (e.g., Granger and Poon (2003), and Anderson, Bollerslev, Christofferson and Diebobld 
(2005) – for historical review). Surprisingly few prior studies deal with the topic of this paper -
the possible relationship between implied volatility and future stock returns. Yet, market 
participants, in particular traders, are well aware of it. A widespread belief among them holds 
that swings in implied volatility value are associated with fear in the market, whereas a decline 
indicates complacency. As a measure of fear and complacency, implied volatility is often used 
as a contrarian indicator: prolonged and/or extremely high VIX readings indicate a high degree 
of anxiety – or even panic – among option traders, and are regarded as a bullish indicator1. 
Prolonged and/or extremely low readings indicate a high degree of complacency, and are 
generally regarded as a bearish indicator. In 2008, the VIX had remained in the low 20’s when 
all knew that problems were spinning out of control, and later in the year spiked, correcting its 
previous assumptions. It spiked, however, far beyond reality as panic drove option premiums 
(i.e., insurance prices) into the stratosphere. It again (quite quickly) over compensated as it fell. 
The VIX suffered huge whipsaws in 2009, 2010 and 2011 trying to over compensate and find 
some realm of equilibrium between perception and math. 
The literature examining VIX primarily focus on the predictive power of the VIX, and 
hence assumes that the VIX actually measures the forward 30-day volatility of the S&P 500 and 
can predict the S&P500 movement a month ahead. Doran, Goldberg and Ronn (2008) use the 
VIX as a proxy for the S&P 500 Index volatility in their time-varying expected S&P 500 return 
model. Bekaert and Hoerova (2013) decompose the square VIX index into the Conditional 
Variance of stock returns (CV) and the equity variance premium (VP). Using different volatility 
forecasting models they examine the predictive power of the VIX and its two components: stock 
market returns and economic activity. They find that the VP is a significant predictor of stock 
returns, but the CV mostly is not. CV, however, robustly and significantly predicts economic 
activity with negative sign, whereas VP has no predictive power for future ecomonic output 
growth. Others study the VIX in comparison to the GARCH model and investigate whether 
different types of GARCH models fit the CBOE VIX. (Hao and Zhang (2013), Lui and Qiao 
(2012)). The key finding in this line of research is that the GARCH model (examined with 
different types of GARCH) consistently underestimates the VIX, and concludes that the 
discrepancy is due to the variance risk premium not captured by the GARCH. 
These studies not only assume the predictive power of the VIX, but also assume it is 
“priced” correctly. The VIX is a measure of implied volatility and is based on options prices 
(i.e., the option premium – how much market participants are willing to pay for protection from 
market movements). In that sense, we assume that market participants “know” the “correct” 
price of the option. If we believe this is indeed true then we can also believe that the implied 
volatility represented by the VIX, calculated from option prices, is also a correct measure of the 
future volatility of the market and can thus predict the movement of the S&P 500.
 
1 On the day of the “flash crash” when the Dow plummeted 900 point just to recover in minutes, the VIX spiked 
more than 60% , supporting the “fear indicator” hypothesis.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
85
There is (to some extent) a circular mechanism that “feeds” itself. The VIX, as a measure of 
implied volatility, is a function of the options and the underlying (i.e., the SPX). When market 
participants view the value of the quoted VIX they may react to it either with adjustments to their 
option prices or with actions in the market (i.e., the S&P 500). This mechanism may explain
why during the years between 2008 and 2011, the VIX over/under reacted and then corrected 
itself. In order to decipher this mechanism and better understand the “cause and effect” 
relationship we postulate two main (and one secondary) hypotheses: (1) If VIX is a forward 
looking measure of the S&P500 future volatility, we would expect a leading relationship,
meaning the VIX movement leads the S&P 500 and hence, we would expect that VIX “granger 
causes” the S&P 500 Index; (2) the VIX measure is a function of the S&P 500, and hence 
implicitly determined by the values of the S&P 500 Index. Therefore, this type of relationship 
implies that the S&P 500 “granger causes” the VIX; (3) Secondary to the main hypotheses, a 
third hypothesis states a bi-directional causality relationship between the VIX and the SPX(but 
also postulating that the impact of the S&P 500 Index (SPX) is the stronger and the more 
significant of the two.)
This paper is the first to examine causality between the implied volatility, the VIX, and its 
underlying, the SPX, and sheds light on the implication of the VIX calculations. Previous 
studies have examined the correlation between VIX and SPX (Zheng (2012), Brenner, Shu and 
Zhang (2010), Carr and Wu (2006) and Whaley (2008)). Whaley (2008), in his simple 
regression analysis of daily changes of the VIX to daily changes of the SPX and a conditional 
rate of change in the S&P 500 on the market going down or up, finds that: (1) negative 
relationship of change in VIX to change in S&P 500; (2) the relation in the VIX and the SPX is 
asymptotic; (3) VIX is more a barometer of investors’ fear of the downside than it is a barometer 
of investors’ excitement (or greed) in a market rally. The evidence in Whaley’s study merely 
documents correlation and is not intended to express causality. 
We examine the intraday interaction of the two minute bar time-series of the VIX and the 
SPX2. Our four main findings offer a new insight as to the interactions of the VIX quotes with 
the market SPX movement and to the implications of the VIX calculations. First, SPX 
significantly and robustly “granger causes” the VIX. This causality test is supported and is 
evident not only in any sample examined but also by using different types of analysis. The VIX 
causality, however, even though indicated by the Granger Causality test that we have a bidirectional causality relationship, is not supported by any other tests, such as the estimated VAR 
model coefficients but in particular the Impulse Response and the Variance Decomposition 
analyses. These two tests evidently show that the SPX is certainly not affected by the VIX, 
whereas the VIX, on the contrary, is significantly affected by the SPX and about 40% of its 
variance can be explained by the SPX movement. 
Second, we observe a pattern in the minute returns/level time series and especially in the 
VIX time series. The SPX seems to strongly and positively relate to its first lag. This impact 
dies, on average after the fourth lag, and the significance of the coefficients on the second to 
fourth lags is reduced significantly. The VIX, however, is significantly related to all lags 
 
2 Ozair (2011) examine the interaction of the daily time series of the SPX and VIX and find a consistent and 
significant ganger causality of the SPX on the VIX, and no opposite causality relationship. 
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
86
estimated in the model and follows a pattern which can be interpreted as a correction followed by 
a momentum, whereas the magnitude of the correction (observed in the first lag) is, on average, 
about six fold compared to following lags. Hence, one can explain the VIX minute changes or 
level values, that on average there is an immediate correction (or reversal) and then some 
element of momentum (which will depend on the magnitude of the change in the VIX for that 
previous minute). This can explain the over/under reaction of the VIX and the correction that 
follows, which implies that VIX’s first reaction tends to over/under estimate the shock/news. 
Third, in every sample and estimation method (VAR or VECM; returns versus levels) we 
observe that the current level of VIX is related/affected by all lags (with the exception of the 
second lag) included in the estimation model. This implies that the VIX time series is much 
more autocorelated than the SPX. Any shock to the SPX will die relatively quickly, while the 
VIX will carry on the impact of a shock for a relatively long period of time. In Market 
Microstructure literature, we can refer to that as a “permanent” market impact – VIX has a 
“permanent” market impact whereas the SPX market impact seems to be more transitory. This 
observation is of particular interest when developing best executions strategies and optimizing 
transaction costs3.
Forth, there is a cointegration relationship of first order between the VIX and the SPX time 
series. The main finding when analyzing the VECM model lies in the Variance Decompositions. 
This variance analysis shows that in the first period following the shock the decomposition of 
variance for the VIX is 30% - 70%, explained by the SPX and VIX respectively. This 
decomposition, however, flips with time – i.e., by the twelfth period (and even sooner) the 
decomposition become 70%-30% explained by the SPX and VIX, respectively. This suggests 
that the SPX shock stays in the VIX system longer, which will also suggest that one can 
“predict” the direction (and to some degree the magnitude) of the VIX in the next ten minutes 
simply by observing the current movement of the SPX. This is a paramount observation, if one 
wishes to make trading decisions (whether as a trader or a hedger or an investor). It also 
suggests that what the current level of the VIX captures is merely the current changes in the SPX 
and has no predictive power or assessment on the future movement of the SPX. 
Collectively, these findings contribute to the growing literature on the Variance Risk 
Premium and the VIX. Our paper may offer an explanation (or alternative explanation) to the 
aforementioned research findings – as to what it measures, what it may predict (if anything) and 
its validity and correctness. For example, the inability to reconcile the discrepancies of the 
GARCH model with the implied volatility of the VIX can be explained by the pattern of the VIX 
time series (as it reacts to shocks to the system) that is observed in this study. 
The reminder of the paper is organized as follows. Section 2 describes the data and provids 
descriptive statistics and explanation on special irregularities within the data sample (section 
2.1); and descriptions of the research method and some hypotheses (section 2.2). Section 3 
reports the empirical analysis and the results for daily sub-samples and for the whole sample 
 
3 This should be examined on the tradable vehicles of the VIX, such as the ETN’s on the VIX and the VIX futures. 
It is very likely that one should, observe the same pattern with the VIX tradable vehicles as they are its derivative.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
87
period. Section 4 provides further analysis and examination of the results discussed in section 3. 
Section 5 illustrates the applicability of the findings in the study and section 6 concludes.
Data and Estimation Procedures
Data: Description, Cleaning and Statistics
To examine the relationship between SPX and VIX, we use the Bloomberg data4 (level I) 
intraday tick and minute bar. The data have been retrieved from the Bloomberg terminal and 
have been collected incrementally over time5. We have collected over a year worth of data from 
August 9th 2012 to October 3th 2013 for the tick data and for the minute bar data from October 5th
2012 to August 9th 2013 (see information in table 1). For the SPX and VIX we have 1,415,935 
and 464,215 observation for the tick data, respectively; and minute bar data 100,323 and 99,950 
observations, respectively. The data consists of 421 calendar days but only 289 trading days due 
to weekend and national holidays where the market is closed and two special days (which are 
unique to this period of time) due to hurricane Sandy (in total 12 days where the market closed 
other than on weekends). There were also three half trading days, when the market closed at 
1pm a day before a major national holiday (see table 2 for details). 
The tick data include date and timestamp and price (i.e., the level quote of the index). The 
S&P 500 index is quoted every five seconds during the trading hours of the day (i.e., 9:30am to 
4pm)6, hence the tick data has 12 entries during each minute. The VIX, on the other hand, is 
quoted only every 15 seconds during the trading hours of the day, and therefore its tick data has 
4 entries during each minute. The S&P 500 index quotes starts exactly with the opening of the 
financial market (i.e., 9:30am), the VIX, however, begins its quotes, for most days7, during the 
second minute of the trading day. Some minutes have different number of ticks, are very few and 
negligible, and account for less than 0.001% and 0.01% for the SPX and VIX respectively for the 
entire sample8.
 
4 Bloomberg receives its market data through NYSE data feed.
5 Historical intraday data is available for download from Bloomberg terminal a maximum of 140 days ago.
6 For more information see http://us.spindices.com/indices/equity/sp-500
7 Out of 289 trading days in the sample, we observe the one minute delay in 279 trading days (i.e., 96.5% of trading 
days); for more information see table 1.
8 More information is available from the author.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
88
Table 1: Sample Data Summary
Data Type Sample Period Observations (1) Calendar Days Trading Days (2) 
Historical Intraday Tick (3) 8/9/12-10/3/13
SPX: 1,415,935 
VIX: 464,215
421 289
Historical Intraday Minute Bar (4) 10/5/12-10/3/13
SPX: 100,323 
VIX: 99,950
364 249
Inferred Intraday Minute Bar (5),(6) 8/9/12-10/3/13
SPX: 118,246 
VIX: 116,101
421 289
Table 2: Dates Market Closed During the Sample Period
Sep 3 2012 Labor Day
Oct 29 2012 Hurricane Sandy
Oct 30 2012 Hurricane Sandy
Nov 22 2012 Thanksgiving
Dec 25 2012 Christmas
Jan 1 2013 New Year
Jan 21 2013 MLK Day
Feb 18 2013 Washington's Birthday
Mar 29 2013 Good Friday
May 27 2013 Memorial Day
July 4 2013 Independence Day
Sep 2 2013 Labor Day
Notes:
The discrepancy in number of observations between SPX and VIX is 405: 126 due to missing intraday VIX data 
during trading hours; 279 due to 1-minute delay of VIX at the beginning of the trading day.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
89
Including 3 days where market closed at 1:00pm - 11/23/12, 12/24/12, 7/3/13
From Bloomberg Data Services Level 1
From Bloomberg Data Services Level 1
Inferred from Historical Intraday Tick
In all subsequent analysis, Intraday Minute Bar observations are limited to 9:30 AM to 4:01 PM of each trading day 
in the sample period, yielding 112748 SPX observations and 112343 VIX observations.
From the above description, it is clear that the entries of tick data for the VIX and SPX are not 
inline. For the purpose of conducting the analysis we had to synchronize the two time series 
(i.e., SPX and VIX), and chose to use the minute bar data9. To work with minute interval, we 
have transformed the tick data to minute intervals, after the transformation we ended-up with 
118,246 and 116,101 observations for the SPX and the VIX, respectively. We were able to 
retrieve minute data for Bloomberg from October 5th 2012 to October 3rd 2013. For the period 
October 5th 2012 to October 3rd 2013 we have compared our calculated minute entries with 
those quoted on Bloomberg terminal (see Table 3). There are very few discrepancies which 
account for less than .01% for both the SPX and the VIX, and the absolute value of differences 
with respect to Bloomberg’s data is also less than .01% for both the SPX and the VIX. Only in 
the case where there are discrepancies in the number of ticks per minutes, it seems that in these 
cases the Bloomberg tick data tend to be underestimated. The results of the comparison have 
supported our calculation of the minute bar and thus we will be using our calculated minute bar 
sample for the rest of the analysis in this research.
The “after trading hours” data (i.e., after 4pm) experience many irregularities which 
primarily stems from lack of liquidity (i.e., lower trading volume, larger quote spread and higher 
volatility) but also from computers’ delays. For this reason we have restricted our sample for 
each trading day to “normal” trading hours, 9:30am to 4:01pm (taking in consideration some 
adjustments that might occur after the close of the markets). The analysis thereafter is performed 
on “normal” trading hours10.
Intraday data exhibits irregularities such as, duplicate observations11, large sequence of 
missing data and significant outliers. We have addressed each issue with accordance to the 
treatment documented in the market microstructure literature and verified that our results are not 
a consequence of special irregularities that are associated with this specific dataset. Cleansing is 
an important aspect of computing realized measures. The literature suggests that when there are 
mis-recordings of prices or hit large amounts of turbulence at the start or the end of the trading 
day then they may sometimes give false signals. Barndorff-Nielsen, Hansen, Lunde and 
Shephard (2009) have studied systematically the effect of cleaning on realised kernels, using 
cleaning methods which build on those documented by Falkenberry (2002) and Brownless and 
Gallo(2006). 
 
9 It is quite common in the market microstructure literature to use 1 minute or 5 minute bar as the appropriate data 
frequency for the analysis (see Madhavan (2000))
10 This is consistent with the market microstructure literature (see for example Madhavan (2000)).
11 By duplicates, we mean that more than one tick entry at the same second (not necessarily with the same value.)
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
90
Table 3: Minute Bar Discrepancies (1)
A comparison of minute discrepancies in the Historical Intraday Minute Bar and the Inferred Intraday Minute Bar for SPX and VIX, in the sample period Oct. 5 
2012 to Oct. 3 2013. In this table, the “General” row represents the number of historical minute bar observations with one or more discrepancies. Each 
subsequent row indicated the number of discrepancies per variable.
Sample period: Oct. 5 2012 – Oct. 3 2013
SPX VIX
# Minutes with 
Discrepancy Sample size Accuracy(3)
Average 
difference(4)
# Minutes with 
Discrepancy Sample size Accuracy
Average 
difference
General 53 100323 99.9472% 44 99950 99.9560%
OPEN ** 18 100323 99.9821% 0.0042% 12 99950 99.9880% 0.0509%
HIGH 18 100323 99.9821% 0.0057% 11 99950 99.9890% 0.0782%
LOW 15 100323 99.9850% 0.0087% 9 99950 99.9910% 0.0556%
LAST_PRICE 18 100323 99.9821% 0.0082% 8 99950 99.9920% 0.0938%
NUMBER_TICKS 50 100323 99.9502% 117.4067% 43 99950 99.9570% 107.0833%
Notes: 
“minute discrepancy” is defined as when any variable of historical and inferred values of Intraday minute bar data are not equivalent. The historical minute bar 
data source includes the following variables: OPEN, HIGH, LOW, LAST_PRICE and NUMBER_TICKS.
For the definition of “minute bar” and “inferred minute bar” see Table 1.
Accuracy is percent of total minute observations, generally and per variable, without discrepancies in the sample period.
1 The Average Difference is the average of the absolute value of the differences between the number of Historical Intraday Minute Bar variable discrepancies 
and the number of Inferred Intraday Minute Bar variable discrepancies. Each difference is normalized (divided) by the number of Historical Intraday Minute Bar 
variable discrepancies.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
91
Table 4: Frequency of Values for VIX and SPX.
Sample period: Aug 9 2012 – Oct 3 2013, 9:30 AM – 4:01 PM for each trading day.
Number of ticks different than 4 for the VIX Number of ticks different than 12 for the SPX
Value of 
the tick Frequency W/ complements (1) Percentage (2)
Value of 
the tick Frequency W/ complements (1) Percentage(2)
1 18 0 0.00% 1 1 1 100.00%
2 12 1 8.33% 2 1 1 100.00%
3 124 33 26.61% 3 1 0 0.00%
5 22 21 95.45% 5 2 1 50.00%
6 1 1 100.00% 6 3 0 0.00%
8 2 2 100.00% 7 1 0 0.00%
Total number of minutes for the VIX 112,343 8 1 0 0.00%
Number minutes with 4 ticks 112,164 99.84% 9 3 0 0.00%
Number minutes that don't have 4 ticks 179 0.16% 10 3 0 0.00%
With complements 58 0.05% 11 660 586 88.79%
Without complements 121 0.11% 13 843 586 69.51%
19 1 1 100.00%
22 1 1 100.00%
23 1 1 100.00%
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
92
Number of ticks different than 4 for the VIX Number of ticks different than 12 for the SPX
Value of 
the tick Frequency W/ complements (1) Percentage (2)
Value of 
the tick Frequency W/ complements (1) Percentage(2)
Total number of minutes for the SPX 112,748
Number minutes with 12 ticks 111,226 98.65%
Number minutes that don't have 12 ticks 1,522 1.35%
With complements 1,178 1.04%
Without complements 344 0.31%
Notes: 
Defined as the minute together with its immediate preceding or succeeding minute averaged at 4 or 12 ticks
Percentage of minutes with complements relative to that particular frequency group
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
93
Number of total ticks per day is 4,704 (12 ticks per minute and 392 minutes) and 1,616 (4 ticks 
per minute and 391 minutes) for the SPX and VIX, respectively. This total number of ticks per 
day is stable 99.97% and 99.99% of the sample for the SPX and the VIX, respectively. Careful 
look at the data reveals that a “duplicate” may not be a “real duplicate” but simply an adjustment 
of missing consecutive entries in the preceding minute or the following minute. The SPX and 
the VIX by construction of the index12 should be quoted every 5 and 15 seconds which 
correspond to 12 and 4 entries per minute, respectively. If a minute records less than the amount 
of quotes required by design of the index, that implies that the “delay” has happened due to 
technological problems with the reporting system either on Bloomberg or the Exchanges, and 
therefore at the beginning of the following minute an adjustment to these missing ticks appears 
to complement and reflect the total 12 tick for the SPX or the 4 ticks for the VIX. (For example, 
a duplicate for the SPX on 1/25/2013 at 11:11:05am of 7 reflects the complement to the merely 5 
ticks recorded in the previous minute 11:10am of that day13.) We can then conclude with 99.9% 
confidence that the data does not consist of any “real duplicate” but simply corrections to 
technology mishaps. 
Table 4 documents the minutes in the sample that has number of entries which are different 
than 12 for the SPX and 4 for the VIX. It shows that the SPX has 1,522 minutes (i.e., 1.3% of 
total minutes sample) that have number of entries different than 12; and the VIX has 179 minutes 
(i.e., 0.16% of total minute sample) that have entries different than 4. Most of these differences 
are complemented and adjusted with respect to the preceding or the following minute to form 
that on average the number of ticks per minutes is 12 or 4 for the SPX and VIX, respectively. 
The percentage of minutes with number of ticks different than 12 for the SPX and different than 
4 for the VIX, which are not complemented with its previous or following minutes is 0.3% and 
0.1% respectively.
The number of irregular ticks in the SPX is more than 8 time of the number of irregular 
minutes within the VIX, and it seems that it is concentrated in two particular month – August 
2012 and October 2012, and within these month it centres only in five days in August and 6 days 
in October. These phenomena might be explained by the very low volume (lowest in the past 
five years) the market has experienced in August 2012 and by the weak corporate results during 
the month of October 201214. It should be noted that all days with irregular ticks in August and 
October of 2012 had been complemented with tick in the following or previous minute to 
account for 12 or 4 ticks for the SPX and VIX, respectively.
Another problem that these data might encounter is significant outliers. Consistent with the 
data cleansing procedure performed by Oxford-Man Institute of Quantitative Finance (Realized 
Library), we consider an outlier with respect to the median absolute minute change for the day 
 
12 See http://www.cboe.com/micro/vix/vixwhite.pdf for the methodology of the VIX index and https://www.spindexdata.com/idpfiles/indexalert/prc/active/whitepapers/Methodology_SP_US_Indices_Web.pdf for the S&P500
Index methodology
13 More information can b provided form the author
14 The market performance might be an explanation to the unusual tick irregularities, but that not to dismiss the 
possibility that it has also could have happened by chance with no specific explanation behind it.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
94
(as our preliminary examination) and then with respect to the median absolute minute returns for 
the day.
Starting with analysing absolute minute changes, we first look at absolute changes that are at or 
higher than 50 times the median of the absolute change of that day. In this case, the SPX had no 
outliers and the VIX only had four. That seems to not be the correct measure for outliers for our 
sample and after further investigation 25 times the median of the absolute change on each day 
appeared to be as a better measurement. In this case we found 7 such events for the SPX and 91 
events for the VIX. 
The analysis for outliers using absolute returns (those which are 25 times the median 
absolute return of each day) reveals some interesting features of the data sample. The SPX has 
seven such outliers concentrated within 4 trading days and the VIX has 91 outliers which are 
concentrated within 50 trading days. For both the SPX and the VIX, the minimum outliers is 
about 25 times the median of the absolute return of the day and the maximum outlier is about 85 
times and 73 times the median absolute daily return for the SPX and the VIX, respectively, 
whereas the median outlier is about 27 and 30 times the daily median absolute return for the SPX 
and the VIX, respectively. As is expected in most intraday data samples we observe that for the 
VIX 34% of the outliers appear during the first half hour of the trading day and about 24% of the 
outliers appear during the last half hour of the trading day, which sum-up to about 58% of all 
outliers in the data sample. The rest are spread out somewhat evenly during the trading day, 
except for the second half hour of the trading day (i.e., 10am to 10:30am) which correspond to 
about 10% of all outliers in the sample (see table 5). 
Table 5: Outliers per 30 Minute Interval 
Sample period: Aug 9 2012 – Oct 3 2013, 9:30 AM – 4:01 PM for each trading day.
Interval VIX SPX
From To
Number 
of outliers Percentage
Number 
of outliers Percentage
9:30a 10:00a 31 34.07% 1 14.29%
10:01a 10:30a 9 9.89%
10:31a 11:00a 1 1.10%
11:01a 11:30a 2 2.20%
11:31a 12:00p 1 1.10%
12:01p 12:30p 1 1.10%
12:31p 13:00p 2 2.20% 1 14.29%
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
95
Interval VIX SPX
From To
Number 
of outliers Percentage
Number 
of outliers Percentage
13:01p 13:30p 5 5.49% 4 57.14%
13:31p 14:00p 4 4.40% 1 14.29%
14:01p 14:30p 3 3.30%
14:31p 15:00p 5 5.49%
15:01p 15:30p 5 5.49%
15:31pp 16:01p 22 24.18%
Total 91 100% 7 100%
Looking at the correlations of the number and size of the VIX outliers with the SPX absolute 
returns and their sign suggests interesting characteristics of the way VIX behaves in relation to 
movements in the SPX (see table 6). In this type of analysis we are more concerned with the 
direction of the relationship rather than its magnitude (as it will be difficult to obtain a significant 
magnitude considering the small sample of outliers). The number of VIX outliers per day has a 
negative correlation with both the SPX total return per day and the sign of its return. Both of 
these observations imply that we should expect more outliers (i.e., irregularities) in the VIX 
when the SPX moves down (i.e., negative returns). The analysis of the size of the VIX outlier 
with the SPX returns per day is less telling. With respect to the absolute SPX return it seems that 
the relationship is positive which would indicate that the higher the return (positive or negative) 
the larger is the VIX outlier. If instead of looking at the total return per day we consider the 
contemporaneous minute return or the preceding minute return, we then find that the size is 
negatively related to the sign of the previous minute return, which implies that if the SPX moved 
down in the previous minute it is likely that we would observe a large adjustment (i.e., change) 
in the VIX value. These observations insinuate that our Hypothesis 2 may have merit15. 
One of the problems one encounters with financial data is “missing data”. In the case on 
financial markets that could often happen due to technological system glitches16. The analysis 
shows that the SPX sample has no missing data, whereas the VIX data encountered a few days 
with missing data and one day in particular with significant gap in the data. 
 
15 Further discussion on the analysis of the examination of the hypothesis is section 2.2
16 For the past year we have experienced several technological systems mishaps – knight capital August 2012, 
Batched Facebook IPO April 2012, CBOE, April 2013, Nasdaq-NYSE AUGUST 2013, NYSE September 2013. 
These are only a few that were documented and reported to the news. In reality, however, one can observe glitches 
and technology mishaps almost every day, on a security basis. (the ones that are usually reported are the ones that 
have an impact on significant part of the financial market (and not simply an individual stock) and which last for 
more than a few minutes.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
96
Table 7 summaries the statistics with regards to the VIX missing data. There are nine 
trading days with missing data (account for 3.1% out of total trading days in the sample) and a 
total of 126 missing minutes (account for 0.1% for total trading minutes in the sample 
considering only trading hours 9:30am to 4:01pm, and 286 whole trading days and three half 
trading days – 112,748 minutes). Four days have only one missing minute and one day with two 
missing minutes, for these minutes we have interpolated the data to fill in for the missing 
minutes. Two days have three missing minutes and one day with ten missing minutes. For these 
days we have deleted these missing observations17. 
April 25, 2013, however, was an exceptional day. The CBOE experienced an outage that 
day since the opening of the trading day and resumed trading only at 1pm18. It is not unusual to 
see a trading delay in one of the 11 exchanges on which options are traded. This type of delay 
happens once a month. It is generally not too disruptive since banks can just reroute orders from 
one exchange to another. The S&P 500 options and the options on the CBOE Volatility Index 
(VIX), exclusively trade on the CBOE so there was no trading in those contracts while the 
CBOE was shut19. On April 25th the CBOE had an internal system issue caused by software 
problem and “not the result of any outside influence” or cyber-attack. Trading resumed in the 
S&P500 options contracts at 12:50 pm and in all other equity and ETF options opened by 1pm. 
Most of the trading functions were operating normally once they reopened, but some electronic 
methodology of confirming open outcry trades were being entered manually. 
Table 7 shows that the VIX on April 25, 2013 had missing data from 11:06am to 12:49pm 
(which account for 104 minutes). It is understandable that the VIX resumes activity around 
12:50pm, as the S&P and VIX options resume trading at that time. It is less clear why would 
Bloomberg show activity on the VIX form 9:30am to 11:05am, while the CBOE was down. The 
VIX quotes are derived (among other parameters) from the quotes of the underlying, S&P500 
and from the prices of the options on the S&P500, which only trade on the CBOE and on April 
25th, 2013 did not start trading before 12:50pm. Hence, it is unclear how those VIX quotes were 
calculated and whether they are reliable. For this reason we have decided to treat this outage on 
CBOE in the following way: (1) Include April 25th, 2013 in the sample but only for the trading 
 
17 There was no particular information relating for these minutes in terms of particular glitches in the system. Since 
we do not know the reason for its absence and a simple interpolation would have distorted the sequence of the data, 
we have decided to delete these observations. Even though there was no stated reason for the absence of these 
minutes, it does not mean that it could not have been a technical mishap of the system. Nonetheless, their deletion 
will have a miniscule effect on the total data and its analysis as a whole, on a daily basis (2% out of daily minutes) 
and most definitely on the whole sample period (0.005% of total trading minutes). 
18 The outage was the latest in a series of disruptions at exchanges, including Nasdaq’s high-profile flub with 
Facebook IPO in April 2012. It also comes at a time when the financial services industry has good reason for 
concern about network security due to hacks. Major banks have suffered numerous denial of service attacks on their 
website in recent months, and Charles Schwab was attacked just earlier that week. The CBOE stressed that it had 
not been hacked. 
19 It should be noted that the CBOE is the only exchange that rarely has any problems.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
97
period 12:50pm to 4:01pm; (2) delete April 25th, 2013 from the sample data; (3) do not perform 
any analysis on a daily basis20. 
To estimate the VAR model (as described below) we needed to calculate the minute 
returns21.We observe that the returns for the VIX and for the SPX have some minutes with zero 
returns: 1,956 minutes for the SPX and 49,439 minutes for the VIX, out of total 112,243 for the 
entire sample22, which account for 1.7% of total observations for the SPX and 44% of total 
observations for the VIX. This phenomenon is prevalent every trading day for the VIX and in 
286 days (out of the total 289 days in the sample) for the SPX. The effect of zero returns in the 
SPX sample data is quite negligible (see table 8). Considering that its number of zero returns 
within a trading day varies as minimum as 1 minute and as maximum of 16 minutes, 0.26% and 
4% of total minutes within the day and with a median of 7 minutes (i.e., 1.79%); and their 
appearance during the day is quite sporadic. Unlike the SPX the VIX experience quite a 
significant amount of zero returns during a trading day, this begs for a more thorough analysis as 
for the patterns of these zero returns and their relationship to movement of the SPX. 
 
20 We have decided to exclude this day from any daily analysis,as this is an unusual day and any results would be 
biased and specific to this particular event. Options (1) and (2) were performed for robustness test.
21 The minute returns are calculated as (
 
 
⁄ ) where t is minute.
22 After accounting for missing data and in the sample (see discussion on table 7)
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
98
Table 6: Correlation of outliers per day and the SPX total returns per day
Sample period: Aug 9 2012 – Oct 3 2013, 9:30 AM – 4:01 PM for each trading day.
Correlation
SPX total return 
per day
SPX absolute total 
return per day
Sign of SPX total 
return per day
Sign of SPX 
return for the 
minute
SPX return for 
the previous 
minute
Sign of SPX return for 
the previous minute
Number of outliers per day –
SPX 0.2647 0.1871 0.1956
Number of outliers per day –
VIX -0.104 0.1726 -0.1271
Size of VIX outliers (1) 0.2005 0.2324 0.1952 0.0711 0.118 -0.0078
Size of SPX outliers (2) 0.2337 0.2337 **
Notes: 
Outliers are defined as absolute returns minute by minute that are above 25 times of the median of absolute returns minute by minute for each day.
Average size of outliers in terms of the median of absolute returns for each day
All 4 days with outlier in SPX has positive total return in SPX.
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
99
Table 7: VIX Missing Data Statistics (1),(2)
Date
Minutes 
Missing Gap 1 Gap 2 Obs Mean
Standard 
Dev. Min Median Max Skewness Kurtosis
8/20/12 1 3:14 PM 390 14.32 0.1971 14.02 14.27 14.78 0.74 2.55
8/21/12 10 11:27 AM - 11:35 AM 11:38 AM 381 14.60 0.4130 14.04 14.58 15.44 0.35 1.94
8/29/12 2 9:58 AM 10:01 AM 390 16.68 0.1312 16.50 16.64 17.00 0.87 2.60
9/14/12 3 12:24 PM - 12:26 PM 388 14.36 0.3164 13.53 14.52 14.70 -1.32 3.57
1/11/13 1 4:00 PM 390 13.55 0.0882 13.37 13.53 13.78 1.00 4.06
1/25/13 1 2:49 PM 390 12.81 0.1003 12.50 12.82 12.99 -1.06 4.20
4/25/13 104 11:06 AM - 12:49 PM 287 13.42 0.2225 13.13 13.33 13.87 0.50 1.86
7/12/13 1 2:37 PM 390 13.93 0.0536 13.74 13.93 14.03 -0.82 4.24
9/16/13 3 1:40 PM - 1:42 PM 388 14.16 0.1577 13.87 14.15 14.47 0.10 2.03
Notes: 
Calculated from Historical Intraday Minute Bar data – see Table 1 Row 2 for details
Sample period: Aug 9 2012 – Oct 3 2013, 9:30 AM – 4:01 PM for each trading day.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
100
Table 8: Zero Return Descriptive Statistics 
This table lists descriptive statistics of the number of zero returns from minute to minute during normal trading hours. In the sample period: Aug 9 2012 – Oct 3 
2013, 9:30 AM – 4:01 PM for each trading day. (289 days with 0-returns in VIX, 286 days with 0-returns in SPX.)
Mean Std. Dev. Smallest
1% 
percentile
5% 
percentile
10% 
percentile
50% 
percentile
90% 
percentile
95% 
percentile
99% 
percentile Largest
# 0-return 
VIX per day 171.21 51.06 26 34 83 106 174 239 248 267 277
# 0-return 
SPX per day 6.86 3.13 1 1 2 3 7 11 13 15 16
% 0-return 
VIX per day 44.17% 12.97% 6.67% 8.72% 22.05% 28.13% 44.87% 61.28% 63.59% 68.46% 71.03%
% 0-return 
SPX per day 1.77% 0.82% 0.26% 0.26% 0.51% 0.77% 1.79% 2.81% 3.32% 4.09% 4.27%
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
101
Table 9: Correlations of Reruns 
This table provides information on the correlation of minute zero returns with in the day and the total return for the day (sign of the total return and the absolute 
value). In the sample period: Aug 9 2012 – Oct 3 2013, 9:30 AM – 4:01 PM for each trading day. (289 days with 0-returns in VIX, 286 days with 0-returns in 
SPX.)
# 0-return 
VIX per 
day
# 0-return 
SPX per 
day
% 0-return 
VIX per 
day
% 0-return 
SPX per 
day
Total 
return SPX 
per day
Total 
return 
VIX per 
day
Absolute total 
return SPX 
per day
Absolute total 
return VIX 
per day
Sign of total 
return SPX 
per day
Sign of 
total return 
VIX per 
day
# 0-return 
VIX per day 1
# 0-return 
SPX per day 0.4083 1
% 0-return 
VIX per day 0.9842 0.4118 1
% 0-return 
SPX per day 0.377 0.9833 0.4091 1
Total return 
SPX per day 0.2825 0.1429 0.2979 0.1491 1
Total return 
VIX per day -0.1919 -0.0931 -0.1948 -0.0907 -0.7688 1
Absolute total 
return SPX 
per day
-0.294 -0.259 -0.2974 -0.2557 -0.1326 0.196 1
Absolute total 
return VIX 
-0.2123 -0.1721 -0.2258 -0.18 -0.2065 0.2215 0.6633 1
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
102
# 0-return 
VIX per 
day
# 0-return 
SPX per 
day
% 0-return 
VIX per 
day
% 0-return 
SPX per 
day
Total 
return SPX 
per day
Total 
return 
VIX per 
day
Absolute total 
return SPX 
per day
Absolute total 
return VIX 
per day
Sign of total 
return SPX 
per day
Sign of 
total return 
VIX per 
day
per day
Sign of total 
return SPX 
per day
0.3042 0.1682 0.3135 0.1619 0.7455 -0.552 -0.0876 -0.1111 1
Sign of total 
return VIX 
per day
-0.1865 -0.1105 -0.172 -0.0923 -0.5286 0.6995 0.1145 0.0882 -0.5659 1
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
103
Table 8 shows that the VIX experiences a much more frequent appearance of zero returns during 
the trading day than the SPX does. Its number of zero returns within a trading day varies 
between a minimum of 26 minutes and a maximum of 277 minutes, 6.67% and 71.03% of total 
daily trading minutes and with a median of 174 minutes (i.e., 44.87%). We then investigate how 
this vast number of zero returns for the VIX relates to the SPX movement. Using correlation 
(see table 9) we again are interested more in the directions rather than the magnitude of the 
measure23. The analysis reveals that when correlating either the daily number of zeros returns 
for the VIX or the percentage of minutes (with zero returns out of daily 391 minutes) with the 
absolute SPX total returns per day, the direction is negative, implying that the lower is the 
change in SPX the more zero minute returns we’ll observe in the VIX – therefore, one should 
expect more activity (adjustments) in the VIX when the SPX has significant movement and viceversa when the SPX barely changes then there are less adjustment in the VIX and thus we’ll 
observe more zero minute returns. When correlating either the number of zero minute returns or 
the percentage of the daily zero minute returns (out of 391 daily minutes) with the sign of the 
total SPX return per day, we observe positive correlation, which indicates that if the sign is 
positive (i.e., the SPX moves upwards) one should expect more zeros in the VIX (i.e., less 
activity), and the opposite when the SPX moves downwards – when the SPX is trending down 
the VIX will adjust more frequently. These two observations are consistent with the documented 
asymmetry in the equity markets, sometimes ascribed to as “leverage effect” or the “risk 
premium” effect – in the equity market it is unlikely that positive and negative shocks have the 
same impact on the volatility. In the story of news, negative news reduces the demand for the 
stocks because of risk aversion. The consequence decline in stock value is followed by the 
increased volatility as forecasted by the news. 
Research Method and Hypothesis
Research Method
We are trying to build an empirical model that best explains and predicts the changes in the S&P 
500 (in other words – a model which explains (and predicts) the returns of the S&P500). 
We can think about the S&P 500 returns as following a Stochastic Differential Equation 
(SDE) of the general form:
 
 
 
 
23 The existence of zero returns in an interaday sample is a consequence of many different variants (such as volume, 
time of the day, news, etc.) which will not be captured by a single measurement such as correlation and hence we 
are only concerned on the direction and not on the magnitude.
WHAT DOES THE VIX ACTUALLY MEASURE? AN ANALYSIS OF THE CAUSATION OF SPX AND VIX
104
Instead of assuming a specific SDE (such as the Geometric Brownian Motion (GBM)), we 
can say that we do not know the exact theoretical model of the SDE that explains returns. 
Therefore, we are trying to build an empirical model that may serve as a good proxy for the SDE. 
If we do not have any specific theory in mind then the best econometric tool for that purpose 
would be estimation via Vector Autoregression (VAR) model (which is a purely atheoretical 
estimation method).
The form of the VAR model is:
 
Where is vector of constants (i.e., intercepts), is matrix (for every 
 ) and is a vector of error terms. We estimate a Bi-Variate VAR model of two 
time series: (i) returns of the S&P 500; and (ii) changes in the VIX.
This estimated Bi-Variate VAR model will result with two estimation equations; (i) 
estimated returns of the S&P 500, and (ii) estimated changes of the VIX. Each estimation model 
will be a function of lag-variables of S&P 500 returns and lag-variables of the changes of the 
VIX. More formally,
 (  )
 
 
And 
 (  )
 
 
Where and are constants; and and are a function of the lags values of the S&P 
500 returns; and and are a function of the lags values of the changes in the VIX; and is 
the optimal number of lags to be determined via information criteria.
The way we can interpret equation (2a) is as follows: remember that we are trying to find a 
good empirical (estimation) model as a proxy for the SDE. Therefore, we can view the function 
 as a proxy for the drift and the function as a proxy for the diffusion, which in this case both 
are in-line with the concept of drift and diffusion, respectively. That is as a proxy for the 
diffusion is in fact a function of the VIX (and the VIX is a measure of the expected volatility of 
the S&P 500 index in the next 30-day period), and hence could be a good representation for the 
randomness term of the SDE. The function , on the other hand, is a function of past returns , 
hence can be perceived as a good representation of the drift term of the SDE. 
ACRN Journal of Finance and Risk Perspectives
Vol. 3, Issue 2, June 2014, p. 83 – 132
ISSN 2305-7394
105
Hypotheses
After describing the empirical models we now present a few main hypotheses.
Since we are using a VAR model we will check two main competing hypotheses (and one 
secondary) with respect to causality.
Hypothesis 1: 
As explained above the VAR index translates, roughly, to the expected movement in the S&P 
500 Index over the next 30-day. This implies that the VIX is a forward–looking measure of the 
S&P500 future volatility. Therefore, we would expect a leading relationship – meaning the VIX 
movement leads the S&P 500 – hence, we would say that VIX “granger causes” the S&P 500 
Index.
Hypothesis 2:
The VIX Index is an “implied volatility” measure extracted from the options’ prices. The option 
price is a function of the underlying, which in this case is the S&P 500 Index. This suggests that 
the VIX measure is a function of the S&P 500, and hence implicitly determined by the values of 
the S&P 500 Index. Therefore, this type of relationship implies that the S&P 500 “granger 
cause” the VIX.
Hypothesis 3 (secondary):
Both VIX and SPX minute return Granger Cause each other’s time series, which implies that 
both arguments on the movement of the VIX could be correct. Although, even if we’ll observe a 
bi-directional causality or a bi-directional feedback, we may still find that one causality is greater 
and more significant than the other. A bi-directional causality does not necessarily indicate that 
the impact is the same, it only indicates that both series affect ea