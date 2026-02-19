---
url: https://dukespace.lib.duke.edu/server/api/core/bitstreams/fee71aba-f189-48fb-9107-c108e3fbaf10/content
title: [PDF] Contagion in Emerging Market Equities - DukeSpace
domain: misc
crawled_at: 2026-02-04T08:08:30.232971+00:00
source: exa_search
chart_count: 0
image_links:
outbound_links:
---

Contagion in Emerging Market Equities
Yiwen Zhu and Richard Li
Professor Emma Rasiel and Professor Aino Levonmaa, Faculty Advisors
April 15, 2011
Duke University
Durham, North Carolina
Honors Thesis Submitted in partial fulfillment of the requirements for Graduation with 
Distinction in Economics in Trinity College of Duke University
2
Acknowledgements
We would like to thank our advisors, Professor Emma Rasiel and Professor Aino 
Levonmaa, for their mentorship and encouragement. Their insights and knowledge 
developed our paper to its full potential. We also would like to thank Professor Daniel 
Egger and his team (Guillaume Guy, Dan Wu, Alexander Lee, John Engstrom, Jeff Chen, 
and Ben Leung) for providing the data used in this paper. Professor Egger and his team 
cleaned and processed raw data, and they also provided great assistance in special 
requests.
3
Abstract
Adapting the definition from Forbes (2002), financial contagion is the significant 
increase in asset return correlation or transmission of volatility after a shock has occurred 
to a country or region. In this paper, we analyze country and regional equity data during 
the Thai Crisis of 1997 and the Credit Crisis of 2007. We derive regression models for 
equity returns and cross-sectional variance (dispersion) to determine relationships in 
these variables between key countries during the crisis periods. We find evidence of 
contagion between countries during the Thai Crisis and to lesser extent during the Credit 
Crisis.
JEL Classification: C12; C32; C51; C58; G01; G14; G15;
Keywords: Equities, Emerging Markets, Contagion, Dispersion, Financial Crisis, Thai 
Crisis, Credit Crisis 
4
1 Introduction
Crises in financial markets can cause asset prices to plunge and may generate
broader financial instability within a country. The sequential spread of a shock from one 
country or sector to another is generally described as contagion. Academic researchers 
are interested in identifying the channels of contagion, and a wide spectrum of definition 
regarding contagion exists. This paper adopts a previous definition from Forbes (2002):
that “contagion is a significant increase in cross-market linkages after a shock to one 
country (or group of countries)”. These cross-market linkages can be measured in 
“correlation of asset returns, probability of a speculative attack, or the transmission of 
shocks or volatility” (Forbes 2001). In this paper, we empirically investigate the existence 
of contagion within the Emerging Markets (“EM”) during both the Thai Crisis and the 
Credit Crisis. We utilize Forbes’s definition of contagion (2002) and, through regression 
analysis, determine its presence during major financial crises between 1996 and 2009.
Two crises1of interest are the Thai Crisis (1997-1998) and the Credit Crisis 
(2007-2009). The Thai Crisis, originating in Thailand after the devaluation of the Baht in 
July 1997, witnessed a sharp decline in returns across Southeast Asian nations, 
particularly Indonesia, Malaysia, the Philippines, and South Korea. Several authors 
including Chiang et al. (2007), Park and Song (2000), and Baig (1999) have concluded 
that these decreases in stock returns across several countries are evidence of contagion. 
The Credit Crisis (2007-2009) is a more recent crisis that can also be analyzed for 
contagion. Turmoil began in the United States as real estate prices crashed and large 
 
1 We also investigated the possible existence of contagion during the Brazil Election in 2002. The 
economic instability Brazil Crisis occurred from political discontent and debt problems. The results did 
not show relationships of significance and the results are provided in Appendices B and C.
5
banks had to write down billions of dollars of assets held in their portfolios
(Brunnermeier 2009). This led to liquidity dry-ups and bankruptcies of major banks
including Lehman Brothers, eventually spiraling to the largest financial crisis since the 
Great Depression (Brunnermeier 2009). Even though the Credit Crisis originated in the 
U.S., there is evidence of its effects spilling over into the emerging markets (Goldstein, 
2009). 
There exist various empirical methods to test for the presence of contagion. Sachs 
et al. (1996) argue that contagion can be detected by observing an increase in the crosscountry correlation of returns. Forbes et al. (2002) develop a model that accounts for 
heteroskedasticity in returns data and conclude that there was no significant increase in 
correlation and, therefore, no contagion during the Thai Crisis. Chiang et al. (2007) argue
the opposite using a dynamic conditional-correlation model, confirming a contagion 
effect. Other methods of contagion analysis include modeling international trade flow 
between countries during crises (Glick, 1999) and examining liquidity of bank holdings
(Allen, 2000).
In this paper, in addition to exploring the relationship between equity returns in 
EM during the two crisis periods, we also investigate the relationship between the 
countries’ cross sectional variances of returns. Cross sectional variance, which is often
labeled dispersion, has been extensively analyzed in recent years and is of considerable 
importance to portfolio managers. Solnik and Roulet (2000) introduced dispersion as a
cross-sectional measure of market correlation. Intuitively, low dispersion implies that 
individual stock returns within a country or index are very similar; while high dispersion 
suggests that the range of returns among equities is much wider. More recently, Yu and 
6
Sharaiha (2007) decomposed dispersion into a combination of both time series volatility 
and correlation. They also show how dispersion measures can be used as a metric for
excess returns. Egger and Jacob (2010) analyze dispersion with regards to portfolio 
concentration and construction. To our knowledge, there has been no previous work that 
utilizes dispersion to explore contagion effects. 
To begin empirical analysis, we start out with the Capital Asset Pricing Model 
(CAPM) (Sharp 1964, Lintner 1965b) specification for individual stock returns. A model 
is derived in which one country’s returns are assumed to be dependent on another 
country’s returns one period earlier. In order to investigate the implication of crisis 
periods for cross-sectional variance, we decompose the sources of variation in returns to a 
market component and a country specific component, following the methodology set out 
by Campbell et al (2001). A model similar to the returns model is then derived. Thus, we 
attempt to determine whether trends in certain countries’ returns (and dispersion) follow
those of another country, after accounting for contemporaneous and lagged market-wide 
movements.
The presence of statistically significant relationships in lagged returns goes 
against the theory of the efficient markets hypothesis (Fama, 1970). This theory argues 
that equity markets are priced to fully reflect all available information, removing 
potential economic profits from trading. This implies that returns should not be 
predictable when trying to uncover return relationships across time. We believe that this 
theoretical assumption may be violated in the real world, especially over relatively short 
time periods and during market crises. Empirical work from Lim et al. (2008) found that 
the Thai Crisis adversely affected stock market efficiency of Asian countries.
7
In this paper, the detection of contagion is through applying indicator variables to 
the derived regression models. These regressions would indicate any statistically 
significant relationship in lagged returns that solely exist for dates specified as a crisis. 
Increases in these relationships between any two countries could signify contagion during 
that crisis. Our findings show significant relationships in returns and dispersion in EM 
during the Thai Crisis and, to a lesser extent, the Credit Crisis.
The remainder of the paper is structured as follows: in section two, we introduce 
the dataset used in the regression estimation. Section three provides the methodology, 
including model derivations for returns and dispersion as well as the use of indicator 
variables to delineate periods specific to each economic crisis. Section four presents our 
results for returns and dispersion during the Thai Crisis and Credit Crisis. Finally, section 
five concludes by summarizing our findings and suggesting areas of further research.
2 Data 
2.1 Data Description
Weekly equity returns and dispersion in the Emerging Markets from July 1996 to 
July 2009 are obtained from the Russell Emerging Markets Indices by Russell 
Investments (Egger, 2010) 2. The regions included in the indices are Asia, Europe, Africa,
the Middle East, and Latin America. A full list of countries is included in Appendix A.
The Russell data contains dividend-adjusted market capitalization in US Dollars for each 
stock and the total number of shares available for trading. For every country in the index, 
the data is used to determine asset prices, and thus, weekly returns and dispersion.
 
