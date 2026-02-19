---
url: https://saudijournals.com/media/articles/SJBMS_109_470-477_FT.pdf
title: [PDF] An Assessment of Contagion between Emerging Stock Markets and ...
domain: misc
crawled_at: 2026-02-04T08:08:17.205016+00:00
source: exa_search
chart_count: 0
image_links:
outbound_links:
---

Citation: Amit Das & Amalendu Bhunia (2025). An Assessment of Contagion between Emerging Stock Markets and 
Developed Stock Markets. Saudi J Bus Manag Stud, 10(9): 470-477.
 470
 
 
Saudi Journal of Business and Management Studies
Abbreviated Key Title: Saudi J Bus Manag Stud
ISSN 2415-6663 (Print) | ISSN 2415-6671 (Online)
Scholars Middle East Publishers, Dubai, United Arab Emirates
Journal homepage: https://saudijournals.com
Original Research Article
An Assessment of Contagion between Emerging Stock Markets and 
Developed Stock Markets
Amit Das1*, Amalendu Bhunia2
1Assistant Professor, Department of Commerce, Surendranath Evening College, Kolkata 700009, India
2Professor, Department of Commerce, Kalyani University, Nadia, India
DOI: https://doi.org/10.36348/sjbms.2025.v10i09.003 | Received: 04.09.2025 | Accepted: 17.10.2025 | Published: 23.10.2025
*Corresponding author: Amit Das
Assistant Professor, Department of Commerce, Surendranath Evening College, Kolkata 700009, India
Abstract
This study investigated financial contagion between emerging and developed stock markets using the DCC-GARCH model 
over the period January 2010 to December 2024. Daily logarithmic return data from eight markets, namely, four emerging 
(India, Brazil, South Africa, Indonesia) and four developed (USA, UK, Germany, Japan) were analyzed across pre-crisis, 
COVID-19 crisis, and post-crisis periods. Descriptive statistics revealed non-normality and volatility clustering, justifying 
GARCH modeling. The ADF test confirmed stationarity at first differences. Univariate GARCH (1,1) estimates showed 
high volatility persistence. DCC-GARCH results revealed significant time-varying correlations, with crisis-period surges 
indicating contagion. Correlations remained elevated post-crisis, suggesting structural interdependence. Time-varying 
correlations peaked during the COVID-19 crisis, with Brazil–Germany and India–USA exhibiting the highest increases. 
Wavelet coherence analysis further confirmed contagion with high short- and medium-term co-movement, particularly 
between Indonesia–Japan and Brazil–Germany. Findings underscored that contagion was dynamic and scale-dependent, 
driven by trade ties, market openness, and global shocks. The study concluded that during crises, diversification benefits 
across these markets diminished significantly due to synchronized volatility and persistent financial linkages.
Keywords: Contagion Effect, Emerging Stock Markets, Developed Stock Markets, COVID-19 Crisis, Wavelet Coherence 
Analysis.
JEL Codes: G12 Stock market, G01 Financial crises, C22 ADF test.
Copyright © 2025 The Author(s): This is an open-access article distributed under the terms of the Creative Commons Attribution 4.0 International 
License (CC BY-NC 4.0) which permits unrestricted use, distribution, and reproduction in any medium for non-commercial use provided the original 
author and source are credited.
1. INTRODUCTION
In an era of financial globalization, the 
interconnectedness of global stock markets has 
intensified, raising renewed concerns about the spread of 
financial contagion across borders. Financial contagion 
refers to the significant increase in cross-market linkages 
during periods of crisis, causing shocks in one market to 
transmit rapidly to others (Forbes & Rigobon, 2002). 
While financial integration brings opportunities for 
capital diversification, it also amplifies systemic risks, 
particularly for emerging markets that are more 
susceptible to external shocks due to their relatively 
underdeveloped financial systems (Bekaert et al., 2014).
The relevance of this study is underscored by a 
series of recent economic disruptions including the 
COVID-19 pandemic, global inflationary pressures, 
interest rate hikes by central banks in developed 
economies, and geopolitical conflicts such as the RussiaUkraine war that have triggered volatility across global 
financial markets. These events have revived debates 
about the transmission mechanisms of financial shocks, 
especially from developed to emerging markets. Recent 
studies (Diebold & Yilmaz, 2014; Phylaktis & 
Ravazzolo, 2020) suggest that the pattern and intensity 
of contagion have evolved, prompting the need for a 
fresh and timely investigation into these dynamics. 
Additionally, the increased integration of emerging 
markets into the global financial ecosystem through 
cross-border investments and digital trading platforms 
further necessitates the assessment of whether these 
markets act merely as shock absorbers or active 
transmitters of global financial stress (Aloui et al., 2011; 
Umar & Suleman, 2017).
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 471
Although the phenomenon of contagion has 
been extensively studied, this study contributes novel 
insights through expanding the temporal scope to include 
both pre- and post-pandemic periods, allowing for a 
more comprehensive understanding of evolving 
contagion dynamics, applying Dynamic Conditional 
Correlation (DCC-GARCH) models and wavelet 
coherence analysis to capture both time-varying and 
frequency-based relationships (Kumar & Padakandla, 
2020), comparing asymmetric effects of contagion i.e., 
from developed to emerging markets and vice versa, 
which remains an underexplored area (Kenourgios et al., 
2011).
2. LITERATURE REVIEW
The concept of financial contagion has been 
extensively studied, particularly in the wake of major 
financial crises. Contagion is understood as a significant 
increase in cross-market linkages after a shock (Forbes 
& Rigobon, 2002), where shocks originating in one 
market or region are transmitted rapidly to others, 
especially during periods of turbulence. This 
phenomenon challenges the conventional assumptions of 
portfolio diversification and poses critical concerns for 
investors and policymakers alike.
Early studies emphasized the role of 
interdependence and market fundamentals in explaining 
co-movements between markets. For instance, Forbes 
and Rigobon (2002) argued that what is labelled as 
contagion may simply reflect strong interdependence. 
However, subsequent studies highlighted that during 
crisis periods, co-movements between markets intensify 
beyond what fundamentals would suggest, indicating 
true contagion (Bekaert et al., 2005). The Asian 
Financial Crisis (1997), the Dot-com Bubble (2000), and 
the Global Financial Crisis (2008) spurred a wave of 
empirical research into contagion channels. Chiang et al., 
(2007) used multivariate GARCH models and found 
increased co-movement among Asian markets during the 
1997 crisis, indicating contagion. Similarly, Aloui et al., 
(2011) demonstrated strong evidence of contagion 
between developed and emerging markets using copulabased models.
A variety of methods have been developed to 
capture contagion effects, including correlation-based 
techniques, GARCH-family models, and more recently, 
wavelet and copula approaches. Forbes and Rigobon 
(2002) argued for a clearer distinction between 
interdependence (persistent correlation) and contagion (a 
significant increase in correlation during crises).
The COVID-19 pandemic, ongoing geopolitical 
conflicts, and monetary policy shifts in developed 
economies have prompted a reevaluation of contagion 
dynamics in recent years. For example, Phylaktis and 
Ravazzolo (2020) used time-varying correlation models 
and confirmed significant contagion effects during 
COVID-19, especially from U.S. and European markets 
to emerging markets. Diebold and Yilmaz (2014) 
developed a spillover index to measure dynamic 
connectedness and found that spillovers intensified in 
global downturns, making this an essential tool for 
evaluating financial contagion in modern contexts. 
Emerging research also considers regional 
heterogeneity. For example, Kumar and Padakandla 
(2020) identified asymmetric volatility spillovers
between BRICS economies and developed markets. 
They noted that the degree and direction of contagion can 
vary significantly depending on global economic 
conditions and regional integration levels.
The COVID-19 pandemic introduced a new 
layer of complexity to the contagion literature. Phylaktis 
and Ravazzolo (2020) found significant contagion during 
the pandemic, particularly from U.S. and European stock 
markets to Asia and Latin America. Similarly, Umar and 
Gubareva (2020) noted that the health crisis led to 
structural breaks and increased volatility 
interdependence across both developed and emerging 
markets. Moreover, geopolitical tensions such as the 
Russia–Ukraine conflict, alongside tightening monetary 
policies in developed economies, have re-emphasized 
the relevance of understanding contagion channels in the 
post-pandemic world (Zaremba et al., 2021).
While extensive research exists on contagion 
from developed to emerging markets, limited studies 
explore bidirectional or reverse contagion, especially in 
the context of post-pandemic shocks. Moreover, the use 
of multi-scale econometric models remains 
underutilized, leaving gaps in understanding the timevarying and frequency-dependent dynamics of 
contagion.
3. THEORETICAL FRAMEWORK
Financial contagion is the transmission of 
shocks or crises from one market to others, leading to 
synchronized downturns or volatility. The study of 
contagion has gained prominence, particularly in the 
context of global financial crises and periods of 
economic instability. Emerging markets, due to their 
integration with the global economy, can be particularly 
vulnerable to contagion from developed markets, which 
are seen as global economic leaders. This theoretical 
framework explores the fundamental concepts, theories, 
and models that underpin the study of financial 
contagion, especially the dynamic linkages between 
emerging and developed stock markets.
Several theories attempt to explain the 
mechanisms underlying financial contagion. These 
theories broadly fall into two categories: fundamentalsbased contagion and market-driven contagion.
3.1 Fundamentals-Based Contagion
Fundamentals-based contagion is the 
transmission of shocks between markets due to real 
economic factors, such as trade linkages, commodity 
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 472
price dependencies, or economic policies. According to 
this theory, markets are interconnected because of shared 
economic conditions and common external shocks. For 
example, a downturn in a developed market may affect 
an emerging market due to the decline in demand for 
exports or capital flows. During crises, these shared 
vulnerabilities are exposed, amplifying the transmission 
of shocks.
The Real Business Cycle (RBC) Theory
provides the foundation for fundamentals-based 
contagion. According to RBC theory, economic shocks 
in one country, particularly in large economies such as 
the USA or the EU, can have significant ripple effects on 
other markets due to trade and financial linkages. The 
increase in economic interdependence between markets 
enhances the likelihood that an economic shock in a 
developed market will lead to a contagion effect in 
emerging markets.
3.2 Market-Driven Contagion
Market-driven contagion, on the other hand, 
focuses on the role of investor behavior, market 
sentiment, and information transmission during periods 
of financial distress. According to this theory, contagion 
arises not from shared economic fundamentals but from 
the way investors react to news and crises. Investors tend 
to respond to global market movements in a herd-like 
manner, increasing the likelihood of contagion.
The Herding Behavior Theory explains how 
market participants tend to follow the crowd during 
periods of uncertainty, leading to the synchronization of 
asset price movements. In times of financial crisis, 
investors may sell off assets simultaneously, leading to a 
global decline in stock prices. The spread of panic or fear 
through media and social networks can exacerbate this 
effect, causing markets that were previously uncorrelated 
to suddenly co-move.
The Globalization of Financial Markets theory 
further supports market-driven contagion by asserting 
that as global capital flows become increasingly mobile, 
financial shocks in one market can easily spill over to 
others. Investors, seeking to reduce risk, may sell off 
holdings across multiple markets, thereby increasing 
correlations and transmitting shocks.
3.3 Contagion Models and Methodologies
A variety of econometric models and 
methodologies are employed to analyze contagion 
between emerging and developed stock markets. The 
models aim to measure the extent and nature of 
interdependencies and the transmission of shocks. Two 
of the most widely used approaches are:
3.3.1 The Correlation Model
One of the simplest ways to measure contagion 
is by examining correlations between market returns 
before, during, and after a crisis. A sudden increase in the 
correlation of returns during a crisis, compared to stable 
periods, is taken as evidence of contagion. The 
correlation model assumes that a shock in one market 
will lead to a change in the risk-sharing behavior of 
investors, increasing correlations between markets.
However, this approach has limitations. It does 
not account for time-varying relationships or the 
dynamic nature of financial markets. Additionally, 
correlation alone may not fully capture the complex and 
sometimes non-linear relationships between markets.
3.3.2 The Multivariate GARCH Models
To account for the time-varying nature of 
financial volatility and correlations, the Generalized 
Autoregressive Conditional Heteroskedasticity 
(GARCH) family of models has become popular in 
contagion analysis. Specifically, the Dynamic 
Conditional Correlation (DCC) GARCH model is 
employed to examine contagion across markets over 
time.
The DCC-GARCH model allows for the 
modeling of time-varying correlations and the 
quantification of the spillover effect between stock 
markets. It captures how correlations between markets 
change in response to market shocks, thereby providing 
a more nuanced understanding of contagion. The model 
is particularly useful in identifying the dynamic 
correlations between emerging and developed markets, 
which fluctuate with changes in market conditions.
3.4 Factors Influencing Contagion between Emerging 
and Developed Markets
Several factors can influence the degree of contagion 
between emerging and developed stock markets, 
including:
3.4.1 Economic Linkages and Trade Dependencies
Countries with high economic interdependence 
are more likely to experience contagion. For example, 
emerging markets that rely heavily on exports to 
developed markets are particularly susceptible to 
financial shocks originating in the developed world. The 
decline in demand or the tightening of liquidity 
conditions in developed economies can result in reduced 
growth prospects for emerging economies, thereby 
transmitting economic shocks.
3.4.2 Capital Flows and Financial Integration
Financial integration, driven by liberalization 
policies and the globalization of financial markets, has 
increased the exposure of emerging markets to global 
shocks. The liberalization of capital accounts and the 
ease with which capital can flow between countries have 
made emerging markets more vulnerable to sudden shifts 
in investor sentiment. During crises, capital flight from 
emerging markets to developed economies can 
exacerbate contagion.
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 473
3.4.3 Market Sentiment and Investor Behavior
The behavior of global investors can amplify 
contagion. During times of crisis, investors exhibit riskaverse behavior, leading to widespread sell-offs and 
flight to safety. As a result, even markets with relatively 
limited economic ties may experience synchronized 
movements in asset prices. Additionally, as information 
about a crisis spreads globally, investor sentiment can 
lead to herd behavior, further propagating contagion 
effects.
4. DATA AND METHODOLOGY
This study investigated the existence and 
dynamics of financial contagion between emerging and 
developed stock markets by analyzing their return comovements and volatility spillovers over time. This 
study covered a sample of both emerging markets (India, 
Brazil, South Africa, and Indonesia) and developed 
markets (USA, UK, Japan, and Germany). The study 
uses daily closing prices of major stock indices (S&P 
500, FTSE 100, Nikkei 225, DAX, BSE Sensex, 
IBOVESPA, JSE All Share, and IDX Composite) 
spanning from January 2010 to December 2024, which 
included both tranquil periods and crisis episodes such as 
the COVID-19 pandemic and recent geopolitical 
tensions. All data were obtained from Yahoo Finance
and were converted into log returns as follows: Rit=ln(Pit
)−ln(Pi(t−1))
Where Rit is the return of index i at time t, and Pit is the 
closing price of index i at time t.
To examine contagion, the study employs the
Dynamic Conditional Correlation Generalized 
Autoregressive Conditional Heteroskedasticity (DCCGARCH) model developed by Engle (2002). This model 
is particularly suitable for assessing time-varying 
correlations and allows for capturing changes in 
volatility transmission during different market phases.
The mean equation is given by: Rt=μ+εt, εt∼N(0,Ht)
The conditional covariance matrix Ht is decomposed as:
Ht=DtRtDt
Where Dt is a diagonal matrix of time-varying standard 
deviations from univariate GARCH(1,1) models, and Rt
is the time-varying correlation matrix.
The univariate GARCH(1,1) specification for each 
return series is: σ
2
it=ωi+αiε
2
i(t−1)+βi ε
2
i(t−1)
The dynamic correlation structure is estimated using: Qt
=(1−a−b)Qˉ+a(εt−1ε
T
t−1)+bQt−1
Rt=diag(Qt)
−1/2Qtdiag(Qt)−1/2
Where Qt is the time-varying covariance matrix of 
standardized residuals, and Qˉ is the unconditional 
covariance matrix of εt. Parameters a and b capture the 
sensitivity of current correlations to past shocks and past 
correlations, respectively.
The presence of contagion was inferred by 
identifying significant increases in conditional 
correlations during crisis periods, particularly beyond 
historical averages. To supplement this, rolling 
correlation plots and wavelet coherence analysis were 
also used to examine co-movement patterns across 
different time horizons. This methodology provided a 
robust framework to detect contagion by distinguishing 
between interdependence and true structural breaks in 
cross-market linkages. The combination of time-domain 
and frequency-domain approaches enhanced the 
empirical validity and offered deeper insights into the
direction, magnitude, and persistence of contagion 
effects.
5. EMPIRICAL RESULTS AND 
ANALYSIS
This segment presented the empirical findings 
based on the Dynamic Conditional Correlation 
Generalized Autoregressive Conditional 
Heteroskedasticity (DCC-GARCH) model. The purpose 
was to examine the existence and nature of financial 
contagion between emerging and developed stock 
markets over the period from January 2010 to December 
2024. We selected four emerging markets, India (BSE 
Sensex), Brazil (IBOVESPA), South Africa (JSE All 
Share), and Indonesia (IDX Composite) and four 
developed markets, the USA (S&P 500), UK (FTSE 
100), Germany (DAX), and Japan (Nikkei 225). All 
indices are transformed into daily logarithmic returns to 
ensure stationarity. The analysis is divided into precrisis, crisis, and post-crisis periods to understand 
contagion patterns, particularly during the COVID-19 
pandemic and the Russia–Ukraine conflict.
5.1 Descriptive Statistics
Table 1: Descriptive Statistics
Index Mean S.D. Skewness Kurtosis Jarque-Bera (Prob)
S&P 500 0.0004 0.0121 -0.412 3.56 0.0001
BSE Sensex 0.0005 0.0134 -0.321 3.94 0.0003
IBOVESPA 0.0003 0.0162 -0.491 4.12 0.0000
FTSE 100 0.0003 0.0118 -0.276 3.71 0.0004
DAX 0.0004 0.0143 -0.393 3.86 0.0002
Nikkei 225 0.0004 0.0129 -0.310 3.77 0.0001
JSE AllShare 0.0003 0.0132 -0.288 3.59 0.0005
IDX Composite 0.0003 0.0141 -0.472 3.80 0.0002
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 474
Table 1 showed the descriptive statistics. All 
return series show non-normality, confirmed by the 
Jarque-Bera test, and exhibit negative skewness and 
leptokurtosis (fat tails), justifying the use of GARCHtype models. All indices showed positive mean returns, 
though very small in magnitude, ranged between 0.0003 
and 0.0005, indicating slight daily gains over the sample 
period. These modest returns were for daily data and 
suggested no extreme upward or downward bias in the 
markets on average. Volatility is critical for investors as 
higher standard deviation implied greater potential 
returns but also higher risk. IBOVESPA reflected the 
relatively higher risk in the Brazilian market.
5.2 Augmented Dickey-Fuller (ADF) Test
Before running GARCH or DCC-GARCH, it is 
essential to determine the stationarity of the data. Most 
financial models require input variables to be stationary, 
especially when dealing with return series. A unit root 
test helps determine whether a time series is nonstationary (has a unit root) or stationary.
Table 2: ADF Unit Root Test Results
Panel A: Level Form (with Intercept and Trend)
Index ADF Statistic 1% Level 5% Level 10% Level p-value Stationary
S&P 500 -1.421 -3.43 -2.86 -2.57 0.8801 No
BSE Sensex -1.837 -3.43 -2.86 -2.57 0.7120 No
IBOVESPA -2.003 -3.43 -2.86 -2.57 0.6487 No
FTSE 100 -1.932 -3.43 -2.86 -2.57 0.6880 No
DAX -1.674 -3.43 -2.86 -2.57 0.7543 No
Nikkei 225 -1.854 -3.43 -2.86 -2.57 0.7055 No
JSE AllShare -1.693 -3.43 -2.86 -2.57 0.7511 No
IDX Composite -1.902 -3.43 -2.86 -2.57 0.6942 No
Panel B: First Differences (with Intercept and Trend)
Index ADF Statistic 1% Level 5% Level 10% Level p-value Stationary
S&P 500 -11.220 -3.43 -2.86 -2.57 0.0000 Yes
BSE Sensex -10.874 -3.43 -2.86 -2.57 0.0000 Yes
IBOVESPA -10.442 -3.43 -2.86 -2.57 0.0000 Yes
FTSE 100 -9.881 -3.43 -2.86 -2.57 0.0000 Yes
DAX -10.275 -3.43 -2.86 -2.57 0.0000 Yes
Nikkei 225 -9.521 -3.43 -2.86 -2.57 0.0000 Yes
JSE AllShare -9.677 -3.43 -2.86 -2.57 0.0000 Yes
IDX Composite -10.115 -3.43 -2.86 -2.57 0.0000 Yes
Table 2 showed that all indices failed to reject
the null hypothesis of a unit root in level form, indicating 
non-stationarity. It was usual for stock price series. This 
implies that the level data was not suitable for regression 
or forecasting without transformation, as they exhibited 
stochastic trends. All return series were stationary in first 
differences. This confirmed that log returns were suitable 
for further time series analysis like DCC-GARCH and 
Granger causality tests. This confirmed that log return 
series were appropriate inputs for DCC-GARCH, 
volatility spillover models, and contagion analysis, 
satisfying the stationarity condition required for such 
empirical financial models.
5.3 Univariate GARCH (1,1) Model Results
Before estimating the DCC-GARCH model, 
univariate GARCH (1,1) models were estimated for each 
return series to capture individual volatility patterns.
Table 3: Univariate GARCH (1,1) Model Results
Parameter Coefficient S.E. z-Statistic
ω 0.000002 0.0000003 7.00
α 0.116 0.021 5.52
β 0.868 0.017 51.05
The results from the Univariate GARCH (1,1) 
model presented in table 3 provide crucial insights into 
the volatility dynamics of the analyzed financial time 
series. The constant term (ω) was estimated and though 
it was small in magnitude as expected for high-frequency 
financial data, it was statistically significant, indicating 
that a constant baseline variance was present in the 
conditional variance equation. The ARCH coefficient 
(α), which measured the short-term impact of shocks 
(news) on volatility and highly significant, suggesting 
that past squared returns exerted a noticeable immediate 
effect on current volatility. The GARCH coefficient (β), 
represented the persistence of volatility over time, also 
highly significant, implying that volatility shocks decay 
slowly and that the series exhibited strong volatility 
clustering, a common feature in financial markets. The 
sum of α + β = 0.984 indicated high volatility persistence. 
Similar results were observed for other indices, 
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 475
reinforcing the suitability of DCC-GARCH for modeling 
joint volatility. On the whole, the model was wellspecified and effectively captures the time-varying 
nature of volatility, supporting its suitability for 
forecasting and risk management purposes in financial 
return series analysis.
5.4 DCC-GARCH Estimation
The multivariate DCC-GARCH model captures 
time-varying correlations between pairs of emerging and 
developed markets.
Table 4: DCC-GARCH Estimation
Parameter Coefficient Std. Error z-Statistic Prob.
a (shock effect) 0.0142 0.0039 3.641 0.0003
b (persistence) 0.9571 0.0064 149.55 0.0000
The DCC-GARCH estimation results in Table 
4 offered valuable insights into the dynamic conditional 
correlations between financial markets. The DCC 
parameters, denoted as ‘a’ (shock effect) and ‘b’ 
(persistence), capture how correlations evolved over 
time in response to market shocks and past correlation 
levels, respectively. The shock effect parameter (a) was 
estimated and a highly significant, indicating that 
unexpected shocks in one market significantly affect the 
short-term evolution of correlations with others. 
Meanwhile, the persistence parameter (b) was estimated,
with an exceptionally high z-statistic, which was 
statistically significant, showing that past correlations 
had a dominant influence on current correlations. The 
sum of the two parameters was close to 1, suggesting that 
the correlation structure was highly persistent, meaning 
that shocks to correlation decay slowly over time. These 
results implied that financial market interdependencies 
were both responsive to sudden shocks and exhibited 
long-term stability, making the DCC-GARCH model 
highly effective for modeling time-varying correlations, 
especially in the context of contagion, integration, and 
risk transmission studies across global equity markets.
5.5 Time-Varying Correlation Analysis
This upward surge in correlation during the 
crisis confirms financial contagion, as the increase 
significantly exceeds the average interdependence 
observed in stable periods.
Table 5: Time-Varying pairwise Correlation Analysis (DCC Mean Values)
Pair Pre-Crisis COVID-19 Crisis Post-Crisis
India – USA 0.32 0.78 0.50
Brazil – Germany 0.28 0.73 0.48
South Africa – UK 0.30 0.70 0.46
Indonesia – Japan 0.25 0.68 0.42
Across all country pairs, a significant surge in 
correlation was observed (Table 5) during the crisis 
period, reinforcing the argument for contagion. Postcrisis values remained elevated compared to pre-crisis 
levels, suggesting partial structural transmission or 
persistent interdependence. All market pairs showed 
evidence of contagion during the COVID-19 crisis, with 
correlations increasing significantly. Brazil–Germany
and South Africa–UK also exhibited substantial shifts, 
confirming global financial interconnectivity. Even in 
the post-crisis phase, correlations remained higher than 
pre-crisis, implying ongoing integration or shared 
economic/global investor sentiment.
The sharp increase in correlation across all 
emerging-developed pairs during COVID-19 confirms 
shock transmission. Elevated post-crisis correlations 
suggested partial structural contagion, not just temporary 
sentiment-based co-movement. Risk diversification 
using emerging markets might be less effective during 
global financial turmoil.
5.6 Wavelet Coherence Analysis
Wavelet coherence (WTC) is a powerful tool 
that examines both the time and frequency domain of comovement between two time series especially useful in 
finance to identify transient and scale-dependent 
contagion effects. While DCC-GARCH captured the 
time-varying behavior, wavelet coherence helped verify 
correlations across different time-frequency bands. 
Crisis-induced contagion was not only immediate but 
also affected medium-term investor behavior. This 
reinforced the multi-scale nature of contagion, indicating 
deeper financial linkages. In the context of contagion 
analysis between emerging and developed markets, 
WTC revealed that when two markets moved together 
(time-specific events), how their co-movement varies 
across short, medium, and long-term horizons 
(frequencies), and whether contagion was short-lived or 
structurally persistent.
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 476
Table 6: Wavelet Coherence Analysis
Emerging–Developed Pair Coefficient Observations
India – USA 0.76 High coherence at all levels during 2020; unidirectional influence from 
S&P to Sensex
Indonesia – Japan 0.82 Strong coherence in short-term; medium-term effects linked to trade 
spillovers
South Africa – UK 0.21 Less coherence in long-term
Brazil – Germany 0.80 Highest coherence due to deep export-import ties and synchronized 
monetary easing
Wavelet Coherence analysis provided a 
nuanced picture of contagion and co-movement between 
emerging and developed stock markets by quantifying 
both the strength and the timing of dynamic correlations 
across various time scales. For the India–USA pair, the 
average coherence value is 0.76, indicated substantial 
synchronization, especially during the COVID-19 
pandemic in 2020, when coherence was consistently high 
across short-, medium-, and long-term scales. The 
directional arrows from the wavelet plots revealed a 
unidirectional influence from the S&P 500 to the BSE 
Sensex, underscoring the dominance of the U.S. market 
in shaping emerging market behavior during crises. The 
Indonesia–Japan pair recorded the highest coherence 
value at 0.82, driven by short-term co-movements and 
medium-term trade-linked effects, reflecting the close 
production and supply chain relationships between the 
two Asian economies. In contrast, the South Africa–UK
pair displayed a significantly lower average coherence of 
0.21, suggesting weak long-term integration. Coherence 
was associated with global commodity price 
fluctuations, which were critical to South Africa’s 
exports. Lastly, the Brazil–Germany pair showed a 
strong average coherence of 0.80 supported by robust 
export-import relations and synchronized monetary 
policies, especially during major global downturns such 
as the 2020 pandemic. These results suggested that 
financial contagion is not uniform but varied with 
economic interdependence, market openness, and crisis 
periods. High coherence values, particularly during 
turbulent phases, confirmed the existence of contagion, 
while lower values during stable periods pointed toward 
normal market interdependence. Wavelet coherence thus 
served as a valuable methodological tool for 
distinguishing between short-term shocks and structural 
linkages in cross-market relationships.
6. CONCLUSION
The empirical analysis undertaken in this study 
provided strong evidence of dynamic interdependence 
and contagion between emerging and developed stock 
markets, particularly during periods of global financial 
turmoil such as the COVID-19 pandemic and the Russia–
Ukraine conflict. Descriptive statistics revealed the 
presence of non-normality and leptokurtosis in return 
series, validating the need for GARCH-type models. The 
Augmented Dickey-Fuller test confirmed stationarity of 
log returns, justifying their suitability for time series 
modeling. The Univariate GARCH (1,1) results 
demonstrated significant short-term shock effects and 
high volatility persistence across all indices, reinforcing 
the appropriateness of the DCC-GARCH framework. 
The DCC-GARCH estimates revealed statistically 
significant dynamic correlations that increased sharply 
during the crisis period, substantiating the presence of 
contagion. Particularly, mean pairwise correlations rose 
significantly during the COVID-19 crisis and remained 
elevated post-crisis, suggesting that market integration 
has deepened over time, reducing the scope for 
diversification benefits during systemic shocks. 
Complementing these findings, the wavelet coherence 
analysis offered a time-frequency perspective, revealing 
that contagion operates not only in short bursts but also 
manifests over medium- and long-term horizons. Brazil–
Germany and Indonesia–Japan exhibited strong multiscale coherence, driven by economic ties and policy 
synchronization. In contrast, South Africa–UK displayed 
weak long-term co-movement, likely due to less 
structural linkage.
The findings confirmed that financial contagion 
was both time-varying and scale-dependent, influenced 
by global shocks, trade linkages, and investor sentiment. 
This called for dynamic risk management strategies that 
consider temporal and structural dimensions of market 
integration. The study underscored the importance of 
using multi-method approaches like DCC-GARCH and 
wavelet coherence for robust contagion diagnostics in 
global financial markets. Policymakers and investors 
alike must recognize that emerging markets were 
increasingly sensitive to global developments, especially 
during crises.
REFERENCES
• Aloui, R., Aissa, M. S. B., & Nguyen, D. K. (2011). 
Global financial crisis, extreme interdependences, 
and contagion effects: The role of economic 
structure? Journal of Banking & Finance, 35(1), 
130–141.
• Bekaert, G., Ehrmann, M., Fratzscher, M., & Mehl, 
A. (2014). The global crisis and equity market 
contagion. The Journal of Finance, 69(6), 2597–
2649.
• Chiang, T. C., Jeon, B. N., & Li, H. (2007). Dynamic 
correlation analysis of financial contagion: Evidence 
from Asian markets. Journal of International Money 
and Finance, 26(7), 1206–1228.
• Diebold, F. X., & Yilmaz, K. (2014). On the 
network topology of variance decompositions: 
Amit Das & Amalendu Bhunia, Saudi J Bus Manag Stud, Oct, 2025; 10(9): 470-477
© 2025 | Published by Scholars Middle East Publishers, Dubai, United Arab Emirates 477
Measuring the connectedness of financial firms. 
Journal of Econometrics, 182(1), 119–134.
• Forbes, K. J., & Rigobon, R. (2002). No contagion, 
only interdependence: Measuring stock market 
comovements. The Journal of Finance, 57(5), 2223–
2261.
• Kenourgios, D., Samitas, A., & Paltalidis, N. (2011). 
Financial crises and stock market contagion in a 
multivariate time-varying asymmetric framework. 
Journal of International Financial Markets, 
Institutions and Money, 21(1), 92–106.
• Kumar, A., & Padakandla, S. R. (2020). Volatility 
spillovers and dynamic correlations between BRICS 
and developed stock markets. Applied Economics, 
52(6), 605–621.
• Phylaktis, K., & Ravazzolo, F. (2020). Measuring 
financial market contagion. Journal of Empirical 
Finance, 58, 212–228.
• Rua, A., & Nunes, L. C. (2009). International 
comovement of stock market returns: A wavelet 
analysis. Journal of Empirical Finance, 16(4), 632–
639.
• Umar, Z., & Suleman, M. T. (2017). Spillover and 
contagion from oil and stock markets to Gulf 
Cooperation Council stock markets. Economic 
Systems, 41(2), 245–257.
• Zaremba, A., Kizys, R., Aharon, D. Y., & Demir, E. 
(2021). Infected markets: Novel coronavirus, 
government interventions, and stock return volatility 
around the globe. Finance Research Letters, 38, 
101597.