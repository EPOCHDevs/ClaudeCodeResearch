---
url: https://pure.eur.nl/ws/portalfiles/portal/189207773/Empirical_Evidence_on_the_Stock_Bond_Correlation.pdf
title: Empirical_Evidence_on_the_Stock_Bond_Correlation.p
domain: misc
crawled_at: 2026-02-04T08:03:01.858114+00:00
source: exa_search
author: 
chart_count: 0
image_links:
outbound_links:
---

EUR Research Information Portal
Empirical evidence on the stock-bond correlation
Published in:
Financial Analysts Journal
Publication status and date:
Published: 01/01/2024
DOI (link to publisher):
10.1080/0015198X.2024.2317333
Document Version
Publisher's PDF, also known as Version of record
Document License/Available under:
CC BY
Citation for the published version (APA):
Molenaar, R., Senechal, E., Swinkels, L., & Wang, Z. (2024). Empirical evidence on the stock-bond correlation. Financial
Analysts Journal, 80(3), 17-36. https://doi.org/10.1080/0015198X.2024.2317333
Link to publication on the EUR Research Information Portal
Terms and Conditions of Use
Except as permitted by the applicable copyright law, you may not reproduce or make this material available to any third party
without the prior written permission from the copyright holder(s). Copyright law allows the following uses of this material
without prior permission:
 • you may download, save and print a copy of this material for your personal use only;
 • you may share the EUR portal link to this material.