2
Clean country level weekly data is provided by Professor Daniel Egger from the Center of Quantitative 
Modeling at Duke University.
8
Individual stock data is categorized by country code. Weekly returns for all the 
stocks with the same country code were grouped together to form weekly returns at the 
country level. Countries that had missing data or fewer than 15 stocks at any given period 
of time were formed into three regional clusters3: EMEA (Europe, Middle East, and
Africa), Asia, and South America. The cross-sectional variance for a given week, defined 
as dispersion, 
 
, is also calculated from the data and grouped at the country and cluster 
level using the definition of dispersion from Equation 3.2.1 in section 3.2.
We focus our contagion analysis on the key countries of Thailand, China, 
Indonesia, and Brazil. Thailand is considered the source of the Thai Crisis, and thus is an 
obvious choice. We choose China because it is the largest economy among EM countries 
according to GDP during the entire time period of the data set4. Indonesia represents a 
Southeast Asian country that has a close geographic proximity and economic relationship 
with Thailand. We also choose Brazil, the largest South American country (by GDP), to 
evaluate the relationship between geographically disperse EM countries. 
2.2 Dispersion Data
Figures 1 through 4 show the time series of dispersion, clustered by geographical 
regions5. We observe that dispersion levels spike at similar times in the same geographic 
regions. This is especially noticeable in Figure 1 of Southeast Asian countries. 
Comparing Figures 1 and 3, we see that South American countries’ dispersion did not 
 
3 Countries in the regional clusters are listed in Appendix A.
4 All Gross Domestic Product information is according to data from The World Bank website
5 The plotted dispersion values are normalized to start at 0. Each country’s first dispersion value is 
subtracted from its remaining dispersion values. This is so that all of the plots would have the same 
starting point.
9
exhibit as large of an increase as those of the Asian countries’ dispersion between 1995 
and 2000. 
Figure 1. Southeast Asia Dispersion Time Series (1996-2009)
Figure 1 above shows that dispersion in Asia, Indonesia, and the Philippines all 
increase around the time of the Thai Crisis. Figure 2 contains the dispersion time series 
for the remaining Asian countries of China, India, Korea, and Taiwan. We see that 
neither India nor Taiwan experience the same sharp increase in dispersion in 1997, but 
China and Korea do. Figure 3 shows while South American countries’ dispersion
increased during the Thai Crisis, they reach even higher levels later in the sample period. 
Finally, Figure 4 contains the remaining countries in the EMEA region. Even though 
European and African countries’ dispersion rose during the Thai Crisis, the levels did not 
reach the same magnitude as the Southeast Asian countries. Additionally, the dispersion 
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Asia Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Indonesia Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Malaysia Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Thailand Dispersion
10
levels in Turkey and EMEA increased to a similar or higher level in the few years before 
2010.
Figure 2. Asian Dispersion Time Series (1996-2009)
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
China Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
India Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Korea Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Taiwan Dispersion
11
Figure 3. South America Dispersion Time Series (1996-2009)
Figure 4. EMEA Country Dispersion Time Series (1996-2009)
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Brazil Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Chile Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Mexico Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
South America Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
Turkey Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
South Africa Dispersion
1995 2000 2005 2010
0
0.02
0.04
Date Cross Sectional Variance
EMEA Dispersion
12
3 Methodology
3.1 Derivation of Model for Returns 
For the returns regressions, we begin with the CAPM model for an individual 
equity return (Sharpe 1964, Lintner, 1965b). According to the CAPM, Equation 3.1.1 
below, the relationship between the expected return of an asset and the expected market 
return is linear with slope, , equal to the ratio of the covariance between the market and 
asset and the variance of the market:
    (3.1.1)
 
 
 (3.1.2)
To empricially implement the CAPM, we utilize Equation 3.1.2 (Campbell, 1996)
which is a single factor linear regression between an individual asset and the overall 
return on the market6. is the return of an asset and time , is the intercept, is 
the coefficient for asset , is the overall market return at time , and is the error 
term for asset at time . We also make the following assumptions: 
  
 
 
 
 
