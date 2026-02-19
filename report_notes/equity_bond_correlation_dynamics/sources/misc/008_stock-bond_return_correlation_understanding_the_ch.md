---
url: https://dspace.stir.ac.uk/retrieve/ec2513f8-8568-4e9c-9a79-648e7797f523/1-s2.0-S1042443125001325-main.pdf
title: Stock-bond return correlation: Understanding the changing behaviour
domain: misc
crawled_at: 2026-02-04T08:03:15.610767+00:00
source: exa_search
author: David G. McMillan
chart_count: 0
image_links:
outbound_links:
---

Stock-bond return correlation: Understanding the 
changing behaviour
David G. McMillan 1
Division of Accounting and Finance, University of Stirling, UK
ARTICLE INFO
JEL:
C22
G12
G15 
Keywords:
Stock returns
Bond returns
Time-varying correlation
Growth
Inflation
Real interest rates
Breakpoint regression
ABSTRACT
The stock and bond return correlation remains important given its central role in portfolio 
behaviour. Previous, primarily US, evidence indicates sign switching, which implies that bonds 
change between diversifying and hedging behaviour. This paper considers time-variation in the 
stock–bond correlation for the G7 markets, including the nature of its economic drivers. Using 
monthly data over a period spanning 1980 to 2023 evidence demonstrates that the correlation 
switches from positive to negative in the late 1990s for six of the seven markets (the switch for 
Japan occurs in the first half of the 1990s). A switch back to positive is observed towards the end 
of the sample for most markets but earlier for France and Italy. Evidence of time-variation within 
the correlation drivers is also noted. Nonetheless, results suggest that inflation and interest rates 
typically exhibit a positive effect on the correlation, consistent with previous work and theoretical 
underpinnings. That is, higher inflation and interest rates depress stock and bond prices due to 
higher discount rates and lower real cash flows, moving them in the same direction. Growth also 
largely imparts a positive effect on the correlation, but this contrasts with the prevailing view. 
This arises through portfolio considerations where higher growth leads to an increase in demand 
for all assets. Of importance for investors, the switch in correlation implies that a portfolio 
manager will need to alter asset weights to maintain a target value for returns or risk. A portfolio 
variance decomposition reveals that while the bond contribution remains broadly constant over 
the sample, that from stocks increases as the correlation contribution shifts from positive to 
negative. The results are of importance to investors and those engaged in modelling market 
behaviour.
1. Introduction
The stock–bond return correlation remains an important ingredient in our understanding of financial markets and for portfolio 
managers, and where it is recognised that the correlation is time-varying.2 Moreover, that understanding can be enhanced through an 
examination of the drivers of correlation movement, and a consideration of key implications that arise from such movement. This 
E-mail address: david.mcmillan@stir.ac.uk. 1 Address: Accounting and Finance Division, University of Stirling, FK9 4LA, UK. 2 More specifically, this literature refers to the correlation between a country’s major stock market index and long-term (typically 10-year) 
sovereign (Treasury) bonds. These assets forming the foundation stones of many portfolio holdings.
Contents lists available at ScienceDirect
Journal of International Financial Markets, 
Institutions & Money
journal homepage: www.elsevier.com/locate/intfin
https://doi.org/10.1016/j.intfin.2025.102242
Received 20 March 2025; Accepted 13 October 2025 
J. Int. Financ. Markets Inst. Money 106 (2026) 102242
Available online 30 October 2025
1042-4431/© 2025 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY license
(http://creativecommons.org/licenses/by/4.0/).
paper examines the stock–bond correlation for the G7 markets in the light of more recent economic and geopolitical shocks (from the 
global financial crisis, and Covid-19 to the Russian invasion of Ukraine and subsequent high inflation).3 Of importance, this paper 
argues that not only is the stock–bond correlation time-varying, but also the conditioning nature of key macroeconomic determinants 
for correlation movement. This arises due to the changing risk characteristics of both growth and inflation for stock and bond markets, 
and with implications for the relative weights of each asset within a portfolio.
Much of the impetus to the research examining stock–bond correlation dynamics comes from the observation that the correlation 
switched from being positive to negative in the early 2000s in the US market. Thus, bonds switched from acting as a diversifier within a 
stock–bond portfolio to a hedger. This early research includes Andersson et al. (2008), Aslanidis and Christiansen (2012) and Gulko 
(2002).
4 Key within this line of research is a desire to understand the drivers of such a switch in correlation. This is often ascribed to a 
flight-to-safety effect following the dotcom crash and the broader changing economic conditions that followed, including heightened 
economic risk (arising, for example, from the financial crisis and Covid-19) and a prolonged period of low interest rates. This greater 
risk led investors to seek safer assets and so moving into bonds and out of stocks, creating a negative correlation. This also aligns with 
the idea that bonds serve as a safe haven (or hedge) in such periods of risk. In contrast, when the economic environment is charac
terised by lower risk, investors are more likely to take a dominant position in stocks, with bonds acting as a diversifier, leading to a 
positive correlation. Correlation shifts thus arise from the evolving risk appetite of investors.
Recent work suggests that this correlation may have returned to a positive value following the high inflation period of 2022 (e.g., 
Lombardi and Sushko, 2023; Brixton et al., 2023). While this period has seen an increase in interest rates, it remains one of high 
economic risk (especially arising from the Russian invasion of Ukraine). Again, understanding the reason for the switch remains as 
equally important as acknowledging the switch. Moreover, this includes examining whether the factors that drive the early 2000s 
switch are the same as those that determine the early 2020s switch. The current literature suggests two broad sets of variables that can 
explain the time-varying nature of the correlations. This relates to inflation-based reasons and growth-based reasons. For example, 
higher inflation (and interest rates) is typically linked to lower stock and bond prices, creating a positive relation, however, there is 
some evidence that stocks may respond in the opposite direction. Higher output is likely to lead to a negative correlation with higher 
stock and lower bond prices, but equally, the opposite correlation can be supported. See, for example, the discussion in Li (2002), 
Duffee (2023), Portelli and Roncalli (2024), Jones and Pyun (2025) among others.
This paper seeks to contribute to the literature by considering three elements of this debate. First, the paper considers the stock and 
bond return correlation for the G7 markets. The majority of research focuses on the US market; however, it is important to consider 
whether the same change and the same factors are equally present in a wider selection of markets. Nonetheless, there are some ex
ceptions to this and, for example, Ponrajah and Ning (2023) and Molenaar et al. (2024) do consider a range of international markets. 
Second, we examine the drivers of the change in correlation. As noted, several papers have previously considered this, but we seek to 
report on whether the nature of those factors changes between the early 2000s switch and the early 2020s one. More specifically, the 
literature identifies several key variables in explaining the time-varying correlation. This includes the real interest rate, inflation and 
output and hypothesises that the former two have a positive effect on the correlation and the latter a negative relation (in addition to 
the above noted papers, also see, Aslanidis and Christiansen, 2012; Viveira, 2012; McMillan, 2019). However, the opposite relations 
are possible, which leads to mixed results, and this paper seeks to examine this. Third, we consider the implications of the correlation 
switches for a stock and bond portfolio. Notably, considering how it affects both portfolio returns and variance, which are of key 
importance for investors.
We obtain monthly data for the G7 markets over the time period ranging from January 1980 to December 2023, although the exact 
sample starting point varies by country. This data consists of the stock and bond index from which return correlations are derived. Data 
is also collected to model the changing correlation, including inflation, output growth and Treasury yields. The results indicate several 
key points that are of interest to investors and those engaged in modelling financial markets. The stock–bond return correlation for all 
G7 markets does switch between being positive and negative. For five (Canada, France, Germany, UK and US) of the markets, the 
pattern of behaviour in the correlation is broadly similar. However, Italy and Japan exhibit differences with the former presenting a 
mostly positive correlation with only a short switch to negative, while the opposite is found for the latter. Further, the factors that 
determine the correlation dynamics, themselves, change over time both in terms of sign and significance, although the real interest rate 
is the most consistent predictor. Generally, however, interest rates, inflation and growth impart a positive effect on the correlation, 
although not without exceptions.
These results demonstrate that the switching correlation behaviour has implications for a stock–bond portfolio. This is in terms of 
both returns and risk with, for example, a lower return to a fixed weight portfolio when a negative correlation occurs. Indeed, the 
results highlight the need to alter weights to maintain a fixed return or risk (standard deviation) value. A portfolio variance 
decomposition also highlights the effect of the changing correlation in regard of diversification. These implications in turn provide the 
key contributions of the paper. Notably, extending our understanding of the ongoing debate surrounding the role of inflation and 
growth factors in the time-varying correlation and, especially, demonstrating that their relative importance varies over time.
3 The choice of the G7 is motivated by these countries having the seven of the eight largest global sovereign bond markets (noting the exclusion of 
China, which is the second largest). Six of these countries are also in the top ten of global stock markets by size. 4 Also see, for example, Baele et al. (2010), Campbell and Ammer (1993) and Connolly et al. (2005).
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
2
2. Background
There is an ongoing literature that seeks to understand the time-varying nature of the stock–bond correlation, linking it to 
movements in economic variables. Initial work considers the sign of the correlation, with Barksy (1989), Shiller and Beltratti (1992)
and Campbell and Armer (1993) supporting a positive relation and Gulko (2002), Connolly et al. (2005) and Andersson et al. (2008)
suggesting a negative one. Subsequent work argues that these results highlight the switching relation between the two assets, which is 
often linked to changing market and economic conditions, notably, flight-to-safety effects during crisis periods. For example, Ponrajah 
and Ning (2023) use a copula approach to identify regime switching between periods of flight-to/from-safety. Arising from this, several 
papers link this time-varying correlation to explicit macroeconomic and financial variables, including inflation, interest rates and 
output growth (e.g., Baele et al., 2010; Aslanidis and Christiansen, 2012, 2014; Viceira, 2012; Aslanidis et al., 2019).
These empirical observations led to the development of theoretical models designed to underpin and explain the nature of the 
identified relations. In an earlier model, Li (2002) argues that the source of the shock matters for the sign of the correlation, with 
interest rate shocks leading to a positive relation and inflation or dividend shocks resulting in a negative one. Subsequently, a series of 
papers consider the role of different macroeconomic shocks for the stock–bond correlation, including output and consumption growth 
shocks, as well as changes in real (as opposed to nominal) interest rates (see, for example, Burkhardt and Hasseltoft, 2012; Chernov 
et al., 2021; Jones and Pyun, 2025).
Duffee (2023) argues that macroeconomic shocks can produce either a positive or negative stock–bond correlation. Duffee high
lights the persistence nature of macroeconomic shocks and the degree of economic uncertainty as being key determinants of the 
correlation. Moreover, as Brixton et al. (2023) note, the broad view appears to be whether inflation or growth considerations 
dominate.5 Higher inflation will lead to higher expected interest rates, which depresses both stock and bond prices and so a positive 
relation arises. Whereas if higher expected interest rates arise from higher growth, then while bond prices will still fall, stock prices 
would be expected to rise, leading to a negative correlation. Furthermore, these effects will interact and vary according to wider 
economic conditions. For example, after the financial crisis, (very) low interest rates might be expected to raise both stock and bond 
prices, but the lower rates were also an indicator of poor expected future conditions and so stock prices continue to fall (e.g., Gregoriou 
et al., 2009).
Within this line of thought, several recent papers link the stock–bond correlation to a key macroeconomic correlation, sometimes 
referred to as the nominal-real correlation, between inflation and growth (see, for example, David and Veronesi, 2013; Song, 2017; 
Boon et al., 2020; Campbell et al., 2020). This research notes a change in the inflation-growth correlation from negative to positive at a 
time similar to the switch from positive to negative in the stock–bond correlation. This again, revolves around the nature of inflation 
and growth, where higher inflation prior to the 2000s, and especially before the financial crisis is associated with lower growth and 
lower stocks (in line with Fama, 1981), but after this period, higher inflation is associated with improving economic conditions, 
offsetting the fear of deflation, leading to higher growth and stocks. While acknowledging that inflation plays a role in the stock–bond 
correlation, Jones and Pyun (2025) argue that consumption growth persistence is a more important driver. Moreover, the nature of 
consumption growth on the stock–bond correlation arises through movements in real interest rates that result from intertemporal 
substitution.
Therefore, in assessing the factors that can affect the stock and bond return correlation, we can generate several hypotheses that can 
be tested. First, higher real interest rates should lead to a positive correlation as they would be associated with lower value of expected 
cash flows. That is, as the rate as which expected future cash flows are discounted rises, so the price of the assets falls, generating a 
positive correlation. However, it is noted that this relation may not hold under all conditions. For example, Gregoriou et al. (2009) note 
a change in the stock market response to falling interest rates during the financial crisis. This arises because the discount rate not only 
contains the interest rate but also a risk premium. The lower interest rates are a sign of worsening economic conditions during the 
financial crisis and thus, while bond prices rise in line with the lower rates, stock prices continue to fall. Second, inflation will also lead 
to a positive correlation as inflation will be related to future interest rate changes. Inflation reduces the value of real cash flows and 
leads to greater macroeconomic uncertainty and risk. However, where stocks act as a hedge against inflation, then a negative cor
relation can emerge. Evidence also exists of a positive relation between inflation and the dividend yield (e.g., Sharpe, 2001; Ritter and 
Warr, 2002; Bekaert and Engstrom, 2010), which implies higher future stocks and a negative correlation. Recent work from Duffee 
(2023) highlights that the nature of inflations role on the correlation is not clear, while earlier, Campbell et al. (2017) note a changing 
nature of the risk premium over time.
Third, output growth is also a factor in determining the correlation and is likely to generate a negative correlation between stock 
and bond returns. As noted above, this arises from the well-established flight-to-safety phenomenon, where investors move from stocks 
to bonds at a time of economic crisis, generating a negative correlation.6 Equally, in a time of growth, investors will have expectations 
of higher future cash flows and so stock prices rise, whereas bond prices may be falling due to higher expected future interest rates. 
Again, generating a negative correlation. In contrast, within a growing economy, investors are likely to demand more of all assets, 
creating a positive correlation, consistent with diversification behaviour within portfolio theory. As a fourth hypothesis, the nature of 
the relation between inflation and output on the stock–bond correlation may also depend on the nature of the interaction between the 
two macroeconomic variables themselves and specifically, the changing risk characteristics of inflation. That is, with inflation being 
associated with lower growth in the first part of the sample (as higher inflation results in households and firms delaying consumption 
5 This view is also espoused in the paper of Portelli and Roncalli (2024) that provides an extensive overview of the research area. 6 An opposite ‘flight-to-risk’ effect might be present during expansionary periods with investors moving from bonds to stocks.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
3
and investment due to lower purchasing power), and higher growth in the second (as both inflation and growth were subdued such that 
higher inflation is an indication of improving economic conditions).
Thus, while there may be a general expectation that real interest rates and inflation lead to a positive correlation and output to a 
negative correlation, there are valid arguments to suggest the opposite. Moreover, that the sign and strength of any relation on the 
correlation will vary over time, and therefore, the fifth hypothesis states that we would expect the nature of the factors that condition 
the correlation to change over the sample period. This paper seeks to considers these issues below.
3. Data and time-varying correlations
3.1. Data
We obtain monthly stock and (sovereign 10-year) bond index return data for the G7. The sample starting period varies according to 
data availability, with the data obtained from LSEG DataStream. Fig. 1 presents the time series plots for the stock and bond price data, 
while Table 1 presents the summary statistics for the returns, and includes the sample start date, which varies from 1980 to 1991, with 
the end of the sample period being December 2023 for all series. While the plots (in Fig. 1) are shown for all available data, the 
summary statistics are for the common sample (as can be observed in Fig. 1, the stock price series is longer than that available for the 
bond price) to provide comparison. These summary statistics support our usual understanding of stock and bond return series. Stocks 
have a higher return than bonds, and this is accompanied by a higher standard deviation and a greater minimum to maximum range. 
All returns series, exhibit non-normality, notably with negative skewness (except US bond returns) and excess kurtosis.
The other data used in this paper consists of the consumer price index, industrial production and the 10-year Treasury bond yield, 
all taken from the same data source. From these, we construct inflation and the growth rate of output (as the log difference of the 
consumer price index and industrial production, respectively) and the real interest rate (as the difference between the 10-year Treasury 
yield and inflation). Summary statistics for this data is not presented but is available upon request.
3.2. Time-varying stock-bond correlation
To give some indication of time-variation in the stock and bond return correlations, Table 2 presents the Pearson correlation over 
the full sample of available data for each country and then separated into the first and second half of the sample for each country (and 
so, the exact sample dates differ across some of the countries). Taking the full sample correlations, we can see a mix of generally small 
positive and negative correlations across the G7 markets, with only Italy indicating some different behaviour, with a more moderate 
positive correlation. However, a clearer pattern can be seen when we separate the correlations between the first and second half of the 
respective samples. Across the first half of the sample for each market there is a positive correlation between stock and bond returns. 
Fig. 1. Time Series Plots. Notes: Graphs depict the time-series plot of the stock and bond index for each series.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
4
For most of the markets, this correlation is relatively moderate in magnitude, although for Japan, it is near zero. In the second half of 
the respective samples, the stock–bond correlation is negative for all markets, except Italy. Again, the correlations are moderate in size, 
except for France, which has a near zero negative correlation. Thus, there is a clear pattern of a positive stock–bond return correlation 
switching to negative over the sample period. The only exception to that is for Italy, for which a similar sized positive correlation exists 
in both sample halves.
In addition to these statistics, Table 3 presents the mean stock and bond return, as well as the correlation, over different macro
economic regimes, i.e., periods of increasing and decreasing output growth (change in industrial production) and inflation (the change 
in inflation rather than just inflation, which is mostly positive throughout). These results highlight some notable differences across 
regimes for both stock and bond returns and how they interact. During periods of positive economic growth, we see that stock returns 
are greater than bond returns for each of the markets, while the converse is generally true in periods of negative economic growth, 
although not uniquely with both the UK and US still exhibiting higher stock returns. There is no obvious pattern for the correlations 
across the two regimes. Here, both positive and negative correlations are present, although the correlation is generally higher in the 
positive growth regime (including being less negative for some markets). Comparing periods of rising and falling inflation, we observe 
higher stock returns with the former and higher bond returns with the latter. In terms of the correlations, again, we observe evidence of 
both positive and negative correlations in each regime, while being generally higher in the regime associated with increasing inflation.
The results from Tables 2 and 3, highlight the indicative presence of time-variation within the stock and bond return correlation. To 
consider this more robustly, we estimate the time-varying correlations utilising two common approaches. We use the DCC-GARCH 
model of Engle (2002) and a three-year rolling window correlation (rolling windows have previously been used by, for example, 
Rankin and Shah Idil, 2014). These two approaches are presented in Fig. 2 and reveal a notable degree of variation in each correlation 
series. Both approaches present a similar picture in terms of movement in the correlations, with the rolling correlations exhibiting 
greater variation around the same pattern. Correlation summary statistics are reported in Table 4.
As noted in the above cited literature for the US market, from both Fig. 2 and Table 4, we see a switch from a positive to a negative 
correlation during the sample period. This is equally observed for each of the G7 markets, although with some differences in behaviour. 
The plots for Canada, Germany, the UK and the US are broadly similar. Here, we see a positive correlation between stock and bond 
return series from the start of the sample until the early 2000s (except for temporary deviations) whereupon the correlation switches to 
negative. The correlation then remains negative until the last two years of the sample (again, except for transitory switches). The 
Table 1 
Stock and Bond Return Summary Statistics.
Series Sample Start Mean Std Dev Min Max Skew Kurt JB
Stock Returns
Canada 1985:01 0.534 4.350 − 24.988 15.114 − 1.309 9.322 0.00
France 1985:01 0.600 5.497 − 24.186 16.567 − 0.598 4.719 0.00
Germany 1980:01 0.472 5.377 − 26.825 14.750 − 0.878 5.344 0.00
Italy 1991:03 0.236 6.077 − 24.770 21.034 − 0.148 4.166 0.00
Japan 1984:01 0.268 5.511 − 24.431 17.445 − 0.441 4.577 0.00
UK 1980:01 0.561 4.575 − 31.823 13.196 − 1.245 8.944 0.00
US 1980:01 0.750 4.542 –23.660 14.021 − 1.003 6.968 0.00
Bond Returns
Canada 1985:01 0.116 2.042 − 7.411 7.209 − 0.095 3.794 0.00
France 1985:01 0.155 1.875 − 6.893 6.294 − 0.253 3.701 0.00
Germany 1980:01 0.086 1.848 − 8.289 5.827 − 0.525 4.555 0.00
Italy 1991:03 0.199 2.363 − 8.429 9.060 − 0.300 4.862 0.00
Japan 1984:01 0.131 1.520 − 7.848 6.395 − 0.542 8.076 0.00
UK 1980:01 0.150 2.417 − 9.177 8.278 − 0.453 4.866 0.00
US 1980:01 0.056 2.455 − 8.757 12.334 0.295 4.774 0.00
Notes: The entries are the mean, standard deviation, minimum, maximum, skewness, kurtosis and Jarque-Bera p-values for the monthly stock and 
bond returns. The sample start date is also shown, with the end date being 2023:12.
Table 2 
Stock-Bond Return Correlation (Pearson).
Full Sample First Half Second Half
Canada 0.034 0.163 − 0.117
France 0.105 0.221 − 0.033
Germany − 0.011 0.179 − 0.197
Italy 0.279 0.299 0.265
Japan − 0.043 0.022 − 0.238
UK 0.156 0.315 − 0.100
US − 0.008 0.217 − 0.237
Notes: Entries are the Pearson correlation for the stock and bond return series. The correlations are reported for the full 
sample as well as for a sample split that apportions 50 % of the data in each sub-sample. The exact dates differ in accordance 
with that outlined in Table 1 but occur in the early to mid-2000s for all series.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
5
pattern for France is similar, but with greater evidence of a move back to a positive correlation occurring earlier in the sample (mid2010s). Differences, however, can be observed for Italy and Japan. Although both series exhibit a switch from positive to negative and 
back, the timeframes differ to those noted above. For Italy, the period of a negative correlation is much shorter and could be argued to 
be a more temporary phenomenon, largely occurring between 2000 and 2004 (again, with other short-term shifts). For Japan, the shift 
to a negative correlation is longer lasting. Here, the correlation switched to negative in mid-1992 and only presents weaker evidence of 
Table 3 
Returns and Correlations over Different Economic Regimes.
Positive Industrial Production Growth Negative Industrial Production Growth
Stock Return Bond Return Correlation Stock Return Bond Return Correlation
Canada 0.646 0.141 − 0.034 − 0.001 − 0.035 − 0.192
France 0.877 0.145 0.084 − 0.046 0.195 − 0.031
Germany 0.566 0.154 − 0.149 − 0.003 0.129 − 0.089
Italy 0.513 − 0.133 0.282 − 0.049 0.524 0.297
Japan 0.275 0.083 − 0.034 0.198 0.198 − 0.070
UK 0.555 0.114 0.171 0.526 0.236 0.137
US 0.821 − 0.025 0.038 0.545 0.293 − 0.085
Positive Change in Inflation Negative Change in Inflation
Canada 0.958 − 0.045 0.052 0.212 0.274 − 0.033
France 0.859 0.020 0.039 0.223 0.300 0.028
Germany 0.791 − 0.046 − 0.034 0.170 0.172 0.003
Italy 0.330 − 0.050 0.310 0.155 0.416 0.255
Japan 0.576 0.151 − 0.056 − 0.142 0.105 − 0.056
UK 0.849 − 0.130 0.259 − 0.102 0.364 0.023
US 1.129 − 0.284 0.083 0.415 0.341 − 0.048
Notes: Entries are the mean values for stock and bond returns and the correlation between them over sub-periods defined according to positive and 
negative output (industrial production) growth and positive and negative changes in inflation.
Fig. 2. Time-Varying Correlations. Note: Graphs depict the stock–bond return correlation for each country estimated using a DCC-GARCH model 
and a three-year rolling window.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
6
a return to a positive correlation in 2023. The correlation statistics in Table 4, again show that the correlation switches between 
negative and positive as evidenced by the minimum and maximum values. They also reveal that the variability (standard deviation) of 
the correlation series is greater with the rolling correlations. In a practical sense, this implies a switch in the behaviour of bonds from 
being an asset that helps diversify a stock position to one that hedges stocks.
4. Explaining Time-Varying correlations.
While observing time-variation within correlations is important, especially for investors engaged in portfolio construction and 
management. It is equally (or more) important in seeking to explain the time-variation. As discussed above, there are two broad 
approaches for such time-variation, linked to inflation and output growth respectively, while it is also noted that interest rates and the 
nature of the linkage between output growth and inflation are potential explanatory variables. Thus, we estimate a regression for the 
time-varying correlation against inflation and inflation volatility, growth and growth volatility (where the volatility series capture 
uncertainty), real interest rates and the correlation between inflation and growth. We consider the regression for each market and for 
both DCC-GARCH and rolling correlations. Inflation and output growth volatility are equivalently estimated with a GARCH and rolling 
standard deviation approach. The regression is given by equation (1), and the results are reported in Table 5.
ρsb,t = α0 + Σi βi xi,t-1 + εt(1)
Where ρsb,t refers to the correlation between stock and bond returns for time period t, xi,t-1 are the noted explanatory variables and εt 
is a random error term. As noted, for each market inflation is given by the change (log difference) in the consumer price index, output 
growth is change in industrial production and the real interest rate is the difference between 10-year Treasury yields and inflation. The 
data is obtained from LSEG DataStream and again, there are some differences in the sample periods.7
From Table 5, we can see that inflation typically has a positive effect on the correlation where it is statistically significant. This 
includes for Germany (at the 10 % level), Japan, the UK and US for the DCC-GARCH correlation series and Canada, Germany, Japan, 
the UK and US for the rolling correlation series. The one exception is for the rolling correlation for Italy, where a negative and 10 % 
significant relation with inflation is noted. Inflation volatility also exhibits a positive relation where it is significant, with greater 
significance for the DCC-GARCH correlation series (France, Germany, Italy, Japan, the UK and US, including at the 10 % level) than for 
the rolling correlation (France and Italy). Output growth equally has a positive relation, including for Canada (DCC-GARCH) and 
France, Italy and the US (rolling). For output growth volatility there is evidence of both a positive relation (France, Italy and Japan 
across the two correlation measures) and a negative relation (Canada, the UK and US with the DCC-GARCH). Real interest rates have 
the greatest effect across the different markets. For the DCC-GARCH regression, there is a positive and significant relation across all 
markets except Canada and Germany, while for the rolling correlation regression, it is significant for all markets. In contrast, for the 
inflation-growth correlation, this is not significant for the DCC-GARCH correlation regressions and is only significant for two markets 
(France and the US, plus another two at the 10 % level, Canada and Germany) with a negative coefficient for the rolling correlation 
regression.
We can consider these results in the context of the discussion in Section 2. A simple description is also presented in Brixton et al. 
(2023). Here, there is an expectation that inflation is associated with a positive correlation as it should have the same impact on asset 
prices (higher inflation leads to lower expected cash flows), while output growth leads to a negative correlation (as an expanding 
Table 4 
Stock-Bond Return Correlation Summary Statistics.
Series Mean Std Dev Min Max Skew Kurt JB
DCC-GARCH Estimated Correlations
Canada − 0.014 0.160 − 0.440 0.442 0.161 2.800 0.25
France 0.077 0.246 − 0.622 0.697 − 0.156 2.640 0.11
Germany − 0.002 0.242 − 0.605 0.553 − 0.148 2.331 0.00
Italy 0.221 0.185 − 0.209 0.615 − 0.012 2.219 0.00
Japan − 0.162 0.263 − 0.662 0.718 0.896 3.565 0.00
UK 0.107 0.314 − 0.635 0.768 − 0.033 2.189 0.00
US − 0.019 0.269 − 0.622 0.539 − 0.044 2.079 0.00
Rolling Window Estimated Correlations
Canada 0.018 0.329 − 0.688 0.671 0.329 2.196 0.00
France 0.081 0.390 − 0.539 0.703 0.150 1.679 0.00
Germany 0.009 0.376 − 0.666 0.699 − 0.005 1.713 0.00
Italy 0.225 0.300 − 0.386 0.735 − 0.258 2.007 0.00
Japan − 0.142 0.367 − 0.684 0.889 0.776 2.472 0.00
UK 0.107 0.360 − 0.624 0.787 0.227 2.079 0.00
US − 0.014 0.387 − 0.789 0.648 − 0.024 1.848 0.00
Notes: The entries are the mean, standard deviation, minimum, maximum, skewness, kurtosis and Jarque-Bera p-values for the estimated timevarying stock and bond return correlations estimated over the sample period noted in Table 1. The rolling windows are based on a three-year period.
7 Due to data availability, the regression for Canada begins in 1998, France and Italy in 1991, Germany in 1992, Japan in 1986, the UK in 1989, 
and US in 1980.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
7
economy supports higher stock prices and a move towards risky assets, conversely falling output leads to a flight-to-safety effect and a 
move into bonds). However, as noted, the opposite relations are possible. The results here, are generally supportive of inflation leading 
to a positive correlation, as do real interest rates, with both variables having similar impacts on expected future asset values (i.e., 
higher inflation and interest rates are expected to depress both stock and bond prices). The effect of output is also largely positive, in 
Table 5 
Stock-Bond Return Correlation Regressions.
DCC-GARCH Correlation
Inflation Infl. Vol. Output Output Vol. Real I.R. Corr N.-R.
Canada − 0.004 
(− 0.14)
− 0.661 
(− 0.02)
0.009 
(2.42)
− 0.041 
(− 3.42)
0.007 
(0.62)
− 0.031 
(− 0.24)
France 0.038 
(0.49)
1.139 
(2.48)
0.006 
(1.62)
0.013 
(2.02)
0.036 
(4.02)
− 0.023 
(− 0.28)
Germany 0.081 
(1.66)
0.589 
(2.85)
0.004 
(0.67)
0.008 
(0.43)
0.014 
(1.50)
− 0.043 
(− 0.35)
Italy − 0.019 
(− 0.47)
0.537 
(5.33)
0.001 
(− 0.19)
0.005 
(2.38)
0.046 
(9.80)
− 0.007 
(− 0.12)
Japan 0.164 
(2.65)
0.439 
(1.87)
0.005 
(0.97)
0.013 
(0.66)
0.047 
(3.14)
0.138 
(1.06)
UK 0.108 
(2.30)
0.844 
(3.83)
0.009 
(1.27)
− 0.052 
(− 2.92)
0.060 
(5.55)
0.007 
(0.08)
US 0.157 
(3.86)
0.209 
(1.85)
0.009 
(1.12)
− 0.048 
(− 2.37)
0.055 
(5.89)
− 0.064 
(− 1.03)
Rolling Window Correlation
Canada 0.091 
(4.50)
− 0.266 
(− 0.82)
0.005 
(1.09)
0.019 
(1.27)
0.088 
(6.59)
− 0.072 
(− 1.95)
France 0.021 
(0.59)
1.511 
(1.91)
0.011 
(1.69)
0.031 
(3.09)
0.077 
(4.74)
− 0.131 
(− 1.98)
Germany 0.085 
(3.09)
0.460 
(1.64)
− 0.002 
(− 0.27)
0.015 
(0.66)
0.063 
(3.99)
− 0.091 
(− 1.68)
Italy − 0.035 
(− 1.89)
1.402 
(4.28)
0.008 
(2.52)
0.005 
(1.34)
0;084 
(7.50)
− 0.005 
(− 0.11)
Japan 0.185 
(10.37)
− 0.157 
(− 1.15)
− 0.003 
(− 0.10)
0.093 
(3.94)
0.111 
(7.49)
− 0.030 
(− 0.80)
UK 0.082 
(3.79)
− 0.192 
(− 0.64)
0.010 
(1.63)
0.001 
(0.04)
0.075 
(5.10)
− 0.023 
(− 0.44)
US 0.053 
(4.29)
− 0.184 
(− 1.27)
0.009 
(1.76)
0.010 
(0.60)
0.095 
(11.81)
− 0.083 
(− 2.84)
Notes: Entries are the estimated coefficients (Newey-West t-statistics) for equation (1). Inflation is the change in CPI and output is the change in 
industrial production. The volatility measures are obtained either by a GARCH(1,1) model or a rolling window to match the correlation series. Real 
interest rates are the 10-year Treasury yield minus inflation. The nominal-real correlation is between inflation and output growth and obtained by a 
DCC-GARCH or rolling window approach accordingly. The sample periods vary with the availability of the macroeconomic data. They start in 1980 
for Japan and the US, 1988 for the UK, 1990 for France, 1991 for Germany and Italy, and 1998 for Canada.
Table 6 
Bai-Perron Breakpoint Tests.
DCC-GARCH Correlation
# of Breaks Break Dates
Canada 2 2007:06 2013:07
France 3 1998:09 2004:03 2013:07
Germany 3 1998: 09 2004:04 2013:07
Italy 4 1998:09 2004:06 2010:06 2019:01
Japan 4 1992:07 1998:08 2004:05 2016:02
UK 3 1998:08 2004:06 2013:07
US 4 1990:05 1998:09 2007:06 2014:09
Rolling Window Correlation
Canada 2 2005:05 2014:09
France 3 1998:09 2005:09 2015:05
Germany 4 1998:08 2003:07 2008:06 2015:05
Italy 4 1999:12 2005:10 2010:12 2016:04
Japan 3 1993:09 2003:08 2016:05
UK 3 1998:08 2008:12 2015:05
US 4 1990:10 1998:08 2008:10 2015:05
Notes: Entries are the number of breaks and dates reported using the Bai and Perron (1998, 2003a,b) breakpoint methodology. The breaks are 
determined using the Bai-Perron methodology on the regression in equation (1), see Table 5 for further notes.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
8
contrast to the suggestion within the theoretical literature. This implies that both asset prices rise with growth and is more indictive of 
the view that investors increase demand for all assets with rising output, consistent with diversification and portfolio theory.
Time-Varying Explanatory Regression
One question that remains open is whether the factors that affect the time-varying correlation remain constant themselves. This is 
especially the case given notable changes in economic risk that occur over the sample period. As discussed by Boon et al. (2020) and 
Campbell et al. (2020), among others, this includes a change in the nature of the inflation and growth correlation, as well as periods of 
subdued inflation and low (and negative) real interest rates. To consider this question, equation (1) is reconsidered using the Bai and 
Perron (1998, 2003a,b) breakpoint testing procedure to examine whether there are breaks in the coefficient values.
The results of the breakpoint tests are presented in Table 6 and indicate that there are a number of breaks within the correlation 
regression for each market. The number and timing of the breaks are broadly consistent across the correlation regressions based on the 
DCC-GARCH and rolling correlation series. Across each of the seven markets, we see three broadly common breaks. This includes a 
break during 1998 or 1999, which is consistent with the dotcom bubble period. In addition, there is a break around the mid-2000s, 
which is just prior to the financial crisis that began in 2007. There is also a common break in the mid-2010s, which occurs around 
the time associated with a number of crisis periods, including US and European debt crises. There are also some breaks associated with 
individual countries, this arises in the early 1990s for those markets with sufficiently historical data (Japan and the US), while both 
Germany and Italy exhibit an additional break associated with the financial crisis and its aftermaths.
Table 7 presents the correlation regressions incorporating breaks.8 Both Tables 6 and 7 seek to group the breaks (Table 6) and 
coefficients (Table 7) around their common dates, although this is not exact. The results in Table 7 show that the variables that affect 
the stock–bond return correlation change over time, both in terms of coefficient sign and statistical significance for each market. We 
can also see that in terms of significant variables across the different decades, these differ across markets within the same time period. 
For example, if we take the US, inflation and output volatility have a positive effect on correlation during the 1980s, only output 
volatility is significant for most of the 1990s, only inflation volatility for the early 2000s, and neither being significant in the postfinancial crisis period. As another example, if we consider real interest rates, from the late 1990s/early 2000s, this is negative and 
significant for Japan and positive and significant for the remaining markets, while in the first half of the 2010s, it negative and sig
nificant for Germany, but positive and significant elsewhere. This implies the potential for diversification benefits when considering 
portfolios across international markets.
Across the full set of results, we can try to draw some general conclusions. Real interest rates is the variable that exhibits the most 
significance across the markets and time periods, as well as the most consistent estimates, although as noted, with some variation 
across markets. Notably, from the late 1990s/early 2000s, real interest rates are predominantly positive and significant. In the earlier 
part of the sample, however, this is not the case. For the macroeconomic variables of inflation and output, this tends towards a mixed 
picture over the different markets and time periods. As with real interest rates, there is greater evidence of significance from the late 
1990s/early 2000s onwards. Moreover, this becomes increasingly predominantly positive for inflation and inflation volatility, 
although the same is not true for output and output volatility.9 Likewise, the nominal-real correlation remains mixed in terms of 
significance and sign across the markets and time.
In sum, these results support the view that real interest rates and inflation will typically impart a positive effect on the stock and 
bond return correlation, although there are some country-specific differences. For output growth, a positive relation is also generally 
observed but there is greater evidence of a negative relation, suggesting a more mixed picture compared to inflation and interest rates.
5. Implications
In examining the implications of the above results, we consider several aspects from an investor perspective of the changing 
correlation behaviour. Fig. 3 presents the cumulative return to an investment that is equally weighted in stock and bonds, although the 
weights used is not specifically relevant to the nature of this exercise. Evident within Fig. 3 is the changing nature of the trend path for 
cumulative returns over the sample period and the switch in the stock and bond correlation from positive to negative observed in Fig. 2. 
This is most cleanly seen in the graphs for Canada, France, Germany, the UK and US. Here, there is an evident shallowing of the 
cumulative trend around the year 2000. This is consistent with the switch in correlation from positive to negative, such that bonds 
change from being a diversifier to a hedger and so detract from any positive stock return performance. The pattern for Italy and Japan 
appears different, given the different correlation behaviour. For Japan, we do see a steeper cumulate returns trend when the corre
lation is positive, however, this is just for the beginning of the sample, prior to the mid-1990s. For Italy, the correlation remains 
positive through the sample period, with the exception of a short period in the 2000s. This period is associated with a fall in cumulative 
returns, although it is noted (e.g., Table 1) that Italian stock return performance is weaker than for the other markets.
To provide an illustration of the effect of the switch in the correlation for portfolio performance, Fig. 4 provides a simple trend 
analysis for the US and the portfolio weights required to maintain this trend. The top figure again plots the cumulative 50/50 portfolio 
over the full sample period, while a trend term is estimated for this portfolio from the start of the sample until the end of 1999. This 
trend is then extrapolated (forecast) over the remainder of the sample. As can be seen, the path of the realised portfolio deviates 
notably below this extrapolated trend, highlighting the effect the change in the correlation has resulted in. The lower panel repeats the 
cumulative 50/50 portfolio and trend but also shows the alternative portfolio weights required to maintain the trend path. Evident 
8 These results are for the rolling correlations, with those for the DCC-GARCH available upon request. 9 Although output growth tends to be more positive between the late 1990s/early 2000s and the mid 2010s, and more mixed thereafter.
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
9
Table 7 
Breakpoint Stock-Bond Return Correlation Regressions.
Canada France Germany Italy Japan UK US
Sample 1: Covering 1980s-Early 1990s
1986:01–1993:08 1980:04- 
1990:09
Inflation 0.020 
(0.86)
− 0.015 (− 1.37)
Infl. Vol. − 0.161 
(− 0.90)
0.356 (2.56)
Output − 0.011 
(− 3.90)
0.005 (0.78)
Output Vol. − 0.169 
(− 2.50)
0.158 (2.23)
Real I.R. − 0.003 
(− 0.11)
0.049 (3.53)
Corr N.-R. − 0.005 
(− 0.16)
0.026 (0.60)
Sample 2: Covering Early 1990s-Late 1990s
1991:01–1998:08 1992:01–1998:07 1991:08–1999:11 1989:01–1998:07 1990:10–1998:07
Inflation 0.023 
(0.91)
0.014 (0.66)
0.060 (2.86)
− 0.155 (− 5.02)
0.044 (1.20)
Infl. Vol. − 0.320 
(− 1.10)
0.007 (0.04)
− 1.178 (− 2.43)
0.323 (1.49)
0.269 (0.94)
Output 0.002 
(0.60)
− 0.007 (− 2.12)
0.010 (4.52)
− 0.046 (− 3.82)
0.003 (0.33)
Output Vol. 0.127 
(0.10)
− 0.063 (− 1.92)
− 0.012 (− 0.50)
− 0.140 (− 3.38)
0.246 (2.95)
Real I.R. − 0.002 
(− 0.22)
0.010 (0.35)
0.034 (4.79)
− 0.051 (− 1.26)
0.037 (0.85)
Corr N.-R. 0.058 
(3.18)
− 0.002 (− 0.04)
− 0.093 (− 5.45)
− 0.152 (− 2.92)
− 0.006 (− 0.26)
Sample 3: Covering Late 1990s-Early/Mid 2000s
1998:01–2005:04 1998:09–2005:08 1998:09–2003:06 1999:12–2005:09 1993:09–2003:07
Inflation 0.124 
(3.09)
− 0.083 (− 2.47)
− 0.004 (− 0.06)
0.063 (1.05)
− 0.112 (− 6.25)
Infl. Vol. − 0.354 
(− 0.85)
− 0.467 (− 0.92)
1.338 (4.43)
2.88 (2.61)
− 0.051 (− 0.42)
Output 0.010 
(1.71)
− 0.005 (− 0.40)
0.003 (0.05)
0.007 (0.78)
0.005 (1.05)
Output Vol. 0.017 
(0.44)
− 0.560 (− 0.49)
− 0.050 (− 1.46)
− 0.013 (− 0.42)
0.331 (3.94)
Real I.R. 0.210 
(5.23)
0.150 (4.25)
0.120 (2.18)
0.147 (5.90)
− 0.063 (− 3.46)
Corr N.-R. − 0.106 
(− 2.76)
0.014 (0.50)
− 0.153 (− 3.76)
− 0.003 (− 0.10)
0.010 (0.40)
Sample 4: Covering Early/Mid 2000s-Late 2000s
2005:05–2014:08 2005:09–2015:04 2003:07–2008:05 2005:6–2010:11 1998:08–2008:11 1998:08–2008:09
Inflation 0.292 
(12.74)
− 0.027 (− 1.26)
0.016 (0.61)
− 0.118 (− 2.46)
0.133 (1.60)
0.094 (4.92)
Infl. Vol. 0.701 
(2.42)
0.724 (2.03)
− 0.609 (− 2.16)
− 0.483 (− 0.79)
0.237 (0.40)
0.521 (6.18)
(continued on next page)
D.G. McMillan Journal of International Financial Markets, Institutions & Money 106 (2026) 102242
10
Table 7 (continued )
Output 0.003 
(1.26)
0.012 (3.81)
0.033 (3.59)
0.002 (1.05)
0.022 (3.30)
0.006 (1.20)
Output Vol. 0.089 
(2.36)
0.402 (0.26)
− 0.077 (− 1.91)
0.024 (1.71)
0.025 (1.48)
− 0.023 (− 0.29)
Real I.R. 0.271 
(13.42)
0.067 (3.67)
0.101 (3.52)
− 0.043 (− 1.43)
0.143 (2.30)
0.148 (13.06)
Corr N.-R. 0.081 
(4.17)
− 0.035 (− 1.36)
− 0.073 (− 1.32)
− 0.073 (− 1.88)
− 0.044 (− 1.35)
− 0.088 (− 4.15)
Sample 5: Covering Late 2000s-Mid 2010s
2009:06–2015:04 2010:11–2016:03 2003:08–2016:04 2008:12–2015:04 2008:10–2015:04
Inflation 0.043 
(1.59)
− 0.084 (− 6.00)
− 0.047 (− 0.85)
0.111 (3.23)
0.176 (3.67)
Infl. Vol. 0.918 
(3.00)
0.113 (0.60)
− 0.181 (− 1.19)
0.851 (1.41)
0.095 (1.07)
Output 0.009 
(6.10)
− 0.015 (− 6.63)
− 0.001 (− 0.02)
− 0.011 (− 1.13)
− 0.022 (− 3.06)
Output Vol. 0.023 
(1.22)
− 0.011 (− 0.52)
0.022 (1.33)
− 0.042 (− 1.95)
− 0.071 (− 1.45)
Real I.R. 0.032 
(1.77)
− 0.029 (− 2.09)
− 0.073 (1.67)
0.149 (5.12)
0.161 (3.77)
Corr N.-R. 0.054 
(3.22)
− 0.007 (− 0.35)
− 0.006 (− 1.22)
− 0.076 (− 1.62)
− 0.157 (− 2.89)
Sample 6: Covering Mid 2010s-Early/Mid 2020s
2014:09–2023:12 2015:05–2023:12 2015:05–2023:12 2016:04–2023:12 2016:05–2023:12 2015:05–2023:12 2015:05–2023:12
Inflation 0.153 
(7.27)
0.064 (5.02)
0.166 (7.94)
− 0.032 (− 5.31)
0.656 (5.40)
0.173 (8.22)
0.187 (5.88)
Infl. Vol. − 0.295 
(− 0.90)
0.705 (2.31)
− 0.025 (− 0.15)
0.159 (2.86)
0.034 (0.17)
− 1.055 (− 4.92)
0.026 (0.22)
Output − 0.011 
(− 2.33)
− 0.001 (− 0.14)
0.001 (0.42)
0.001 (0.09)
0.002 (0.71)
0.003 (0.73)
− 0.011 (− 1.86)
Output Vol. − 0.017 
(1.51)
0.177 (0.80)
− 0.002 (− 0.30)
0.001 (1.26)
0.194 (7.34)
− 0.001 (− 0.17)
− 0.018 (− 1.57)
Real I.R. 0.193 
(6.94)
0.126 (8.65)
0.194 (9.68)
− 0.012 (− 1.54)
0.553 (4.33)
0.136 (7.20)
0.206 (8.09)
Corr N.-R. − 0.081 
(− 2.54)
− 0.021 (− 0.88)
0.028 (0.79)
0.020 (1.18)
− 0.009 (− 0.20)
0.083 (2.50)
− 0.122 (− 2.26)
Notes: Entries are the estimated coefficients (Newey-West t-statistics) for equation (1) allowing for Bai-Perron breakpoints. The correlations are obtained using the rolling window approach. Inflation is the change in CPI and output is the change in industrial production. The volatility measures are obtained using a rolling window to match the correlation series. Real interest rates are the 10-year Treasury yield minus inflation. The nominal-real correlation is between inflation and output growth and obtained by a rolling window approach. The results are grouped by approximate s