In case the material is published with an open access license (e.g. a Creative Commons (CC) license), other uses may be
allowed. Please check the terms and conditions of the specific license.
Take-down policy
If you believe that this material infringes your copyright and/or any other intellectual property rights, you may request its
removal by contacting us at the following email address: openaccess.library@eur.nl. Please provide us with all the relevant
information, including the reasons why you believe any of your rights have been infringed. In case of a legitimate complaint,
we will make the material inaccessible and/or remove it from the website.
Financial Analysts Journal
ISSN: (Print) (Online) Journal homepage: www.tandfonline.com/journals/ufaj20
Empirical Evidence on the Stock–Bond Correlation
Roderick Molenaar, Edouard Sénéchal, Laurens Swinkels & Zhenping Wang
To cite this article: Roderick Molenaar, Edouard Sénéchal, Laurens Swinkels & Zhenping Wang
(2024) Empirical Evidence on the Stock–Bond Correlation, Financial Analysts Journal, 80:3,
17-36, DOI: 10.1080/0015198X.2024.2317333
To link to this article: https://doi.org/10.1080/0015198X.2024.2317333
© 2024 The Author(s). Published with
license by Taylor & Francis Group, LLC.
View supplementary material
Published online: 21 Mar 2024.
Submit your article to this journal 
Article views: 9930
View related articles
View Crossmark data
Citing articles: 2 View citing articles
Full Terms & Conditions of access and use can be found at
https://www.tandfonline.com/action/journalInformation?journalCode=ufaj20
Empirical Evidence on the
Stock–Bond Correlation
Roderick Molenaar, Edouard Sen echal, CFA, Laurens Swinkels  , and
Zhenping Wang
Roderick Molenaar is a senior researcher with Robeco, Rotterdam, the Netherlands. Edouard Sen echal is a senior portfolio manager with 
the State of Wisconsin Investment Board, Madison, Wisconsin. Laurens Swinkels is a senior researcher with Robeco, Rotterdam, the
Netherlands, and an associate professor of finance at Erasmus University, Rotterdam, the Netherlands. Zhenping Wang is senior analyst
with the State of Wisconsin Investment Board, Madison, Wisconsin. Send correspondence to Laurens Swinkels at lswinkels@ese.eur.nl.
The correlation between stock and
bond returns is a cornerstone of
asset allocation decisions. History
reveals abrupt regime shifts in correlation after long periods of relative
stability. We investigate the drivers
of the correlation between stocks
and bonds and find that inflation,
real rates, and government creditworthiness are important explanatory variables. We examine the
implications of a shift in the stock–
bond correlation and find that
increases are associated with higher
multi-asset portfolio risk and higher
bond risk premia.
Keywords: bonds; correlation; inflation;
interest rates; stocks
Disclosure: No potential conflict of interest
was reported by the author(s).
PL Credits: 2.0
Introduction
T
he correlation between stocks and bonds is an essential driver of
any asset allocation decision. It impacts not only the overall risk of a
diversified multi-asset class portfolio but also the risk premia one
should expect to receive for taking risk in different asset classes. The
obstacle one faces when estimating the correlation between stocks and
bonds is that it fluctuates extensively across periods. Volatility of asset
classes can vary widely inside of a business cycle but remain relatively
stable over longer horizons. Correlations between stocks and bonds may
persist with the same sign for extended periods, before eventually reversing. For example, the average correlation between stocks and bonds was
0.35 in the United States between 1970 and 1999 and then was −0.29
between 2000 and 2023. The effect of these variations can be seen in
Figure 1. Keeping equity and bond mean returns and volatilities constant
at the full sample values, the figure shows that the correlation in the first
three decades leads to a volatility of 10.5% per annum for the 60/40
portfolio, whereas this decreases to 8.4% with the correlation realized in
the post-1999 period.
In times when allocations to government bonds reduce overall portfolio
risk, it would make sense that the expected returns on bonds are low or
even negative. Investors may be prepared to pay for (imperfect) insurance against equity market downturns. In other words, the bond risk premium (also sometimes called the term premium), that is, the additional
return that investors are expected to earn from investing in Treasury
Research
We would like to thank Lieven Baele, Derek Bloom, Stefano Cavaglia, Edwin Denson,
Johan Duyvesteyn, Bob Galesloot, Leo Kropywiansky, and Pim van Vliet for valuable
discussions. The views expressed in this paper do not necessarily reflect those of the
State of Wisconsin Investment Board or Robeco.
This is an Open Access article distributed under the terms of the Creative Commons
Attribution License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work
is properly cited. The terms on which this article has been published allow the posting
of the Accepted Manuscript in a repository by the author(s) or with their consent.
Volume 80, Number 3 © 2024 The Author(s). Published with license by Taylor & Francis Group, LLC. 17
Financial Analysts Journal | A Publication of CFA Institute
https://doi.org/10.1080/0015198X.2024.2317333
bonds rather than Treasury bills, may become negative
in times when the stock–bond correlation is negative.
Today’s market participants have little experience,
perhaps except for the last two years, investing in an
environment where the correlation between stocks
and bonds is positive. Given that a shift in level or
even the sign of the correlation between stocks and
bonds can last for decades, short historical data periods (i.e., 10 or even 20 years) are of little help to
understand the drivers of co-movements between
stocks and bonds. To resolve this, our analyses use
multiple decades of historical data across multiple
countries. Figure 2 contains the time series of correlations for the United States using data starting in
1875. Researchers have several choices on how to
calculate the stock–bond correlation. The effects of
some of these choices are described with more detail
in Online Appendix A, where we argue that using the
Spearman rank correlation instead of the conventional Pearson correlation helps to obtain a more
robust estimate of the stock–bond correlation. Figure
2 shows that the stock–bond correlation tends to be
positive or close to zero. Exceptions with a correlation below −0.2 occur in the early 1930s, in the late
1950s, and during most of the 2000s.1
The main question that we aim to answer is whether
we can better understand what characterizes periods
in which the stock–bond correlation is above or, alternatively, below zero and how this affects multi-asset
portfolio risk and the bond risk premium. This means
that our goal is to explain stock–bond correlations with
economically motivated variables. This also means that
we leave forecasting the stock–bond correlation for
future research. We start by formulating theoretical
drivers of the stock–bond correlation, estimate these
using our historical dataset, and link these to the prevailing monetary and macroeconomic environment.
Additional empirical evidence from other countries
complements our insights from U.S. financial markets.
Our findings can be summarized as follows. First, we
observe that the stock–bond correlation varies
Figure 1. Multi-Asset Portfolio Risk and Return for Different Stock–Bond Correlation
Notes: Authors’ average standard deviation and excess returns from January 1970 to June 2023. Pearson correlation coefficient of
monthly returns computed between January 1970 and December 1999 and between January 2000 and June 2023.
Financial Analysts Journal | A Publication of CFA Institute
18
considerably over time, both in magnitude and sign.
Second, before 1951, real risk-free rates and inflation
had no discernable impact on the stock–bond correlation.2 After 1951, as central banks started to adopt
countercyclical monetary policies, we find remarkably
similar patterns across developed markets: the stock–
bond correlation tends to be high during periods
when inflation and real risk-free rates are high. This
relation tends to be absent in countries where government bonds have a lower credit rating. Third, we
find that the sign and magnitude of the stock–bond
correlation play a significant role to estimate portfolio
risk. Moreover, bond risk premia are positively
related to estimates of the stock–bond correlation, as
is implied by the capital asset pricing model (CAPM).
Our contribution is threefold. First, we provide longrun empirical evidence on the economic drivers of the
correlation between stocks and bonds in three major
developed markets.3 Second, we examine the impact
of the credit quality of government bond markets on
the stock–bond correlation and its drivers, which as far
as we know has not been explored in the literature.
Third, our results extend the work of Ilmanen (2003)
and confirm the existence of a positive relation
between stock–bond correlation and risk premia.
Theoretical Drivers of the Stock–
Bond Correlation
We can derive the drivers of the stock–bond correlation by modeling the returns using factors that affect
their valuations.4 We assume that government bond
yields (y) contain three components: the expected
short real interest rate (rr) and inflation (p) until
maturity of the bond and the bond risk premium (brp)
for holding bonds instead of short-term Treasury
bills.5 Since the current bond yield is known, the
unexpected part of the bond return comes from
changes in the three components:
r
b
tþ1  ab − bb
rrDtþ1rr − bbpDtþ1p − bbbrpDtþ1brp (1)
We expect that each of the b-s in Equation (1) are
positive.
We assume that equity yields contain four components: the expected short real interest rate (rr) and
inflation (p) over the life of the stock, the expected
growth rate of dividends (g), and the equity risk premium (erp).6 Since the current dividend (or earnings)
yield is known, the unexpected part of the equity
return comes from changes in the four components:
Figure 2. Stock–Bond Correlation for the United States
Notes: Spearman rank correlation based on monthly returns for the U.S. equity market and government bonds with 10-year maturity. Rolling window estimation using 36 monthly observations over the period January 1875 to June 2023.
Source: Authors, Global Financial Data.
Empirical Evidence on the Stock–Bond Correlation
Volume 80, Number 3 19
r
e
tþ1  ae − be
rrDtþ1rr − bepDtþ1p − beerpDtþ1erp þ begDtþ1g
(2)
We again expect that each of the b-s are positive.
This leads to the following covariance between stock
and bond returns:
cov rb
tþ1,r
e
tþ1
n o ¼ bb
rrberrr2
rr þ bb
pbepr2
p þ bb
rrbep þ bbpberr  rrr, p þ ...
... þ bb
rrbeerprrr, erp − bbrrbegrrr, g þ bbpbeerprp, erp − bbpbegrp, g þ ...
... þ bb
brpberrrbrp, rr þ bbbrpbeprbrp, p þ bbbrpbeerprbrp, erp − bbbrpbegrbrp, g:
(3)
This formula indicates that the volatility of real interest
rate changes and inflation changes should have a positive effect on the stock–bond correlation. For each of
the other nine components, the effect depends on the
sign of the covariance of the cross-terms. Since we
expect all betas to be positive, the coefficients of the
decomposition are also positive, except for those related
to the expected growth rate of cash flows. Correlation
is effectively a volatility-scaled covariance, so any driver
of correlation will have the same directional impact on
covariance; see Brixton et al. (2023). We give economic
intuition for the components of Equation (3).
First, a higher variance of real interest rates should
also generate a higher correlation in bonds and
equity prices, as higher (lower) real interest rates lead
to lower (high) values of future cash flows of both
stocks and bonds, all other things equal. More variability in real interest rates then leads to equity and
bond returns in the same direction.
Second, ceteris paribus, a higher variance of changes
in expected inflation should generate larger co-movements in bonds and equity prices. This is consistent
with Brixton et al. (2023). However, the inflation level,
the time-series variance of inflation, and forward-looking uncertainty around future inflation are positively
related, which may make it empirically difficult to disentangle. Friedman (1977) states that higher inflation
is accompanied by higher policy uncertainty. High
inflation often leads to countercyclical monetary policy, inducing abrupt changes in economic policies or
even political unrest, and thus wide uncertainty
regarding future inflation. Ball (1992) presents a model
where expected inflation is more uncertain when it is
high. When inflation is around the central bank’s
ambition level, it is expected to be stable. However,
when inflation is high, it is hard to predict how and
how fast the central bank will react. The central bank
wants to curb inflation but will be reluctant to create
deflation given the concern of recession. The positive
relation between the level and variability is known as
the Friedman–Ball hypothesis.7 Note that forwardlooking uncertainty can also be high when short-term
realized volatility is low. David and Veronesi (2016)
find that inflation uncertainty, measured by the dispersion of survey forecasts, contains different information
from the realized inflation time-series volatility.
Finally, we have a series of cross-terms that affect the
stock–bond correlation. Since real interest rates and
inflation are the only variables that affect both stock
and bond prices, there is no variance term for the
other variables. For example, there is no variance term
of economic growth. Instead, the sign of the covariance of economic growth with inflation and real rates
determines its effect on the correlation between
stocks and bonds. Stock returns are expected to
increase with economic growth through the corporate
earnings channel, but the relation of economic growth
with inflation and real rates is not a priori clear, see,
for example, Cukierman et al. (1993). On the other
hand, bond returns are in the short run negatively correlated with economic growth; see Ilmanen (2011).
Well-documented episodes of stagflation during the
1970s illustrate this point. Similarly, divergences in the
risk premia of bonds and equities should reduce the
correlation between stocks and bonds. Episodes of
divergence between bond and equity risk premia have
been more common in the years since 2000. During
episodes of increased risk aversion (i.e., 2000, 2008,
2020) bond risk premia compress while equity risk premia expand. Such a relation depends on bonds being
considered as “safe haven” assets. However, the
assumption that sovereign bonds are “safe haven”
assets is not always correct. Campbell, Pflueger, and
Viceira (2020) develop a model where bonds can
switch from safe to risky assets. If the correlation
between inflation and output gap is negative, then
bonds become risky assets and are positively correlated with equities. On the other hand, if inflation is
positively correlated with the output gap, then bonds
are a safe asset and negatively correlated with equities. David and Veronesi (2016) highlight the importance of the macroeconomic environment to
understand the impact of inflation on the correlation
between stocks and bonds. In low-inflation environments, an increase in inflation has a small negative
impact on the pricing of bonds but is good news for
equity markets, as it signals higher growth and lower
equity risk premia. Baele and Van Holle (2017) emphasize the importance of monetary policy during lowinflation environments. In high-inflation environments,
the correlation between stocks and bonds is always
positive. When inflation is low, it is the conjunction of
Financial Analysts Journal | A Publication of CFA Institute
20
low inflation and loose monetary policy that creates a
negative correlation between stocks and bonds.
The Appendix contains details of our data sources.
Here, we give a broad overview of our choice of
data series for each of the theoretical factors that we
distinguish. For bonds, we use Adrian, Crump, and
Moench (2013) for the bond risk premium, the average of the past 10-year inflation as the inflation forecast, and the observed government bond yields to
obtain the expected short-term real interest rates.
For expected inflation, we later also use the survey
of the University of Michigan, which is a one-year
inflation expectation. For equities, we take the risk
premium from Damodaran (2023), and for growth we
use the average of the past 10-year growth in industrial production.
Drivers of the Stock–Bond
Correlation
Due to data availability, we can only estimate the
theoretical model developed in “Theoretical Drivers
of the Stock–Bond Correlation” over a relatively
recent sample starting in 1961. For our deep historical sample starting in 1875 (shown in Figure 2), we
are limited to examining a smaller set of potential
drivers: inflation and real rates.8 We continue by
examining the drivers of the stock–bond correlation
internationally for the G7 countries and for five large
emerging markets. Finally, we show that using uncertainty in inflation forecasts further improves our
understanding of the variability of the stock–bond
correlation.
Empirical Results. Descriptive statistics on the
sample starting in 1875 can be found in Table OB1
in Online Appendix B. The data on each of the theoretical drivers discussed in “Theoretical Drivers of the
Stock–Bond Correlation” is not available over long
historical periods. Therefore, we limit ourselves to
realized inflation levels (see, e.g., Ilmanen 2003) and
the real interest rates that have been shown to be
helpful in explaining the stock–bond correlation in
the literature; see, for example, Yang, Zhou, and
Wang (2009) and Wu et al. (2022).9 Regimes with
high interest rates are associated with higher stock–
bond correlation, as interest rates are then more
important in determining stock and bond returns. As
discussed in “Theoretical Drivers of the Stock–Bond
Correlation,” the level and uncertainty of inflation are
highly related and difficult to disentangle.
Table 1 contains the results of regression models to
explain the stock–bond correlation for the United
States, the United Kingdom, and France over 36-
month periods. For each country, we have three columns with regression results. The first column contains the full-sample results, which start in 1875 for
the United States, in 1801 for the United Kingdom,
and in 1871 for France. The second column contains
the sample until 1951. The third column contains the
post-1951 period, or the modern sample that is likely
to be more representative of the current environment. The reason to choose 1951 as a breakpoint is
the Treasury Accord of 1951, which is often used as
a regime shift in U.S. fixed-income markets, and
many empirical studies start afterward.
For the United States, both inflation and the real rate
are significant over the full sample period. As
expected, the effect of inflation is positive (coefficient ¼ 4.48, t statistic ¼ 4.04) and the effect of
the real rate is also positive (coefficient ¼ 4.36,
t statistic ¼ 3.47). The explanatory power of the
model is limited, with an adjusted R2 of 0.19. When
we examine the two subperiods, it becomes clear
that the explanatory power is solely due to the modern, post-1951 sample. The adjusted R2 is only 0.01
for the 1875–1951 sample, and both explanatory
variables are insignificant. Over the more recent
period, the adjusted R2 is markedly higher at 0.39,
and both explanatory variables are statistically significant (inflation t statistic ¼ 3.82, real rate t
statistic ¼ 4.17). We perform a statistical test to
examine whether the parameters during the first subsample, which are positive but not statistically significant, are different from the parameters in the second
subsample. The p value of this F test is 0.019, indicating that the parameters are indeed significantly
different from each other.10
For the United Kingdom, there is no statistical
significance for inflation over the full sample
(t statistic ¼ 1.01), but the real rate is (t statistic ¼ 2.03).
The explanatory power of the model is low, with an R2
of only 0.05. For the historical sample, both coefficient
estimates are positive, but they are not statistically
significant (inflation t statistic¼ 1.40, real rate
t statistic¼ 1.52), and the explanatory power is weak,
with an adjusted R2 of 0.04. For the modern sample,
we find that both inflation and real rate are positive
and statistically significant (inflation t statistic¼ 3.59,
real rate t statistic ¼ 2.95). While the coefficients
are similar to those in the United States, the explanatory power for the United Kingdom is lower, at
0.25. A statistical test for differences in coefficient
estimates over the two subsamples does not reject
Empirical Evidence on the Stock–Bond Correlation
Volume 80, Number 3 21
the null hypothesis of equal coefficients, with a
p value of 0.853. The reason is that while the coefficients are not statistically significant over the first
subsample, they are similar in magnitude to those
estimated over the modern sample. The results of
France are like those of the United States and the
United Kingdom.11 Over the full sample both inflation and real rates are significant, over the first subsample they are both insignificant, and over the
modern sample they are again significant. The
explanatory power is low over the full sample (0.09)
and the historical subsample (0.19) but reaches 0.42
over the modern subsample. The coefficients are
significantly different over the first and second subsample, with a p value of 0.004.
Our results are consistent with the approach of Baele
and Van Holle (2017), which uses monetary policy to
understand time variations in the correlation between
stocks and bonds. A countercyclical monetary policy
in periods of low inflation implies that the central
bank’s monetary policy will be primarily guided by
growth and unemployment. Central bank policies over
the last twenty years reflect well this environment.
Inflation is less of a concern to central bankers, and
lower growth will directly lead to lower real rates, and
conversely, higher growth will lead to higher real
rates. Therefore, bonds will become countercyclical
assets with very attractive hedging characteristics.
Bonds will benefit not only from lower inflation and
real rates but also from declining risk premia and
therefore will be negatively correlated with equity.
However, in the absence of countercyclical policies,
lower inflation alone is not sufficient to create a negative stock–bond correlation. A structural shift in central bank policies occurred after World War II as
countercyclical monetary policies seeking to balance
inflation and unemployment became commonplace. In
the United States, Bordo (2007) notes that the Fed
regained its independence with the Treasury-Fed
Accord of 1951 and “began following a deliberate countercyclical policy under the directorship of William
McChesney Martin.” Before World War II, the Fed
monetary policy was dictated by either the gold standard (see Elwell 2012) or the real bill doctrine, which
resulted in monetary policies that at best were cycleagnostic and often were pro-cyclical. Taylor (1999)
uses his eponymous rule to explain monetary policy
and finds that inflation and output gap do not explain
real interest rates set by the Fed during the 1879 to
1914 period. On the other hand, Taylor finds that
since the 1950s the output gap and inflation played
an increasingly important role in explaining changes in
Fed policy rates. Therefore, the seemingly surprising
lack of relation between inflation and stock–bond correlation that we observe before during our historical
sample could simply illustrate that countercyclical
monetary policy has become the norm, but absent
these policies it is not clear that we would observe
such a strong relation among inflation, real rates, and
the stock–bond correlation.
Because of data availability to estimate the theoretical drivers of the stock–bond correlation, we focus
exclusively on the modern sample in the remainder
of this section. Our sample starts a little later, in
Table 1. Explaining the Stock–Bond Correlation over the Long Term
United States United Kingdom France
Start 1875 1875 1952 1801 1801 1952 1871 1871 1952
End 2023 1951 2023 2023 1951 2023 2023 1951 2023
Intercept −0.05 0.15 −0.20 0.27 0.30 −0.06 0.12 0.44 −0.12
t statistic −0.77 2.12 22.36 5.68 4.55 −0.73 1.90 4.35 −1.57
Inflation 4.48 0.96 5.66 0.75 2.61 3.80 2.28 −2.80 3.42
t statistic 4.04 0.55 3.82 1.01 1.40 3.59 2.60 −0.95 3.53
Real rate 4.36 0.70 7.35 1.88 2.88 3.70 2.78 −2.02 7.01
t statistic 3.47 0.44 4.17 2.03 1.52 2.95 3.32 −0.69 6.06
Adj R2 0.19 0.01 0.39 0.05 0.04 0.25 0.09 0.19 0.42
Equality (p value) 0.019 0.853 0.004
Notes: Dependent variable is the 36-month Spearman rank correlation between stock and bond markets over the full sample period
(starting dates for United States: January 1875, United Kingdom: January 1801, France: January 1871, same end date: June 2023),
over a historical sample until December 1951, and over a modern sample starting in January 1952. Independent variables are measured as averages over the same 36-month period as the dependent variable. The t statistics use Newey and West (1987) standard
errors with 35 overlapping observations. Bold t statistics indicate statistical significance at the 5% level. The bottom row contains
the p value corresponding to the F test for equality of the coefficients for inflation and real rate over the two subsample periods.
Source: Authors.
Financial Analysts Journal | A Publication of CFA Institute
22
1961, as this is the starting date of the bond risk premium estimates from Adrian, Crump, and Moench
(2013) that we use.12
Table 2 contains the estimation results over the
period from 1961 to 2023. The first column,
labeled with “Theoretical,” includes each of the factors from Equation (3).
13 About half of the correlations have a statistically significant coefficient with
the expected sign. For example, a positive correlation between the change in bond and equity risk
premia is associated with a positive effect on the
stock–bond correlation (coefficient ¼ 0.74, t
statistic ¼ 3.76). The relation between bond risk and
equity risk premia can change significantly over
time. During periods of higher inflation uncertainty,
government bonds behave more like risky assets,
which impacts positively the stock–bond correlation.
The correlation between the bond risk premium
and growth is the only one with a statistically significant estimate of the wrong sign (coefficient ¼ 0.56, t statistic ¼ 2.53). The volatility of
expected inflation has a negative sign, contrary to
the theoretical model’s predictions, but is not statistically significant (coefficient ¼ −0.47, t
statistic ¼ −0.66). This may be due to the difficulty
of obtaining a reliable proxy for inflation uncertainty. We show in the following section that for a
similar model based on survey-based measures of
inflation uncertainty, the volatility of expected inflation has a positive sign and is statistically significant. The volatility of the real short interest rate
has a statistically significant positive coefficient
(coefficient ¼ 0.21, t statistic ¼ 3.16).
The next column, labeled with “Empirical,” contains
only two purely empirically motivated level variables,
which we also used over the historical samples in
Table 1. The level of realized inflation and real interest rate are statistically significant and have t values
well above two.14 The explanatory power of this simple two-parameter model, as measured by the
adjusted R2
, is 0.52, whereas the explanatory power
of the theoretical model with eleven parameters is
0.63. Although lacking theoretical support, our simple
“empirical” model can explain a large share of the
time-variation of the stock–bond correlation.15 This
suggests that the Friedman–Ball hypothesis is valid
for both inflation and real rates. Higher inflation levels and real rate levels come with higher inflation and
real rate uncertainty. Therefore, in the absence of a
precise measure of inflation and real rates uncertainty, the levels of inflation and real rates do a very
good job of capturing uncertainty.
The final column contains the combination of the
theoretical and empirically motivated variables. The
same sign and statistical significance of both
Table 2. Explaining the 36-Month Stock–Bond Correlation
Theoretical Empirical Combination
Coeff. t statistic Coeff. t statistic Coeff. t statistic
q (brp, erp) 0.74 3.76 – 0.34 3.67
q (brp, p) 0.08 0.57 – 0.03 0.26
q (brp, rr) −0.08 −0.82 – −0.16 −2.83
q (brp, g) 0.56 2.53 – 0.25 2.03
q (p, erp) −0.03 −0.30 – −0.04 −0.49
q (p, g) −0.18 −1.49 – −0.01 −0.14
q (rr, erp) 0.62 4.65 – 0.62 7.05
q (rr, p) 0.28 2.99 – 0.30 3.31
q (rr, g) 0.07 0.46 – −0.24 22.22
r (p) −0.47 −0.66 – 0.62 0.96
r (rr) 0.21 3.16 – −0.18 −1.84
l (p) – − 7.72 4.73 9.99 6.28
l (rr) – − 9.39 5.25 9.31 7.85
Adjusted R2 0.63 0.52 0.79
Notes: Dependent variable is the 36-month Spearman rank correlation between U.S. stock and bond markets
over the period June 1961 to June 2023. Each component from Equation (3) is shown here, where correlations
are indicated with q, volatilities with r, and ex-post averages with l. The components are as follows: bond risk
premium (brp), equity risk premium (erp), real interest rate (rr), growth (g), and inflation (p). The column “Coeff”
the estimated coefficients, and the t statistics use Newey and West (1987) standard errors with 35 overlapping
observations. t statistics in bold are significant at the 5% level and of the expected sign.
Source: Authors.
Empirical Evidence on the Stock–Bond Correlation
Volume 80, Number 3 23
empirical level variables are still there, indicating that
they are not subsumed by the theoretically motivated
variables. Again, four are statistically significant with
the expected sign, of which three are the same as in
the model in the first column. Both volatilities are
statistically insignificant, possibly because of the positive association between the level and volatility of
inflation. The adjusted R2 is 0.79, about 0.16 higher
than the model without the level variables.
Figure 3 illustrates the three models’ ability to explain
the stock–bond correlation. The theoretical model follows the estimated stock–bond correlation closely
most of the time. It is late to turn positive during the
second half of the 1970s. It picks up very well the sign
switch in the late 1990s and captures the spike in correlation we experienced after the COVID-19 crisis. The
empirical model also captures the general level of the
stock–bond correlation. It leads to much smoother estimates and does not adjust as quickly during regime
shifts. As expected, the combined model shows a very
good fit with the observed U.S. stock–bond correlation
over this period.
These empirical results indicate that the theoretically
motivated variables can explain a large part of the
time-series variation of the stock–bond correlation
and are preferred over a simple model with the level
of inflation and the real rate. At the same time, for
many countries outside the United States, several of
these theoretically motivated explanatory variables
are difficult to obtain or estimate. Our results suggest
that practitioners who aim to analyze international
financial markets can rely on the easier-to-obtain levels of inflation and the real rate. Even though the
explanatory power is somewhat lower, it can explain
about half the time-series variation in the stock–
bond correlation. In the next subsection, we examine
the international dimension of our results.
International Evidence from Developed
and Emerging Markets. Because we do not
have data on each of the theoretically motivated variables for our international sample, we perform the
regression analyses on the two empirically motivated
level variables, inflation and real rates, which we
found to give reasonably good results for the United
Figure 3. Fit of the Explanatory Models for the Stock–Bond Correlation
Notes: Figure shows the stock–bond correlation and the explanatory values based on the theoretically motivated model, the empirically motivated model, and the combination of the two, as well as the U.S. stock–bond correlation, calculated as the Spearman correlation over rolling 36-month periods over the period June 1961 to June 2023.
Source: Authors.
Financial Analysts Journal | A Publication of CFA Institute
24
States in the previous section. We repeat this for the
six other countries that make up the G7: Canada,
France, Germany, Italy, Japan, and the United
Kingdom. In addition, we add five large emerging
markets that have a substantial data history of both
investable government bonds and equity markets:
Brazil, Malaysia, Mexico, South Africa, and Thailand.
Since the sample period is now shortened to start in
1987 for the other developed markets, we also
include the United States over the same sample
period.16 The samples for the emerging markets start
later, mostly at the turn of the millennium and at the
latest in January 2002.
Table 3 shows the model with only realized inflation
and real rates. We see that over this shorter estimation period, both variables for the United States are
still statistically significant, with t values of 2.77 and
2.79. For three out of six other G7 countries, the
coefficient for inflation is also statistically significant.
It seems that inflation is somewhat less important in
this sample that starts in 1988, as the inflationary
periods from the 1970s are not included. The real
rates are significant for all G7 countries except Italy,
where it has a t value of 1.43. The explanatory
power for Italy is rather low, with an adjusted R2 of
only 0.12. This may be related to its creditworthiness
during the European sovereign debt crisis, where
Italian government bonds traded as a risky instead of
a safe asset. The distribution of its S&P credit rating
is displayed below the R2 in Table 3, where this
increased riskiness can be observed.
To examine whether the low explanatory power is
characteristic of countries with lower credit ratings,
we extend our sample with five large emerging
markets that have sufficiently long histories of
local-currency government bond and equity market
returns. The frequency of the credit ratings is displayed at the bottom of Table 3. Of the five emerging markets, Malaysia has been the least creditrisky, as it was A-rated for most of the sample
period, while the four other countries mostly were
BBB- or BB-rated. For four out of five countries, the
explanatory power of inflation and the real rate is
low, with R2 values below 0.20. The only exception
is Mexico, which has an R2 of 0.43, similar to that of
the United States. This may have to do with the
partial integration of financial markets of these two
geographical neighbors. The results for the United
States hold up for countries with safe-haven characteristics, but generally not for riskier countries. In
this instance, researchers on international financial
markets cannot automatically extrapolate the U.S.
results but need to take the credit quality of the
country into account. This difference is an important
insight for practitioners who want to apply the
model outside the United States, something that is
Table 3. Explaining the 36-Month Stock–Bond Correlation: International Evidence
G7 countries Emerging markets
CA FR DE IT JP UK US BR MY MX ZA TH
Inflation 5.51 −2.00 18.87 1.52 14.67 10.92 14.27 −0.60 27.51 8.49 2.90 2.25
t statistic 0.73 −0.14 3.61 0.42 2.49 3.48 2.77 −0.16 1.76 4.16 1.48 0.70
Real rate 11.47 8.62 4.66 3.40 9.96 5.01 8.57 −0.83 23.56 6.51 −0.25 7.46
t statistic 3.77 2.50 2.10 1.43 2.93 2.29 2.79 −0.53 1.48 4.53 −0.12 1.56
Intercept −0.24 −0.07 −0.48 0.15 −0.35 −0.27 −0.46 0.43 −0.55 −0.21 0.16 −0.02
t statistic −1.85 −0.38 −3.10 1.26 −6.93 −2.18 −3.34 1.38 −1.18 −1.98 1.27 −0.32
Adjusted R2 0.60 0.31 0.42 0.12 0.58 0.41 0.40 0.01 0.19 0.43 0.05 0.18
Credit rating AAA AAA AAA A AA AAA AAA BB A BBB BBB BBB
AAA 72 67 100 0 36 78 64 0 0 0 0 0
AA 28 33 0 50 39 22 36 0 0 0 0 0
A 0 0 0 17 25 0 0 0 91 0 0 0
BBB 0 0 0 33 0 0 0 30 9 96 57 100
BB (or lower) 0 0 0 0 0 0 0 61 0 4 43 0
Notes: Dependent variable is the 36-month Spearman rank correlation between stock and bond markets for the G7 over the period
January 1988 to June 2023. CA¼ Canada, FR¼ France, DE¼ Germany, JP¼ Japan, UK¼ United Kingdom, US¼ United States. For
emerging markets, BR ¼ Brazil (start January 2002), MY¼ Malaysia (start January 2002), MX¼ Mexico (start January 2002),
ZA¼ South Africa (start July 1994), TH¼ Thailand (start¼ February 2001). Independent variables are measured as averages over the
same 36-month period as the dependent variable. The rows with “t statistic” contain t statistics using Newey and West (1987) standard errors using 35 overlapping observations. Bold indicates statistical significance at the 5% level. Credit rating contains the average S&P credit rating over the sample period. The distribution of credit ratings is displayed in the bottom five rows, in percentages.
Source: Authors.
Empirical Evidence on the Stock–Bond Correlation
Volume 80, Number 3 25
often disregarded in the finance literature (see, e.g.,
Karolyi 2016).
These international results confirm to a large extent
our observations for the United States, as the inflation and the realized real return on the Treasury bill
are important drivers of the stock–bond correlation
over the period from 1987 to 2023 for countries
with a relatively safe government bond market.
Uncertainty in Inflation Expectations. So
far, our series on expected inflation has been the
past 10-year average. However, for a shorter sample
period, we can also make use of surveys of expected
inflation. This allows us to infer not only the level of
expected inflation but also the uncertainty surrounding the expectation by examining the dispersion of
inflation expectations of the respondents. This may
be a better measure of inflation risk than the timeseries volatility of inflation, especially in case of inflation shocks; see David and Veronesi (2013).17
Therefore, in the theoretical model we use the
expected inflation from the Michigan survey, which is
available from 1978 onward, instead of the past 10-
year realized inflation. We also replace the timeseries volatility of inflation with the cross-sectional
dispersion of inflation expectations.18 We leave the
two variables from the empirical model unchanged.
Table 4 contains the new estimation results.
An important difference with our previous model
shown in Table 2 is that the coefficient for the volatility of expected inflation is now positive and statistically significant. Most other explanatory variables
have the same sign as in Table 2, but more are statistically significant. The explanatory power increases
from 0.63 in Table 2 to 0.82 in Table 4. The combination model shows that the coefficients for inflation
level and real risk-free rate remain significant when
survey inflation expectations are used. Several coefficients that were significant in the first column are no
longer significant. Their role is taken over by the two
important empirically motivated variables. The
explanatory power of the combined model reaches
even 0.88. Figure OB2 in Online Appendix B illustrates the fit of these models over time.
Investment Implications
In this section, we analyze the investment implications in more detail. The first and most straightforward implication concerns the risk of multi-asset
portfolios. The second implication that we discuss is
the link of the stock–bond correlation with the
expected bond risk premium, extending the important work of Ilmanen (2003).
Time-Varying Risk of a Multi-Asset
Portfolio. A higher correlation between stocks and
bonds implies a higher risk for multi-asset or balanced
portfolios that many institutional and retail investors
hold. Figure 4 shows the 36-month volatility of the 60/
40 stock/bond portfolio on the vertical axis as a function of the stock–bond correlation measured over the
same period on the horizontal axis.19 This empirical
analysis complements the hypothetical portfolio analysis
in Brixton et al. (2023). The colors of the dots represent
the two different regimes: 1970–1999 and 2000–2023.
The first period shows a stock–bond correlation of
þ0.35, while it is −0.29 in the second period. The scatterplot is far from a straight line, indicating that the
explanatory power of the stock–bond correlation for
portfolio risk is not perfect, as in the theoretical example of Figure 1 where we held volatilities constant.
Time variation in bond and especially equity volatility
also plays an important role for portfolio risk.
During the first regime, with the positive stock–bond
correlation, the volatility of the 60/40 portfolio was
close to 10.5%. During the second regime, with the
negative stock–bond correlation, the volatility of the
60/40 portfolio declined to 8.4%. This decline can be
partially attributed both to a decline in bond volatility
(from 8.2% to 7.3%; see Table 5) and a switching sign
of the stock–bond correlation. A multi-asset investor
who aims to keep their risk profile constant may need
to reduce the allocation to equities in times of a positive stock–bond correlation. Holding volatilities constant over the entire sample, a return to the first
subsample positive correlation between stocks and
bonds requires that 60/40 investors reduce their
equity position by 25% (i.e., invest in a 35/65 portfolio)
to arrive at the same portfolio risk.20
Changes in the correlation between stocks and bonds
should also affect the contribution of the sources of
the variance in a multi-asset portfolio. Table 5 contains the variance decomposition of the portfolio volatility in equity, bond, and correlation risk. Indeed,
during the negative stock–bond correlation regime,
more than 100% of the variance of a multi-asset
portfolio can be ascribed to equities, as bond investments reduce overall portfolio variance. During the
positive stock–bond correlation regime, the contribution of bonds to total portfolio risk is positive. The
empirical and theoretical models that we developed
in “Theoretical Drivers of the Stock–Bond
Correlation” explain current levels of the stock–bond
correlation with contemporaneous macroeconomic
Financial Analysts Journal | A Publication of CFA Institute
26
Table 4. Explaining the 36-Month Stock–Bond Correlation with Survey
Expectations
Theoretical Empirical Combination
Coeff. t statistic Coeff. t statistic Coeff. t statistic
q (brp, erp) 0.44 2.96 0.25 1.84
q (brp, p) 0.57 3.46 0.42 2.57
q (brp, rr) 0.23 1.81 0.07 0.60
q (brp, g) 0.56 4.24 0.40 2.52
q (p, erp) 0.40 2.19 0.40 2.08
q (p, g) −0.44 22.00 0.01 0.02
q (rr, erp) 0.77 5.33 0.95 6.28
q (rr, p) 1.41 7.35 0.20 0.64
q (rr, g) −0.63 22.76 −0.37 −1.73
r (p) 4.76 2.96 4.01 3.55
r (rr) 0.11 3.64 −0.09 −1.50
l (p) 6.33 2.90 7.36 3.28
l (rr) 10.10 4.48 7.63 4.12
Adjusted R2 0.82 0.55 0.88
Notes: Dependent variable is the 36-month Spearman rank correlation between U.S. stock and bond markets
over the period January 1978 to June 2023. Each component from Equation (3) is shown here, where correlations are indicated with q, volatilities with r, and ex-post averages with l. p refers to the expected inflation
from the Michigan survey, and its volatility is the cross-sectional volatility of the estimates. The column “Coeff.”
contains the estimated coefficients, and “t statistic” contains the corresponding t statistics using Newey and
West (1987) standard errors using 35 overlapping observations.
Source: Authors.
Figure 4. Relation between Stock–Bond Correlation and Portfolio Risk
Notes: Average of standard deviation and Pearson correlation coefficient of monthly returns computed over 36-month rolling windows ending January 1970 to June 2023.
Source: Authors.
Empirical Evidence on the Stock–Bond Correlation
Volume 80, Number 3 27
variables. To forecast the stock–bond correlation,
one needs to be able to forecast these macroeconomic variables, which is beyond the scope of this
paper. However, our research outlines the importance of changing macroeconomic environments to
understand the risk of multi-asset class portfolios.
For example, the coefficient estimates of the empirical model in Table 2 indicate that a 1% increase in
both inflation and real rates results in a þ 0.17
increase in the correlation between stocks and
bonds. In turn, this can lead to an increase of 0.8%
to 1.7% in the risk of a 60/40 portfolio, depending
on the starting stock–bond correlation.21 Therefore,
reliable macroeconomic forecasts are a critical input
for cross-asset class risk management and in the
absence of reliable macroeconomic forecast one
should use macro scenario analysis and stress tests.
The increase in total risk due to stock–bond correlation concerns investors who are not affected by the
present value of their liabilities. However, for multiasset investors with long-dated unhedged bond-like
liabilities, such as pension funds and life insurance
companies, an increase in the stock–bond correlation
would also decrease their solvency risk, as stocks
now better hedge liability risk. In our analysis of
bond risk premia, we assume that the marginal investor does not have unhedged bond-like liabilities.22
The Bond Risk Premium. A higher stock–bond
correlation makes bonds a riskier investment for
multi-asset investors. It could increase the bond risk
premium that investors require for holding bonds
instead of short-term Treasury bills. This can also be
seen from the CAPM:
E Rf g bonds − Rriskfree ¼ b  E Rf g market − Rriskfree
where
b ¼ cov Rbonds f g , Rmarket
var Rf g market
¼ rbonds
rmarket
 qbonds, market