6 We assume that the weekly risk-free return is zero.
13
We aggregate individual stock return data to the country level. This step stems 
from a restriction in our data source. Our data consists of returns only for each country at 
time , therefore we cannot estimate the individual asset regressions. For country with 
 stocks, let represent the individual asset in country . We can find the equal 
weighted mean return by using: 
 
 
 
 
 
 
 
 
 
 
 
 
 
 (3.1.3)
We can now consider two countries and and define their equal weighted mean 
return: 
 
 
 (3.1.4)
 
 
 (3.1.5)
In order to analyze the effect of country 's return on those of country , we
would like to run a regression of the error term of country on that of country , which
controls for the effect of the market factor:
  (3.1.6)
However, as and are unobservable in the real world, we must rewrite 
Equation 3.1.6 in terms of the observable variables in Equations 3.1.4 and 3.1.5.
 
 
 (3.1.7)
14
 
 
 (3.1.8)
Substituting Equations 3.1.7 and 3.1.8 into Equation 3.1.6, we have: 
 
  
 
  
We now have a regression for the equal weighted mean return for country at 
time in terms of the market return and the equal weighted mean return of country . Let: 
 
 
  
 
Then the final equation will be: 
  (3.1.9)
Comparing Equation 3.1.9 with Equation 3.1.6 we note that the coefficient 
remains unchanged in the transformation. Thus, testing testing the null hypothesis for 
 versus the alternative of , that is, testing the impact of the residual of 
country on country , is equivalent to testing the impact of the return in country on that 
of country in the transformed Equation 3.1.9. 
We believe the effects of a crisis from country will not effect the returns of 
country without having a time lag. We then incorporate a time lag of one period and 
perform a similar substitution, except with: 
15
 
 
 (3.1.10)
 
 (3.1.11)
We then substitute Equations 3.1.10 and 3.1.11 into Equation 3.1.12 below: 
  (3.1.12)
 
  
 
  
Let: 
 
 
 
 
 
 
Then our equation for return of country on the market return and the return of 
country with lag 1 is: 
  (3.1.13)
Again, notice that the coefficient in Equation 3.1.13 is the same as from 
Equation 3.1.12. This means that, testing for significance of in the derived regressions, 
and testing the null hypothesis for versus the alternative of are equivalent.
16
3.2 Derivation of Model for Dispersion
The mathematical definition of cross sectional variance is: 
 
 
 
 
 
 
 
 
 (3.2.1)
 is the number of assets while is the cross sectional average return at time .
Taking Equations 3.2.1 and and the cross-sectional average7shown in Equation 
3.1.3 and substituting them into the definition of 
 
, we get: 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  
 
  
  
Using the definitions for variance and covariance, and the orthogonality 
assumptions, we can further simplify the formula for cross sectional variance of returns. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
We can simplify the notation by rewriting the cross-sectional variance as a 
function of squared market returns, 
 
, and cross sectional variance of the residual, 
 
: 
 
7 from our initial assumptions about the distribution of .
17
 
   
 (3.2.2)
Since Equation 3.2.2 provides the form of cross sectional variance for a single 
country, we can then consider 
 
for countries and ; let 
 
and 
 
be the cross 
sectional volatilities for countries and respectively. 
 
 
 
 
 
 (3.2.3)
 
 
 
 
 
 (3.2.4)
As with the derviations of our return model above, we wish to separate market 
effects from country-specific effects for dispersion as well. To analyze the impact of the 
cross sectional variance of country on that of country , we would like to run the 
equation below:
 
 
 
 
 
 (3.2.5)
However, because we cannot observe 
 
 
and 
 
 
, we must rewrite Equations 
3.2.3 and 3.2.4 such that we are able to derive a regression equation in terms of the 
observable values: 
 
 
 
 
 
 (3.2.6)
 
 
 
 
 
 (3.2.7)
Substituting Equations 3.2.6 and 3.2.7 into Equation 3.2.5, we derive a regression 
for cross sectional variance of country , 
 with respect to a market squared term, 
 
,
and the cross sectional variance of country , 
 
:
18
 
 
 
 
 
 
 
 
 
 
We now have the cross sectional variance for country in terms of the squared 
market return and the cross sectional variance of country . Let: 
 
 
 
We have the final equation of: 
 
 
 
 
 (3.2.8)
If we allow for a lag of 1 period, Equation 3.2.5 will be modified to become: 
 
 
 
 
 
 (3.2.9)
Once again, substituting the formulas for 
 
and 
 
into Equation 3.2.9 results 
in: 
 
 
 
 
 
 
 
 
 
  
We obtain a regression for the cross sectional variance of country in terms of the 
squared market return at time , the squared market return at time , the cross 
sectional variance of country at time . Let: 
19
 
 
 
 
We have the cross sectional variance of country in terms of the squared market 
return from time and as well as the cross sectional variance of country from the 
previous period: 
 
 
 
 
 
 (3.2.10)
In both Equations 3.2.8 and 3.2.10, the coefficient, , is the same value from 
Equations 3.2.5 and 3.2.9 respectively. The analysis of from Equations 3.2.8 and 
3.2.10 is equivalent to the analysis of in Equations 3.2.5 and 3.2.9.
3.3 Regression Models
The following equations are used for regressions on returns (Equation 3.3.1) and 
dispersion (Equation 3.3.2). Both equations are multivariate linear regression models 
used on the entire sample time period (1996 to 2009).
 
(3.3.1)
 
 
 
 
 
(3.3.2)
 is the weekly returns for country at time t and 
 
is the dispersion for country at 
time . and are the intercepts while and represent the coefficients for the 
market factors, and 
 
respectively. is the coefficient for the return of country 
20
at time , . is the coefficient for lagged dispersion of country , 
 
