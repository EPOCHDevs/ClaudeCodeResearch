---
url: https://www.scienpress.com/download.asp?ID=2402927
title: [PDF] An Empirical Examination of VIX Market Fluctuations
domain: misc
crawled_at: 2026-02-04T08:07:26.196920+00:00
source: exa_search
chart_count: 0
image_links:
outbound_links:
---

Advances in Management & Applied Economics, Vol. 12, No. 4, 2022, 109-118
ISSN: 1792-7544 (print version), 1792-7552(online)
https://doi.org/10.47260/amae/1246
Scientific Press International Limited
An Empirical Examination of VIX Market 
Fluctuations
Yu-Min Lian1, Yu-Jhih Jhong2, Po-Hsuan Wang3and Wei-Ming Chen4
Abstract
This study investigates the impacts of the Standard & Poor’s (S&P) 500 Index, the 
NASDAQ Volatility Index (VXN), the spot prices of gold and silver, and the U.S. 
Dollar Index (DXY) on the CBOE Volatility Index (VIX). Specifically, the 
proposed arbitrage pricing theory (APT) model, programmed by Python, performs 
multi-factor regression analysis that analyzes the degree of impact measured by the 
beta coefficient of systematic risks on each factor. Our samples include daily 
transaction data from 2007 to 2018, divided into three periods to assess the VIX’s 
impact for each sub-period. The three periods are entitled as the “Global Financial 
Crisis Period” (2007–2009), the “European Debt Crisis Period” (2010–2012), and 
the “Follow-up Period” (2013–2018). Empirical results show that the major factors 
are the S&P 500 index and the VXN, with the DXY being a minor factor. Moreover, 
both gold and silver spot prices have a significant impact on the VIX.
Keywords: VIX, Global financial crisis, European debt crisis, Systematic risk,
Arbitrage pricing theory, Multi-factor regression model.
1 Assistant Professor, Department of Business Administration, Fu Jen Catholic University, New 
Taipei City, Taiwan.
2 Department of Business Administration, Fu Jen Catholic University, New Taipei City, Taiwan.
3 Department of Business Administration, Fu Jen Catholic University, New Taipei City, Taiwan.
4 Department of Business Administration, Fu Jen Catholic University, New Taipei City, Taiwan.
Article Info: Received: May 3, 2022. Revised: May 21, 2022. 
Published online: May 24, 2022.
110 Lian, Jhong, Wang and Chen
1. Introduction 
The Volatility Index (VIX), introduced by the Chicago Board Options Exchange 
(CBOE), measures the implied volatility of S&P 500 index options, indicates 
market volatility for the next 30 days, and reflects investors’ sentiments (Whaley, 
2000). The VIX, often referred to as the fear index, is the stock market’s measure 
of expected volatility. When the VIX is low, investors believe that future stock 
market volatility will be moderate and prices will be stable. Conversely, when the 
VIX is high, stock prices may fluctuate significantly in the future, the uncertainty 
of the stock market will increase, and investors will become concerned (Fernandes 
et al., 2013). Therefore, the VIX indicates investors’ psychological sentiment.
The 2008 Global Financial Crisis was caused by the default of a large number of 
subprime mortgages, after a crisis in the U.S. housing market. Immediately after the 
Lehman Brothers bankruptcy, the crisis spread from real estate to the credit and 
stock markets. Subsequently, the S&P 500 index fell from 1,463 to 893, and the 
VIX reached a historical high of 89.53. Meanwhile, as a hedged financial 
commodity, gold prices tripled and silver prices fell by 50%. 
The European sovereign debt crisis occurred shortly after the Global Financial 
Crisis. Several Eurozone members, including Greece, Portugal, Ireland, Spain, and 
Italy, failed to make government debt payments and entered into technical default. 
Although these defaults occurred in only a few Eurozone countries, it has since 
become a problem for the entire region, leading to a possible split of the Eurozone. 
During the European sovereign debt crisis, the VIX rose to 45.45, the highest point 
of the past year and the U.S. Dollar Index (DXY) rose to above 80.
In this study, to illustrate the multiple factors affecting the VIX, we selected five 
variables from the stock, currency, and commodity markets that significantly 
correlate with the VIX. Our study specifically applies their relevance to the VIX for 
the aforementioned three periods. Empirical results show the evidences of ensuring 
the main impact factors for investments in the VIX market.
The remainder of this study is organized as follows: Section 2 summarizes previous 
studies and describes the variables; Section 3 provides the empirical model; and 
conclusions are presented in the final section.
An Empirical Examination of VIX Market Fluctuations 111
2. Data
In this study, we adopted the following five assets as explanatory variables for 
analysis. 
The source and description of the data used in the regression are as follows:
Table 1: Data
Variables Logarithmic 
Return Description Period Source
VIX lnRVIX
CBOE S&P 500 Volatility 
Index
2007.01.01
to
2018.12.31
Yahoo! 
Finance.com
S&P500 lnRS&P500 CBOE S&P 500 Index Yahoo! 
Finance.com
VXN lnRVXN Nasdaq 100 Volatility Index Yahoo! 
Finance.com
DXY lnRDXY U.S. Dollar Index Investing.com
XAU lnRXAU Spot Price of Gold Investing.com
XAG lnRXAG Spot Price of Silver Investing.com
Note: For Table 1, lnR indicates the logarithmic return of Variable.
Standard & Poor’s (S&P) 500 Index: The S&P 500 Index is a U.S. stock market 
index based on the market capitalizations of 500 large companies listed on the 
NYSE or the NASDAQ. It differs from other U.S. stock market indexes, such as the 
Dow Jones Industrial Average or the Nasdaq Composite Index, and is considered 
among the most representative indexes of the U.S. stock market. Auinger (2015) 
found a strong negative correlation between the VIX and the daily yield of the S&P 
500 Index.
The U.S. Dollar Index (DXY): Another common indicator of investor 
apprehension, the DXY measures the value of the dollar relative to other foreign 
currencies (Nikos, 2006). It is a reference marker for the strength of the dollar. 
Harwood (2011) and Liao et al. (2018) showed a significant and positive correlation 
between the VIX and the DXY.
The NASDAQ 100 Volatility Index (VXN): The VXN, which measures the 
implied volatility of the NASDAQ 100 index, is comprised largely of high-tech 
industrial companies and does not include financial stocks. It is often used to reflect 
trends in the NASDAQ market or in the U.S. high-tech industry (Simon, 2003). 
Arak and Mijid (2006) and Schwert (2001) found that the VIX should significantly 
and positively correlate with the VXN.
Gold and Silver Spot Prices: The choice of two precious metal factors is based on 
the earlier studies. Gold and silver are inversely related to each other. Gold, a 
hedged commodity (Kolluri, 1981), positively correlates with the VIX, and silver, 
an investment commodity, negatively correlates with it; these influences were 
confirmed Jubinski and Lipton (2013) and Chen (2011) confirmed these 
correlations. Both gold and silver prices are highly sensitive to market fluctuations.
112 Lian, Jhong, Wang and Chen
3. Methodology
The research was organized as follows. We calculated the logarithmic return of 
factors and then checked variance inflation factors to ensure that no 
multicollinearity existed. After detecting multicollinearity, we establish an APT 
model for regression analysis.
3.1 Unit Root Test
According to Granger and Newbold’s research in 1974, it is necessary to confirm 
whether time series data is a stationary series before performing an analysis. 
Therefore, this study employs both an Augmented Dickey–Fuller test and the 
Phillips–Perron test to the variables’ stability. The test formula is as follows:
The Augmented Dickey–Fuller Test:
∆𝑌𝑡 = 𝛼 + 𝛾𝑌𝑡−1 + ∑𝑖=2
𝑛 𝛽𝑖∆𝑌𝑡−𝑖+1 + 𝜀𝑡
(1)
where ∆𝑌𝑡represents the time series 𝑌 after a difference, 𝛼 is the intercept term, 
T is the time trend, 𝜀𝑡is a white noise, and 𝑖 is the maximum lag order. The null 
hypothesis of the test is 𝛾 = 0, that is, the time series Y contains a unit root. We 
have used Akaike information criterion to choose the lag order.
The Phillips–Perron Test:
∆𝑌𝑡 = 𝛼 + 𝜌𝑌𝑡−1 + 𝜀𝑡
(2)
The null hypothesis of the test is 𝜌 = 0, that is, the time series Y contains a unit 
root. The alternative hypothesis is 𝜌 ≠ 0, meaning that the time series Y is 
stationary. The lag order was selected by Newey–West.
Table 2: Unit Root Test
Level
𝐥𝐧𝐑𝐕𝐈𝐗 𝐥𝐧𝐑𝐒&𝐏𝟓𝟎𝟎 𝐥𝐧𝐑𝐃𝐗𝐘 𝐥𝐧𝐑𝐕𝐗𝐍 𝐥𝐧𝐑𝐗𝐀𝐔 𝐥𝐧𝐑𝐗𝐀𝐆
ADF Statistic −19.985
(9)*
−26.865
(4)*
−55.523
(1)*
−21.801
(8)*
−55.890
(1)*
−56.168
(1)*
PP Statistic −59.978
(1)*
−60.582
(1)*
−55.523
(1)*
−57.821
(1)*
−55.890
(1)*
−56.168
(1)*
Note: For Table 2, * indicates a 5% significance, respectively. (.) indicates the lag order selected by 
Akaike information criteria.
Table 2 shows the results of the unit root test. It can be seen from the table that all 
the variables have reached a stationary level.
An Empirical Examination of VIX Market Fluctuations 113
3.2 Variance Inflation Factors
Before performing regression analysis, it is necessary to confirm whether 
multicollinearity exists. In statistics, the variance inflation factor (VIF) quantifies
the severity of multicollinearity in an ordinary least squares regression analysis.
𝑉𝐼𝐹𝑖 = 1/(1 − 𝑅𝑖
2
) (3)
where 𝑅𝑖
2
is the 𝑅
2
-value obtained by regressing the 𝑖
𝑡ℎ predictor on the 
remaining predictors. A VIF of 1 means there is no correlation between this 
independent variable and any other variables. VIFs between 1 and 10 indicate 
moderate correlations not severe enough to warrant corrective measures. VIFs 
greater than 10 represent critical levels of multicollinearity, where coefficients are 
poorly estimated and p-values are questionable. Table 3 shows the value of the VIFs.
Table 3: Variance Inflation Factors
Variables VIF Factor
Intercept 1.5594
lnRDXY 2.9452
lnRS&P500 3.3168
lnRVXN 1.8626
lnRXAG 4.4428
lnRXAU 5.7642
3.3 Arbitrage Pricing Model
To measure the impact of multiple factors on the VIX, we refer to the arbitrage 
pricing theory (APT) model of Ross (1976). An APT is more flexible than the 
capital asset pricing model (CAPM), because the model allows multiple risk factors 
to explain the assets. In this research, we established an APT model that considers
the link between expected returns and i-th factor sensitivities. The original APT 
model specified by Ross is as follows:
𝑅𝑗 − 𝑅𝑓 = α + ∑𝑖
𝑛βi(𝑅𝑖 − 𝑅𝑓) + ε𝑖 (4)
where Rjrepresents the return of asset j and Rfis the risk-free rate (the yield on 
a one-year U.S. T-bill). α is the intercept term, and ε𝑖is a risky asset's 
idiosyncratic random shock, with a mean of zero. 𝑅𝑖 − 𝑅𝑓 is the excess return of 
factor 𝑖, which is computing as the difference between the return and the risk-free 
rate. βx,indicating the sensitivity of RVIX to factor i.
114 Lian, Jhong, Wang and Chen
4. Estimation and Results 
In this study, we established an APT model that considers the link between expected 
returns and the i-th factor sensitivities, as follows:
𝑙𝑛𝑅𝑉𝐼𝑋 − 𝑙𝑛𝑅𝑓 = α + β1(𝑙𝑛𝑅𝑆&𝑃500 − 𝑅𝑓)+ β2(𝑙𝑛𝑅𝐷𝑋𝑌 − 𝑅𝑓)
+ β3(𝑙𝑛𝑅𝑉𝑋𝑁 − 𝑅𝑓)+ β4(𝑙𝑛𝑅𝑋𝐴𝑈 − 𝑅𝑓)+ β5(𝑙𝑛𝑅𝑋𝐴𝐺 − 𝑅𝑓) + ε𝑖
(5)
where 𝑙𝑛𝑅𝑉𝐼𝑋 is the logarithmic return of VIX, 𝑙𝑛𝑅𝑆&𝑃500 is the logarithmic
return of the S&P 500 index, 𝑙𝑛𝑅𝐷𝑋𝑌 is the logarithmic return of the DXY, 
𝑙𝑛𝑅𝑋𝐴𝑈 is the logarithmic return of the gold spot price, 𝑙𝑛𝑅𝑋𝐴𝐺 is the logarithmic
return of the silver spot price, and ε𝑖is the error term. α, β1, and β2…β5 are
parameters to be estimated.
4.1 Full Period (2007-2018)
Table 4: Regression Results for the Full Period
Dependent Variable: VIX Method: Least Squares
Variable β Std. Error t-statistic Prob.
Constant −0.0008 0.001 −1.174 0.241
lnRS&P500 −0.8109 0.055 −14.783 0.000
lnRDXY 0.5434 0.067 8.163 0.000
lnRVXN 0.9535 0.011 84.878 0.000
lnRXAU 0.3850 0.077 5.022 0.000
lnRXAG −0.1579 0.049 −3.228 0.001
R-squared: 0.851 F-statistic: 3418 Akaike Info. 
Criterion: −12,470
Adj.
R-squared: 0.851 Prob.(F-statistic): 0.00 Schwartz Criterion: −12,430
Table 4 shows that all explanatory variables have a significant impact on the returns 
of the VIX, where 𝑙𝑛𝑅𝑆&𝑃500 has negative effects which is significant. This is 
consistent with the research findings of Auinger (2015). The positive relationship 
of 𝑙𝑛𝑅𝐷𝑋𝑌 and 𝑙𝑛𝑅𝑉𝑋𝑁 with VIX returns also agrees with Harwood (2011), Liao
et al. (2018), Mijid (2006), and Schwert (2001). The significantly positive effect of 
𝑙𝑛𝑅𝑋𝐴𝑈 is also consistent with previous assumptions, while 𝑙𝑛𝑅𝑋𝐴𝐺, as opposed to 
gold, has a significantly negative effect on the VIX, meaning that silver is not 
suitable for hedging within the full period.
An Empirical Examination of VIX Market Fluctuations 115
4.2 Global Financial Crisis Period (2007–2009)
Table 5: Regression Results of the Global Financial Crisis Period
Dependent Variable: VIX Method: Least Squares
Variable β Std. Error t-statistic Prob.
Constant −0.0020 0.002 −1.229 0.219
lnRS&P500 −0.5395 0.071 −7.568 0.000
lnRDXY 0.3811 0.094 4.074 0.000
lnRVXN 1.0057 0.023 43.818 0.000
lnRXAU 0.1115 0.111 1.044 0.316
lnRXAG −0.0579 0.074 −0.784 0.434
R-squared: 0.867 F-statistic: 970.6 Akaike Info. 
Criterion: −3,222
Adj.
R-squared: 0.866 Prob.(F-statistic): 0.00 Schwartz Criterion: −3,195
Table 5 shows that the explanatory variables during the 2008 financial crisis were 
significant, except for gold and silver. This means that 𝑙𝑛𝑅𝑋𝐴𝑈 and 𝑙𝑛𝑅𝑋𝐴𝐺 had
no significant impact on the VIX during this period. We suggest that, at the time of 
the 2008 financial crisis, gold and silver were not perceived as the important safe 
haven assets by investors. When global stock markets were hit by the financial crisis, 
the VIX reflected U.S. stock market investors’ concerns by rising above 80. Gold, 
meanwhile, actually appreciated.
4.3 The European Debt Crisis Period (2010–2012)
Table 6: Regression Results of the European Debt Crisis Period
Dependent Variable: VIX Method: Least Squares
Variable β Std. Error t-statistic Prob.
Constant −0.0023 0.001 −2.046 0.041
lnRS&P500 −1.2921 0.140 −9.249 0.000
lnRDXY 0.1381 0.206 0.670 0.503
lnRVXN 0.8312 0.023 35.905 0.000
lnRXAU 0.3960 0.132 2.996 0.003
lnRXAG −0.1909 0.068 −2.793 0.005
R-squared: 0.890 F-statistic: 1199 Akaike Info. 
Criterion: −3,426
Adj.
R-squared: 0.889 Prob.(F-statistic): 0.00 Schwartz Criterion: −3,399
116 Lian, Jhong, Wang and Chen
Table 6 shows that all explanatory variables have a significant effect on the VIX’s 
returns, except for 𝑙𝑛𝑅𝐷𝑋𝑌 during the European debt crisis. 𝑙𝑛𝑅𝑋𝐴𝑈 has a 
significant positive impact and 𝑙𝑛𝑅𝑋𝐴𝐺 has a significant negative impact. Gold 
became an ideal safe haven asset for investors after a financial crisis. The change in 
significance is consistent with our previous position. Meanwhile, silver opposed the 
aforementioned property of gold.
4.4 The Follow-Up Period (2013–2018)
Table 7: Regression Results of the Follow-Up Period
Dependent Variable: VIX Method: Least Squares
Variable β Std. Error t-statistic Prob.
Constant −0.0011 0.001 −0.959 0.338
lnRS&P500 −1.7535 0.140 −12.548 0.000
lnRDXY 1.2070 0.146 8.277 0.000
lnRVXN 0.8963 0.018 49.626 0.000
lnRXAU 0.7365 0.151 4.885 0.000
lnRXAG −0.2823 0.102 −2.780 0.006
R-squared: 0.835 F-statistic: 1518 Akaike Info. 
Criterion: −5,997
Adj. 
R-squared: 0.835 Prob. (F-statistic): 0.00
Schwartz 
Criterion: −5,965
Table 7 shows the explanatory variables’ regression results after the financial crisis. 
All the explanatory variables have a significant impact on the returns of VIX. 
𝑙𝑛𝑅𝑆&𝑃500 and 𝑙𝑛𝑅𝑋𝐴𝐺 have significant negative effects and 𝑙𝑛𝑅𝐷𝑋𝑌 , 𝑙𝑛𝑅𝑉𝑋𝑁,
and 𝑙𝑛𝑅𝑋𝐴𝑈 have significant positive effects. Recent regression results have a 
higher coefficient value, indicating a greater impact of each explanatory variable on 
the VIX after a global financial crisis. Among all explanatory variables, 𝑙𝑛𝑅𝑆&𝑃500
and 𝑙𝑛𝑅𝑉𝑋𝑁 have the strongest effects on the VIX’s returns, while 𝑙𝑛𝑅𝑋𝐴𝐺 has the 
weakest effects.
An Empirical Examination of VIX Market Fluctuations 117
5. Conclusion
Using an APT model, this study aims to discover what factors impact the returns of 
the VIX. The selected period from 2007 to 2018 includes two major financial events:
the 2008 financial crisis and the 2010 European debt crisis. We divide these two 
periods and one following period into three separate study models to observe which 
explanatory variables influence the returns of the VIX.
We believe that our data sources (Yahoo! Finance.com and Investing.com) are 
reliable. Of the APT model’s five explanatory variables, the stock returns 
𝑙𝑛𝑅𝑆&𝑃500 and 𝑙𝑛𝑅𝑉𝑋𝑁 represent the capital market’s impact on the returns of VIX,
𝑙𝑛𝑅𝐷𝑋𝑌 represents the impact from the money market, and 𝑙𝑛𝑅𝑋𝐴𝑈 and 𝑙𝑛𝑅𝑋𝐴𝐺
represent the impact from the precious metals market.
The following conclusions were drawn from the empirical results. 
1. The explanatory variables we selected have a significant effect on the returns of 
VIX. 
2. From the three periods’ regression results, we find that explanatory variables’ 
effect on the VIX’s returns increases gradually over time. 
3. The VIX’s returns primarily are affected by the explanatory variables
𝑙𝑛𝑅𝑆&𝑃500 and 𝑙𝑛𝑅𝑉𝑋𝑁 . 𝑙𝑛𝑅𝑆&𝑃500 has significant negative effects and
𝑙𝑛𝑅𝑉𝑋𝑁 has significant positive effects. This is consistent with our previous 
assumption. 
4. In the 2013–2018 regression results, 𝑙𝑛𝑅𝐷𝑋𝑌 has a significant positive effect
on the returns of the VIX. It also shows that the DXY has gradually increased 
its impact on the returns of the VIX, which indicates the strong performance of 
the U.S. dollar in recent years.
ACKNOWLEDGEMENTS
Yu-Min Lian is grateful to the Ministry of Science and Technology (MOST) for 
support through Project No.: MOST109-2410-H-030-019-MY2.
118 Lian, Jhong, Wang and Chen
References
[1] Arak, M. and Mijid, N. (2006). The VIX and VXN volatility measures: Fear 
gauges or forecasts? Derivatives Use, Trading & Regulation, 12, pp. 12-27.
[2] Auinger, F. (2015). The causal relationship between the S&P 500 and the VIX 
index: Critical analysis of financial market volatility and its predictability. 
Springer Gabler, pp. 50-55.
[3] Chen, S.H. (2011). A study on the gold price relationship with stock index, oil 
prices and volatility index. Feng Chia University, FCU e-Theses & 
Dissertations.
[4] Fernandes, M., Medeiros, M.C. and Scharth, M. (2013). Modeling and 
predicting the CBOE market volatility index. Working Paper, p. 342.
[5] Harwood, V. (2011). Correlation between the VIX index and the U.S. dollar 
index. https://sixfigureinvesting.com/2011/04/correlation-between-the-vixindex-and-the-u-s-dollar-index/
[6] Liao, J., Shi, Y. and Xu, X. (2018). Why is the correlation between crude oil 
prices and the US dollar exchange rate time-varying?-Explanations based on 
the role of key mediators. International Journal of Financial Studies, 6, p. 61
[7] Jubinski, D. and Lipton, A.F. (2013). VIX, gold, silver, and oil: How do 
commodities react to financial market volatility? Journal of Accounting and 
Finance, 13, pp. 70-88.
[8] Kolluri, B.R. (1981). Gold as a hedge against inflation: An empirical 
investigation. Quarterly Review of Economics and Business, 21, pp. 13-24.
[9] Nikos, K. (2006). Commodity prices and the influence of the U.S. dollar. 
World Gold Council, pp. 1-12.
[10] Ross, A.R. (1976). The arbitrage theory of capital asset pricing. Journal of 
Economic Theory, 13, pp. 341-360.
[11] Schwert, G.W. (2001). Stock volatility in the new millennium: How wacky is 
Nasdaq? University of Rochester, Rochester, NY 14627 and National Bureau 
of Economic Research.
[12] Simon, D.P. (2003). The Nasdaq volatility index during and after the bubble. 
Journal of Derivatives, 11, pp. 9-24.
[13] Whaley, R.E. (2000). The investor fear gauge. Journal of Portfolio 
Management, 26, pp. 12-17.