Stated differently, the bond risk premium is a function of bond volatility, the correlation of bond returns
with the market, and the Sharpe ratio of the market:
E Rf g bonds − Rriskfree ¼ rbonds  qbonds, market

E Rf g market − Rriskfree
rmarket
Given the higher volatility of equity relative to bonds,
equity markets play a dominant role in the variation
of the market portfolio. Therefore, one can assume
that variations in the correlation between bond
returns and the market returns are closely related to
variations in the correlation between bond returns
and stock returns. A higher correlation implies a
higher CAPM-implied risk premia for bonds; see
Singer and Terhaar (1997). However, there are other
theories for the bond risk premium, such as an inflation-risk premium or preferred habitat by long-term
investors such as pension funds, insurance
Table 5. Risk and Return of the 60/40 Stock–Bond Portfolio
1970–2023 1970–1999 2000–2023
Stock–bond correlation 0.07 0.35 −0.29
Bond premium ACM (%) 1.7 2.4 0.9
Stock Bond 60/40 Stock Bond 60/40 Stock Bond 60/40
Excess return (%) 6.0 2.1 4.7 5.7 1.6 4.3 6.4 2.8 5.3
Volatility (%) 14.8 7.8 9.6 14.8 8.2 10.5 14.7 7.3 8.4
Sharpe ratio 0.51 0.28 0.59 0.45 0.20 0.45 0.58 0.37 0.77
Variance decomposition
Equity (%) 100 0 89 100 0 71 100 0 111
Bond (%) 0 100 12 0 100 11 0 100 14
Stock–bond correlation (%) 0 0 −1 0 0 18 0 0 −25
Notes:Top panel: Average of 36-month excess returns, standard deviation, Sharpe ratio, and Pearson correlation coefficient of
monthly returns computed over 36-month overlapping windows ending January 1970 to June 2023. Bottom panel:
Decomposition of the 60/40 portfolio variance into equity, bonds, and equity-bonds co-movements. 100% ¼ 60%2r2ð Þ stocks
r2ð Þ 60=40 þ
40%2r2ð Þ bonds
r2ð Þ 60=40 þ 2∙60%∙40%∙rð Þ stocks rð Þ bonds qðstocks, bondsÞ
r2ð Þ 60=40 : Each of the three variance components is computed over 36-month rolling windows ending January 1970 to June 2023. We take the average of each component during each period. This explains why the sign
of the stock–bond correlation is slightly positive over the full sample period, while it is slightly negative for the variance decomposition. ACM ¼ Adrian, Crump, and Moench models.
Source: Authors, Federal Reserve Bank of New York
Financial Analysts Journal | A Publication of CFA Institute
28
companies, and sovereign wealth funds; see Vayanos
and Vila (2021).
We can also try to directly estimate the expected
bond risk premium without taking the CAPM as a
starting point. This is not a straightforward exercise