.
Finally, and are the respective regression error terms. 
The returns model in Equation 3.3.1 takes into account the market factors that 
affect country returns. We assume that contemporaneous and lagged market factors have 
significant relationships with both the explanatory country and the target country. Only 
by controlling for the market factor can the coefficient of the explanatory country have 
meaningful interpretation. The same analysis applies for Equation 3.3.2.We run the
regression models across the entire data sample to identify statistically significant 
relationships between the weekly returns or dispersion of one country on next week’s 
returns or dispersion of a different country. 
3.4 Indicator Regression Models
Equations 3.4.1 and 3.4.2 were used to determine the relationship between the 
emerging markets’ returns and the dispersion of Brazil, China, and Thailand during the 
Thai Crisis (1997-1999) and the Credit Crisis (2007). 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
(3.4.1)
 
 
 
 
 
 
 
 
  
 
 
 
 
 
 
 
 
 
 
  
(3.4.2)
The same coefficients from Equations 3.3.1 and 3.3.2 remain in models with an 
indicator variable and are given the same interpretations. The additional terms of 
 
and 
 
 
represent the coefficients for market factors, and 
 with an indicator 
variable. 
 
is the coefficient for lagged returns of country during time periods of crisis, 
 
 
represents the respective coefficient for dispersion. The indicator variable takes the 
value of 1 when country is in a crisis period and 0 during non-crisis, or normal, periods. 
21
The dates when the indicator variable equals 1 are given in Table 1 below. The Thai 
Crisis began on 7/2/1997 when the Thai baht devalued and ended on 12/30/19988. The 
Credit Crisis dates were selected by identifying the market peak of the S&P500 index 
with the end date being identified as the trough.
Table 1: Crises Start and End Dates
Crisis Start Date End Date
Thai 7/2/1997 12/30/1998
Credit 4/11/2007 3/9/2009
The indicator variable separates the relationships during the crisis period from the 
remaining time periods. The inclusion of indicator variables reflects the assumption that 
both market effects and country-specific effects between countries change during the 
time of a crisis. A statistically significant estimate of 
 
and 
 would provide support 
for this assumption.
3.5 Exponential Weighted Moving Average Correlations
An exponentially weighted moving average (EWMA) model, or exponential 
smoother, is used to calculate the covariance between the returns of two given countries
(Engle 2009)9. The EWMA model uses a weighted average of the most recent 
observation in estimating the conditional covariance:
 
 
(3.5.1)
 is the calculated exponentially weighted moving average covariance. t is the time 
and r is the weekly return for a given country. The unknown κ in the model is chosen, by 
convention, to be 0.94 for weekly return data10. The correlation in the first period is the 
 
8 Thai Crisis dates from Chiang et al. (2007)
9 The EWMA was popularized by RiskMetricks (Longerstaey, 1996)
10 κ = .94 is the RiskMetrics model developed by J.P Morgan 
22
sample covariance of the entire data set. Correlations, ρ, are calculated using Equation 
3.5.2 below and used to in the exploratory data analysis for returns. 
 
 
 
(3.5.2)
4 Results
4.1Return Results
4.1.1 Exploratory Analysis
We perform exploratory analysis on country returns by analyzing the trends in 
correlations estimated from the equations 3.5.1 and 3.5.2 between Thailand and each 
country (or cluster) during the Thai crisis period. The economic downturn spread to 
neighboring Asian countries and contributed to financial contagion, described by Chiang 
et al. (2007), as can be seen in Figure 5. Correlation levels during the Thai Crisis period
are graphed using a gradient heat map. Regional clusters of EMEA, Asia, and South 
America are also included. During the crisis period, it appears that return correlations
have increased over time. The increase in correlation rolls through Asia as indicated by
the wavy black line. We will use Equations 3.3.1 and 3.4.1 to assess whether financial 
instability in Thailand during the Thai crisis period increased the predictability between 
weekly returns in Asian countries. 
23
Figure 5. Correlation Levels with Thailand during Thai Crisis
Correlation (ρ) Legend: Darker = higher correlation
In Figure 6, the EWMA correlations during the Credit Crisis are provided using 
the same methodology as in Figure 5. As seen in Figure 6, the correlations during the 
period of the Credit Crisis were extremely high for not only Asian countries but also
countries in other geographic regions. During the Thai Crisis on the other hand, only 
Asian countries experienced increased return correlations. Also, correlations across all of 
EM were generally higher prior to the Credit Crisis, relative to levels around the time of 
the Thai Crisis. 
Indonesia Malaysia Asia Taiwan Korea China S.Africa Chile EAME Brazil Mexico S.Amer India Turkey
Jul-97
Jul-98
Jan-99
Jan 98
24
Figure 6. Weekly Returns Correlation Levels with China during Credit Crisis
Correlation (ρ) Legend: Darker = higher correlation
4.1.2 Thai Crisis Return Results
Table 2 summarizes the regression results from using Equations 3.3.1 and 3.4.1 to 
analyze the Thai Crisis from July 1997 to December 1998. Selected results for China, 
Indonesia, and Brazil are shown with relevant estimated coefficients for the regression 
with lagged Thai returns as an explanatory variable11. Panel A of Table 2 provides the 
coefficients for the relationship between each “dependent” country and Thailand’s lagged 
returns for the entire sample period given by (Equation 3.3.1), with the adjusted 
 of 
 
11 Complete tables can be found in the Appendix B.
Indonesia Malaysia Asia Taiwan Korea China S.Africa Chile EAME Brazil Mexico S.Amer India Turkey
Jul-07
Jul-08
Jan-09
Jan 08
25
the regression model in the next column. Panel B contains the coefficients for the 
indicator regression model (in Equation 3.4.1) and the adjusted 
 
.
 
(3.3.1)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
(3.4.1)
Table 2: Weekly Returns Regression with Thailand during Thai 
Crisis – July 1997 to December 1998
Panel A Panel B
Country 
 
 
 
 
 
 
China 0.1165 0.3765 -0.0230 0.2581* 0.5275
(0.0866) (0.0416) (0.0929)
Indonesia 0.0204 0.4075 0.0116 0.2275 0.4150
(0.0612) (0.0574) (0.1281)
Brazil -0.0084 0.4079 0.0204 -0.1851* 0.4397
(0.0622) (0.0415) (0.0925)
* significant at the .05 level
By comparing to 
 
and 
 
, we can contrast the relationship between the 
returns of China, Indonesia, and Brazil, relative to Thailand’s lagged returns, both for the 
entire sample period and for the Thai Crisis period. The statistically significant 
 
indicates that Thailand’s returns have additional explanatory power on the returns of 
China and Brazil during the crises period, while lack of significance in indicates lack 
of explanatory power of Thailand’s returns on the “dependent countries” over the sample 
period as a whole. From Table 2, it thus appears that there is an increased lagged return 
relationship with Thailand for both China and Brazil during the crisis. 
Insights regarding the nature of the return relationships can be derived not only 
from the statistical significance of the indicator variable 
 
but also from the sign and 
relative magnitudes of the coefficients. During times of crisis, when the indicator variable 
is 1, the total magnitude of the relationship with lagged Thailand returns is the sum of 
26
magnitudes of 
 
and 
 
. The magnitude of 
 
indicates the extent to which the dependent 
country is additionally affected by Thai returns during the crisis period. As seen in Table 
2 for China and Brazil, it appears that there is an increased return relationship for both 
China and Brazil during the crisis. The amplification of the relationships with lagged 
Thai returns would indicate predictable return relationships derived from declining equity 
returns spreading to other countries during a crisis. Furthermore, the positive sign of the 
coefficient for China suggests China’s returns move in an amplified direction compared 
with Thailand’s returns. There is also meaningful increase in the adjusted 
 between the 
two models, which provides further evidence of an increase in the impact of lagged Thai 
returns on China during the crisis. The negative coefficient in the case of Brazil might
indicate a change in portfolio allocations in emerging markets during the crisis, with 
investors assuming that all of Asia would be affected by Thai currency collapse, but that 
South America’s geographic distance would immunize it from the Asian crisis.
The lack of significance of 
 
in Indonesia indicates the absence of additional 
explanatory power of Thailand’s returns on Indonesia’s during the crisis. While 
correlations between Indonesia and Thailand appear to have increased based on Figure 5,
the lack of an amplified relationship during a crisis may be explained close geographic 
proximity of Thailand and Indonesia. Impact from Thailand’s returns on Indonesia’s 
happen on an almost contemporaneous basis, such as hours or days, rather than the
weekly returns that we use in our analysis12. This may explain the lack of significance on 
all the coefficients in the Indonesia regressions. All in all, the significant relationships 
 
12 Analysis on higher frequency data could be part of future studies.
27
that exist between Thailand with China and Brazil point to contagion that does not exist 
in non-crisis periods.
4.1.3 Credit Crisis Return Results
In order to analyze the Credit Crisis period, we use Equations 3.3.1 and 3.4.1 for 
two explanatory countries, Thailand and China. We use Thailand to facilitate comparison 
with the Thai Crisis results. 
 
(3.3.1)
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
(3.4.1)
Table 3: Weekly Returns Regression with Thailand during Credit 
Crisis – April 2007 to March 2009
Panel A Panel B
Country 
 
 
 
 
 
 
China 0.0227 0.4851 0.0411 -0.1303 0.4861
(0.0378) (0.0395) (0.1474)
Indonesia 0.0662 0.3764 0.0781 -0.1975 0.3747
(0.0515) (0.0541) (0.2016)
Brazil -0.0212 0.4082 -0.0219 -0.0209 0.4129
(0.0370) (0.0386) (0.1440)
* significant at the .05 level
Table 3 displays regression results for the Credit Crisis, with Thailand as the 
explanatory variable. The lack of significance in 
 
any of the coefficients indicates no 
significant relationships with Thailand’s lagged returns during this period. The inference 
is supported by the almost identical adjusted 
 between the two models. 
28
Table 4 displays regressions with China’s returns as the independent variable. 
Here again we observe no significance in any of the indicator variables. The likely 
explanation is that the Credit Crisis did not originate in these countries but in fact, had 
originated in the United States. Weekly returns in China therefore had no additional 
significant explanatory power during this period. Similar to Table 3, we again observe 
that the adjusted 
 did not change between the two models. Unlike the Thai Crisis, the 
lack of significant findings in returns fails to show evidence for contagion during the 
Credit Crisis. 
4.2 Dispersion Results
4.2.1 Thai Crisis Dispersion Results
Tables 5, below, summarizes the regression results from Equations 3.3.2 and 3.4.2
for the Thai Crisis period, with Thailand as the explanatory variable. Again, selected 
results for China, Indonesia, and Brazil are shown with relevant coefficients
13
. The 
following regressions are used:
 
 
 
 
 
(3.3.2)
 
13 Complete Tables can be found in Appendix C.
Table 4: Weekly Returns Regression with China during Credit 
Crisis – April 2007 to March 2009
Panel A Panel B
Country 
 
 
 
 
 
 
Thailand -0.0560 0.4155 -0.0488 -0.0038 0.3916
(0.0396) (0.0410) (0.1443)
Indonesia -0.0587 0.3760 -0.0402 -0.2196 0.3747
(0.0528) (0.0552) (0.1941)
Brazil 0.0572 0.4099 0.0341 0.2233 0.4165
(0.0379) (0.0393) (0.1382)
* significant at the .05 level
29
 
 
 
 
 
 
 
 
  
 
 
 
 
 
 
 
 
 
 
  
(3.4.2)
Table 5: Weekly Dispersion Regression with Thailand during 
Thai Crisis – July 1997 to December 1998
Panel A Panel B
Country 
 
  
 
China 0.1570* 0.3119 0.2374* -0.1721* 0.1213
(0.0265) (0.0450) (0.0484)
Indonesia 0.4439* 0.3171 0.1036 0.2881* 0.3824
(0.0402) (0.0661) (0.0710)
Brazil 0.1733* 0.3198 0.1814* 0.0390 0.3320
(0.0206) (0.0353) (0.0379)
* significant at the .05 level
The second column provides summary data for Equation 3.3.2. After accounting 
for market effects, all three countries’ dispersions have statistically significant positive 
relationships with Thailand’s dispersion in the previous week. In general, when 
Thailand’s dispersion increased, Indonesia, China, and Brazil’s dispersion increased in 
the following week. This is potentially explained by autocorrelation in time series 
volatility (Bollerslev, 1986). Equation 3.3.2 does not differentiate between periods in the 
Thai Crisis and those outside of the crisis. In order to determine if Thailand’s dispersion 
in the previous week had an additional impact on China, Indonesia, and Brazil during the 
Thai Crisis, we utilize the results from Equation 3.4.2.
 
 
and 
 
are the coefficient estimates from Equation 3.4.2. From Table 5, it can 
be seen that the Thai Crisis has an additional impact on dispersion in both China and 
Indonesia, but not in Brazil. Thailand’s effect on China’s dispersion decreases during the 
Thai Crisis, as noted by the negative value of 
 
. During the Thai Crisis, returns became 
more volatile, resulting in uncertainty in the directional movements of all Thai stocks and 
30
thus increased dispersion. This is because certain stocks went down more than others 
during the Crisis. Figure 5 in section 4.1.1 shows that China’s returns correlation with 
Thailand during the Thai Crisis was not as high as other Southeast Asian countries, such 
as Indonesia. This implies that while uncertainty existed in the Thai market, increasing 
Thai dispersion, the effect would not fully reach the Chinese market. China, then, would 
not experience such an increase in dispersion. 
Thailand’s dispersion does not significantly impact Indonesia’s dispersion during 
periods outside of the Thai Crisis, as indicated by the lack of significance of 
 
. However, 
during the crisis, 
 
is statistically significant, indicating that Thailand’s dispersion from 
the previous week has a positive relationship with Indonesia’s dispersion during the crisis 
period. Indonesia’s stocks may have performed similar to Thailand’s, with certain assets 
losing more value than others, thereby increasing dispersion during the time of the Thai 
Crisis.
In Brazil, the Thai Crisis has no statistically significant additional impact on 
dispersion – the estimate for 
 
is not significant at the 0.05 level. However, Thailand’s 
dispersion does appear to be positively related to Brazil’s dispersion for the sample 
period excluding the Thai Crisis. Because the Thai Crisis effects were stronger for Asian 
countries compared to South American countries, Brazil’s market does not experience the 
same return volatility14. Instead of some stocks falling in value more than others (thus 
attributing to contagion), Brazil’s stocks may not have experienced this increase in 
dispersion during the Thai Crisis. Therefore, the dispersion in Thailand does not appear 
to provide additional influence on dispersion in Brazil in the Thai Crisis. 
 
14 Time series market volatility in Brazil during the crisis was 3.73%, compared to 11.54% and 7.86% in 
Indonesia and Thailand respectively.
31
4.2.2 Credit Crisis Dispersion Results
 
 
 
 
 
(3.3.2)
 
 
 
 
 
 
 
 
  
 
 
 
 
 
 
  
 
  
(3.4.2)
We now shift our focus to the Credit Crisis from April 2007 to March 2009. 
Applying regression Equations 3.3.2 and 3.4.2 once more, we use Thailand and China as 
regressors15. Table 6 displays the same regression statistics as Table 5 but for the Credit 
Crisis. Again, we see statistical significance in for all three countries. When 
Thailand’s dispersion increases, dispersion in China, Indonesia, and Brazil subsequently 
increase as well, holding all else constant. 
Table 6: Weekly Dispersion Regression with Thailand 
during Credit Crisis– April 2007 to March 2009
Panel A Panel B
Country 
 
  
 
China 0.1570* 0.3119 0.1530* 0.5026* 0.3295
(0.0265) (0.0268) (0.1115)
Indonesia 0.4439* 0.3171 0.4219* -0.0865 0.3204
(0.0402) (0.0412) (0.1711)
Brazil 0.1733* 0.3198 0.1952* 0.0012 0.3422
(0.0206) (0.0208) (0.0864)
* significant at the .05 level
The Credit Crisis does not result in statistically significant additional impact on 
the dependent countries’ dispersion except for China, where 
 
is statistically significant 
at the 0.05 level. During the Credit Crisis, China’s dispersion increases if Thailand’s 
dispersion rose the week before. A possible explanation is the fact that the Credit Crisis 
originated in the US. China is the largest economy in the set of emerging markets, and 
has financial ties to the US. The US may have a statistically significant impact on both 
Thailand and China’s dispersion. The seemingly strong relationship between Thailand 
 
15 The rationales for selecting China and Thailand are stated in the Section 2.1.
32
and China’s dispersion is then attributed to the US. Therefore, US dispersion may be a 
latent variable that might better explain the dispersion in Thailand and in China
(Goldstein, 2009).
Table 7 summarizes the results with China as the explanatory country. In 
Indonesia and Brazil, an increase in China’s dispersion, in general, increases their 
dispersion as well, as indicated by the significance in from Equation 3.3.2. There is no 
significant relationship between China’s dispersion and that of Thailand.
Table 7: Weekly Dispersion Regression with China during 
Credit Crisis – April 2007 to March 2009
Panel A Panel B
Country 
 
  
 
Thailand 0.0008 0.1421 0.4211* -0.3642* 0.1195
(0.0332) (0.0485) (0.0766)
Indonesia 0.3477* 0.2357 0.4020* -0.2367* 0.4319
(0.0566) (0.0593) (0.0937)
Brazil
0.1498* 0.2781 0.1769* -0.1182* 0.2927
(0.0283) (0.0298) (0.0472)
* significant at the .05 level
After adding the indicator variables (Equation 3.4.2), the results change. During 
periods outside of the Credit Crisis, an increase in China’s dispersion is expected to 
increase dispersion in Thailand, Indonesia, and Brazil. All three estimates are statistically 
significant at the 0.05 level. However, during the Credit Crisis, China’s dispersion level 
has a negative effect on dispersion in the three countries. This is denoted by the 
statistically significant negative estimates for 
 
. These results from Table 7 imply that 
while dispersion increased in China during the Credit Crisis, the respective dispersion in 
Thailand, Indonesia, and Brazil did not increase as much. Again, since the Credit Crisis 
originated in the US, there may be a latent variable at work (Goldstein, 2009). It would 
33
be interesting to see the relationship between US dispersion and the dispersion of the 
dependent countries.
Because China and Thailand’s previous week’s dispersion had a positive 
relationship (as seen in Table 6), one would naturally expect the same result when 
Thailand’s dispersion is regressed with China’s dispersion from the week before. 
However, coefficient for 
 
is negative in the case of Thailand in Table 7, however, it is 
positive in Table 6. After examining Figures 7 and 8 below, we see that it makes sense 
for 
 
to be less than 0. The solid line in each figure represents the regression during the 
Credit Crisis. When we invert the relationship, we invert the plots as well. While solid 
line is above the dashed line in Figure 7 (Thailand’s dispersion has a greater effect on 
China’s during the Credit Crisis), it is above the dashed line in Figure 8 (China’s 
dispersion has less of an effect on Thailand’s during the Credit Crisis). 
0
0.005
0.01
0.015
0.02
0.025
0.03
0.035
0 0.005 0.01 0.015 0.02 0.025 0.03 0.035
China Dispersion
Thai Dispersion
Figure 7. China Dispersion (Y) v. Thai Dispersion (X)
China (Credit Crisis) China (Non-Credit Crisis)
Linear (China (Credit Crisis)) Linear (China (Non-Credit Crisis))
34
Our regression results indicate contagion in Asian nations during the Thai Crisis. 
The regression results from the Credit Crisis do not imply the existence of contagion 
from Thailand or China to other countries. China’s impact on the dependent countries’ 
dispersion decreased during the Credit Crisis, and Thailand only significantly impacted 
China’s dispersion. The significant relationship between Thailand’s and China’s 
respective dispersion level is potentially explained the presence of a latent variable. Since 
the Credit Crisis originated in the US, it is possible that US dispersion has a statistically 
significant relationship with both Thailand and China’s dispersion. 
5 Conclusion 
Our thesis aimed to determine whether emerging equity markets showed evidence 
of contagion during the Thai Crisis and the Credit Crisis. We derived a multivariate 
0
0.005
0.01
0.015
0.02
0.025
0.03
0.035
0 0.005 0.01 0.015 0.02 0.025 0.03 0.035
Thai Dispersion
China Dispersion
Figure 8. Thai Dispersion (Y) v. China Dispersion (X)
Thai (Credit Crisis) Thailand (Non-Credit Crisis)
Linear (Thai (Credit Crisis)) Linear (Thailand (Non-Credit Crisis))
35
regression model that accounts for both a market effect and the country specific effect of 
returns (and dispersion), and applied indicator variables to distinguish between periods of 
a specific crisis from all other periods in the sample. 
We found that contagion existed between countries that are geographically close
to Thailand during the Thai Crisis. We also saw a positive relationship between the Thai 
returns and Chinese returns during the Thai Crisis, on the other hand, there existed a 
negative relationship between Thai returns and Brazil returns during this period. Our 
results for the regression models during the Credit Crisis did not indicate the existence of 
contagion among the emerging markets in this period. As previously mentioned, this may 
be explained by the fact that the Credit Crisis had originated in the United States or the 
Credit Crisis may be more global than the Thai Crisis. 
We found some evidence contagion through analyzing dispersion as well. As with 
returns, we found that contagion existed during the respective crises in countries in close 
geographic proximity to the source of the crisis. Indonesia’s dispersion had a positive 
relationship with that of Thailand from the previous week. Additionally, the regression 
results showed that Thailand’s impact on Indonesian dispersion was amplified during the 
Thai Crisis. Our model did not confirm the existence of contagion during the Credit 
Crisis. This may be explained by the same reasons as we outlined for returns.
Because the Credit Crisis originated in the US, further investigation is needed on 
the relationship between US returns and dispersion with those of emerging markets. In 
our thesis, we established that presence of contagion in the Thai Crisis between Thailand 
and neighboring Asian countries. We are also interested in a potential “ripple effect,” 
where contagion spreads from the Asian nations affected directly by the Thai Crisis to 
36
their neighbors. In the case of the Thai Crisis, our “pandemic” is the devaluation of the 
Baht in 1997, and we would monitor its spread from Thailand to China, Indonesia, 
Malaysia, and the Philippines, and from these four nations to their neighbors, and so on. 
Finally, adjusting the models to account for heteroskedasticity of the data, following
Forbes in 2002, could also be an area of future area research. While contagion has yet to 
be fully characterized, the relationships uncovered shed greater light on market behaviors 
during times of crisis. 
37
References 
Allen, F., & Gale, D. (2000). Financial Contagion. The Journal of Political Economy, 
108(1), 1-33.
Ankrim, E., & Ding, Z. (2002). Cross-Sectional Volatility and Return Dispersion.
Financial Analysts Journal, 58(5), 67-73.
Baig, T., and Goldfajn, I. (1999). Financial Market Contagion in the Asian Crisis. IMF 
Staff Papers, 46(2), 167-195.
Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. Journal 
of Econometrics, 31(3), 307-327.
Brunnermeier, M. (2009). Deciphering the Liquidity and Credit Crunch 2007-2008. 
Journal of Economic Perspectives, 23(1), 77-100. 
Campbell, J., Lettau, M., Malkiel, B., & Xu, Y. (2001). Have Individual Stocks Become 
More Volatile? An Empirical Exploration of Idiosyncratic Risk. The Journal of 
Finance, 56(1), 1-43.
Campbell, J., & Lo., A. (1996). The Econometrics of Financial Markets. Princeton, New 
Jersey: Princeton University Press.
Chiang, T., Nam Jeon, B., & Li, H. (2007). Dynamic correlation analysis of financial 
contagion: Evidence from Asian markets. Journal of International Money and 
Finance, 26(70), 1206-1228.
Egger, D., & Jacob, J. (2010). Emerging Markets: Return Dispersion and Portfolio 
Concentration. Lazard Investment Research.
Engle, R. (2009). Anticipating Correlations: A New Paradigm for Risk Management. 
Princeton, New Jersey: Princeton University Press.
Fama, E. (1970). Efficient Capital Markets: A Review of Theory and Empirical Work. 
The Journal of Finance, 25(2), 383-417.
Forbes, K., & Rigobon, R. (2001). International Financial Contagion. Norwell, 
Massachusetts: Kluwer Academic Publishers.
Forbes, K., & Rigobon, R. (2002). No Contagion, Only Interdependence: Measuring 
Stock Market Comovements. The Journal of Finance, 57(5), 2223-2261.
38
Glick, R., & Rose, A. (1999). Contagion and trade: Why are currency crises regional?. 
Journal of International Money and Finance, 18(4), 603-617.
Goldstein, M., & Xie, D. (2009). US Credit Crisis and Spillovers to Asia. Asian 
Economic Policy Review, 4, 204-222.
Lim, K. Brooks, R., & Kim, J. (2008). Financial crisis and stock market efficiency: 
Emperical evidence from Asian countries. International Review of Financial 
Analysis, 17(3), 571-591.
Lintner, J. (1965b). The Valuation of Risk Assets and the Selection of Risky Investments 
in Stock Portfolios and Capital Budgets. The Review of Economics and Statistics, 
47(1), 13-37.
Longerstaeu, J. (1996). RiskMetrics – Technical Document. New York: Morgan Guaranty 
Trust Company.
Park, Y., & Song, C. Institutional Investors, Trade Linkage, macroeconomic Similarities, 
and Contagion of the Thai Crisis. Journal of the Japanese and International 
Economies, 15 (2), 199-224.
Sharpe, W. (1964). Capital Asset Prices: A Theory of Market Equilibrium under 
Conditions of Risk. The Journal of Finance, 19(3), 425-442.
Solnik, B., & Roulet, J. (2000). Dispersion as Cross-Sectional Correlation. Financial 
Analysts Journal, 56(1), 54-61.
Yu, W., & Sharaiha, Y. (2007). Alpha budgeting – Cross-sectional dispersion 
decomposed. Journal of Asset Management, 8, 58-72.
39
Appendix A: Complete Country List and Cluster Breakdowns
Countries EMEA Cluster South America 
Cluster Asia Cluster
Brazil Morocco Colombia Philippines
Chile Oman Argentina Vietnam
China Mauritius Venezuela Laos
Indonesia Pakistan Peru
India Qatar Panama
Korea Poland
Mexico Portugal
Malaysia Romania
Thailand Russia
Turkey Slovenia
Taiwan Slovakia
South Africa Tunisia
Ukraine
Latvia
Libya
Greece
Egypt
Estonia
Czech Republic
Cyprus
Botswana
Bahrain
Bulgaria
Croatia
Hungary
Kazakhstan
Kuwait
Jordan
United Arab 
Emirates
Israel
40
Appendix B: Full Tables for Returns
I. Regressions without Indicators
 
(3.3.1)
Table 8: Weekly Returns Regression with Thailand
Country 
 
Brazil
0.9515* 0.0886 -0.0084 0.4079
(0.0455) (0.0570) (0.0622)
Chile
1.1640* -0.0908 -0.0043 0.4848
(0.0464) (0.0581) (0.0635)
China
1.2502* -0.0349 0.1165 0.3765
(0.0633) (0.0793) (0.0866)
Indonesia
0.9342* 0.0726 0.0204 0.4075
(0.0447) (0.0561) (0.0612)
India
1.5092* -0.0085 -0.0555 0.5361
(0.0546) (0.0684) (0.0747)
Korea
0.8034* 0.0392 -0.0791 0.4434
(0.0351) (0.0439) (0.0480)
Mexico
0.8951* -0.0131 0.1141* 0.4467
(0.0396) (0.0496) (0.0541)
Malaysia
1.0113* 0.0166 0.0708 0.4148
(0.0475) (0.0595) (0.0650)
Turkey
1.0923* -0.1414 0.1614 0.2317
(0.0775) (0.0972) (0.1061)
Taiwan
0.9951* -0.0675 0.0379 0.5323
(0.0362) (0.0454) (0.0496)
South Africa
0.8423* -0.0327 -0.0921 0.4272
(0.0376) (0.0471) (0.0515)
EMEA
0.6352* 0.0381 -0.0810* 0.5172
(0.0239) (0.0300) (0.0327)
S.Amer
0.6451* 0.0132 0.0201 0.4416
(0.0285) (0.0357) (0.0390)
Asia
0.9622* -0.0081 0.0392 0.4297
(0.0434) (0.0544) (0.0594)
* significant at the .05 level
41
Table 9: Weekly Returns Regression with China
Country 
 
Brazil
0.9563* 0.0173 0.0572 0.4099
(0.0455) (0.0632) (0.0379)
Thailand
1.0087* 0.1209 -0.0560 0.4155
(0.0475) (0.0661) (0.0396)
Chile
0.5445* 0.0820* 0.0058 0.3803
(0.0281) (0.0391) (0.0234)
Indonesia
1.2487* 0.0978 -0.0587 0.3760
(0.0634) (0.0882) (0.0528)
India
0.9358* 0.0715 0.0107 0.4075
(0.0448) (0.0623) (0.0373)
Korea
1.5099* -0.0722 0.0284 0.5359
(0.0547) (0.0760) (0.0455)
Mexico
0.8042* -0.0477 0.0371 0.4425
(0.0352) (0.0489) (0.0293)
Malaysia
0.8972* 0.0691 -0.0165 0.4432
(0.0398) (0.0553) (0.0331)
Turkey
1.0953* -0.0267 -0.0219 0.2291
(0.0778) (0.1082) (0.0648)
Taiwan
0.9967* -0.0512 0.0041 0.5319
(0.0363) (0.0505) (0.0302)
South 
Africa
0.8439* -0.1423* 0.0504 0.4267
(0.0377) (0.0524) (0.0314)
EMEA
0.6322* 0.0003 -0.0060 0.5129
(0.0241) (0.0335) (0.0200)
S.Amer
0.6470* 0.0071 0.0148 0.4417
(0.0286) (0.0397) (0.0238)
Asia
0.9585* 