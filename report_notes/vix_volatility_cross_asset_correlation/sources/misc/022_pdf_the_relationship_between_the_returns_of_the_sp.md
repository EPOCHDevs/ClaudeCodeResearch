---
url: http://arno.uvt.nl/show.cgi?fid=153799
title: [PDF] The relationship between the returns of the S&P 500 index and the ...
domain: misc
crawled_at: 2026-02-04T08:07:27.862729+00:00
source: exa_search
author: 
chart_count: 0
image_links:
outbound_links:
---

The relationship between the returns of the S&P 500 
index and the Volatility Index VIX
Master thesis Finance
Name: Mike van Wees 
Snr.: 2031259 
Anr.: 287368 
Subject: Master thesis Finance 
Supervisor: Dr. Rik Frehen
2
Preface
This thesis is a major and important component of my master Finance at Tilburg 
University. In the past period I completed this research with a lot of dedication. This 
results in my thesis: ‘The relationship between the returns of the S&P 500 and the Volatility 
Index VIX'.
I would like to thank my supervisor Dr. Rik Frehen, who guided me through the 
process, and helped me when I had problems during my thesis. During our meetings, the 
valuable tips from you helped me a lot and you helped me to take this thesis to a higher 
level with good results. Furthermore, I would like to thank my family and friends with the 
support throughout the thesis.
I hope you find the thesis an interesting research.
Mike van Wees,
Tilburg, September 28, 2020
3
Abstract
The research question during this thesis is: Is there a relationship between the 
returns of the S&P 500 index and the VIX, and is it possible to set up a profitable trading 
strategy for the S&P 500 index using the VIX? During the study, different models were 
compared to determine whether the VIX might have predictive power. Subsequently, a 
rule of thumb was drawn up based on one of the models. Then, the relationship between 
the value of the VIX and the returns of the S&P 500 index is analysed. Finally, an 
investment strategy based on the VIX is developed. It can be concluded that there is a 
relationship between the value of the VIX and the returns of the S&P 500 index. When the 
VIX is high, the returns from the S&P 500 index are extremely widespread and these 
returns decrease. In addition, the investment strategy tested in the thesis is very 
interesting for investors as this strategy achieves significantly higher returns, compared to 
when the investor always stays in the S&P 500 index. Using this strategy investors can 
profit from the relationship between the VIX and returns of the S&P 500 index.
4
Table of contents
Preface................................................................................................................. 2
Abstract ............................................................................................................... 3
1. Introduction ...................................................................................................... 6
2. Literature Review............................................................................................... 9
2.1 What is the VIX ............................................................................................ 9
2.2 Choice of VIX ............................................................................................... 9
2.2.1 Investor fear gauge ................................................................................. 9
2.2.2 Private information among investors .........................................................10
2.2.3 S&P 500 Index .......................................................................................11
2.3 Exchange market crashes .............................................................................11
2.3.1 Dot-com Bubble .....................................................................................11
2.3.2 Financial crisis........................................................................................12
2.3.3. Coronavirus stock market crash...............................................................12
2.4 Predicting market returns or exchange market downturns.................................13
2.4.1 Volatility and stock market returns ...........................................................13
2.4.2 The VIX and stock market returns ............................................................14
2.4.3 Economic value of predicting volatility and stock market returns...................15
3. Dataset and descriptive statistics ........................................................................17
3.1 sample selection ..........................................................................................17
3.2 Institutional features and datasets .................................................................17
3.2.1 Institutional features S&P 500 ..................................................................17
3.2.2 Data sources and datasets .......................................................................18
3.3 Descriptive statistics.....................................................................................18
4. Empirical model................................................................................................20
4.1 Simple regression model...............................................................................20
4.2 Multivariate regression model........................................................................20
4.3 Rule of thumb .............................................................................................21
4.4 Investment strategy using the VIX.................................................................21
5. Results ............................................................................................................22
5.1 Simple regression model...............................................................................22
5.2 Multivariate regression model........................................................................24
5.3 Choice of the model .....................................................................................28
5.3.1 Adjusted R-Squared of the model .............................................................28
5.3.2 Information criteria.................................................................................28
5.4 Rule of thumb .............................................................................................30
5.5 investment strategy using the VIX .................................................................31
6. Conclusion .......................................................................................................38
5
Bibliography.........................................................................................................41
Appendix I ...........................................................................................................43
Appendix II..........................................................................................................44
6
1. Introduction
During this thesis, it is investigated whether there is a relationship between the 
returns of the S&P 500 index and the value of the volatility index VIX. The S&P 500 index 
is a stock market index that measures the performance of the largest 500 companies, 
which are listed on the stock market in the United states. This index is one of the most 
important equity indices in the world (Wang, 2008). 
The volatility index VIX is measured since 1993 by the Chicago Board Options 
Exchange (CBOE). The VIX is originally designed to measure the market expectations of 
30 day volatility implied by at the money S&P 100 index options. However in 2003 the VIX 
is updated as a result of that the VIX measures market expectations of the near-term 
volatility implied by stock index option prices. The VIX is constructed to be a general 
estimator of the market’s estimate of the S&P 500 volatility over 30 days (Blair, Poon, & 
Taylor, 2001).
In addition to investigating whether there is a relationship between the VIX and the 
returns of the S&P 500 index, the study also investigated whether the VIX has predictive 
power and whether the VIX can be used during the development of an investment strategy.
This leads to the main question of the thesis, which is used as a guideline for the research. 
This main question is as follows:
Is there a relationship between the returns of the S&P 500 index and the VIX, and is it 
possible to set up a profitable trading strategy for the S&P 500 index using the VIX?
According to Whaley (2000) the volatility index VIX is also called the investor fear 
gauge. The VIX measures the implied index volatility of the S&P 500 over 30 days. Since 
the implied volatility is the forward looking volatility, the VIX can be seen as a predictor 
for uncertain times (Shaikh & Padhi, 2015). This confirms Whaley’s (2000) opinion, 
because when the volatility and the VIX increases it is possible that fear among investors 
increases and that is why the VIX is also called the investor fear gauge. This opinion 
indicates that investors see the VIX as a fear meter, this opinion makes the research 
question in this thesis relevant to determine whether there is a relationship between the 
VIX and the returns of the S&P 500 index. By answering this question, it can be determined 
whether the VIX can really be seen as a fear predictor. 
In addition to that is this research question economically relevant on the basis of 
the market on which the VIX is based. The VIX is based on the S&P 500 index, which is 
the largest American equity market. When it can be established on the basis of this thesis 
that there is a relationship between the VIX and the returns of the S&P 500 index, and this 
7
thesis also shows a strategy that ensures that returns can be increased, this is interesting 
for many investors, as many of them invest in the S&P 500.
Various datasets are used during this thesis. These datasets are mainly collected 
through WRDS, data that was not yet available through WRDS is collected through Yahoo 
Finance. The dataset used in the thesis is the value of the VIX between January 1993 and 
May 2020. In addition, the returns of the S&P 500 index are used in this thesis. The dataset
regarding the returns of the S&P 500 index is also from the period January 1993 to May 
2020. These datasets serve as the basis for the empirical model and to answer the research 
question.
The first step in the empirical model is to draw up the simple regression model. This 
model predicts the returns of the S&P 500 index based on the historical returns of the S&P 
500. The historical returns are lagged by one month and in addition also by one day.
Subsequently, the multivariate regression model is drawn up, using this model, returns are 
predicted based on historical returns and the VIX. Historical returns as well as the VIX are 
lagged by one month and also by one day. One of the four models is used for establishing 
the rule of thumb. Before this rule of thumb is drawn up, it is first decided which model 
will be used, based on the adjusted R-squared and information criteria. Ultimately, a rule 
on thumb is drawn up based on the returns, which are predicted using one of the four 
models.
Finally, an investment strategy is described in the empirical model. This strategy is 
based on the VIX. The investment strategy that is tested in the thesis is one based on the 
data from January 1993 to May 2020 of the VIX. The mean of the VIX over this period of 
6,902 observations is 19.38. The standard deviation of the VIX over this period of 6,902 
observations is 8.39. The investment strategy that I want to test in the thesis is to exit the 
market when the VIX is higher than the value of the mean plus one standard deviation.
This means that I will exit the market if the VIX has a value higher than 27.77 (19.38 + 
8.39) and that I enter the market again when the VIX is lower than 27.77. Subsequently, 
the returns between the restricted and unrestricted strategies are compared to analyse 
whether the strategy performs better than if the investor always remains in the market.
The simple regression and multivariate regression model were first created in the 
chapter results to determine which of the models performs best. It can be concluded that 
all values of the adjusted R-squared of the models are very low, since the independent 
variables of all models explains less than a percent of the variation in the dependent 
variable. This also makes sense since the exchange market is unpredictable. When the
exchange market is predictable, it is possible for any individual to predict the market and 
generate big profits.
8
Based on the adjusted R-squared and the information criteria, I concluded that the 
simple regression model performs better than the multivariate regression model. This 
applies to the models that are lagged with one month the models that are lagged with one 
day. The multivariate regression model included the lagged VIX. Based on the choice of 
the model and the data I used, it can be concluded that the VIX does not contribute to 
predicting returns of the S&P 500 index.
Using the returns predicted by means of the simple regression model, I determine 
the following rules regarding investing in the S&P 500 index or exiting the S&P 500 index.
• I will exit the S&P 500 index when the model predicts that the returns will be -12.12 
percent or lower. This means I will exit the market when the predicted return is 
below the mean minus one the standard deviation.
• I will enter the S&P 500 index when the models predicts that return will be 18.26 
or higher. This means that I will enter the market when the predicted return is 
higher than the mean plus one standard deviation. 
When the previously described rules are followed by an investor, this investor exits 
the market 42 times over the past 27 years and enters the market 45 times or buys 
additional assets at that time in over the past 27 years. 
Finally, the investment strategy based on the VIX is tested. I test this second 
strategy since the first strategy was not based on the VIX and I want to set up a profitable 
investment strategy using the VIX. This strategy is tested on the basis of two different 
periods. The entire period that the VIX exists, from January 1993 to May 2020 and the 
period from January 2017 to May 2020. For the period 1993 to 2020 the average daily 
return using the investment rule is 0.07 percent, this daily return is relatively much higher 
than the 0.035 percent if the investor always remains in the market. For the period 1993 
to 2020 the average daily return using the investment rule is 0.057 percent, this daily 
return is relatively much higher than the 0.044 percent if the investor always remains in 
the market. Based on the two outcomes in the different samples, it can be concluded, that 
higher returns can be achieved by means of the investment strategy based on the VIX. In 
comparison with the unrestricted strategy when the investor always remains in the market.
This conclusion is reinforced as the results are also significant. For the period from January 
1993 to May 2020, the significance level is 1 percent and the period January 2017 to May 
2020, the significance level is 5 percent.
The rest of the thesis is organized as follows. Section 2 literature review, section 3 
dataset en descriptive statistics, section 4 empirical model, section 5 results and section 6 
conclusion. 
9
2. Literature Review
In this chapter, the study begins by explaining the main variable of the thesis in 
section 1. Section 2 discusses why the main variable should be used. Moving on with 
section 3, stock market crashes from 1993. The last part of this chapter analyses what is 
already known about predicting stock market yields using historical literature.
2.1 What is the VIX
The objective of this research is to investigate the relationship between the VIX and 
stock market returns. The main variable of the thesis is the VIX. The volatility index VIX is 
measured since 1993 by the Chicago Board Options Exchange (CBOE). The VIX is originally 
designed to measure the market expectations of 30 day volatility implied by at the money 
S&P 100 index options. However in 2003 the VIX is updated as a result of that the VIX 
measures market expectations of the near-term volatility implied by stock index option 
prices. The VIX depends on the prices of a portfolio 30 calendar day S&P 500 calls and puts 
with weights being inversely proportional to the squared acquisition strike price
(Fernandes, Medeiros, & Scharth, 2014). The VIX is an implied volatility index derived from 
put and call options of the S&P 500 index with maturities of 30 days (22 trading days) 
(Becker, Clements, & McClelland, 2009). The VIX is constructed to be a general estimator 
of the market’s estimate of the S&P 500 volatility over 30 days (Blair, Poon, & Taylor, 
2001).
2.2 Choice of VIX
The aim of this research to determine whether there is a relationship between the 
VIX and the returns of the S&P 500 index. It is then analysed whether it is possible to draw 
up a profitable investment strategy using the VIX. The main component which is used in 
this research to set up this strategy is the volatility index VIX. The choice of the VIX is 
based on the value as predictor for investors and in addition the market on which the VIX 
is based, namely the S&P 500 index options. 
2.2.1 Investor fear gauge
According to Whaley (2000) the volatility index VIX is also called the investor fear 
gauge. The VIX measures the implied index volatility of the S&P 500 over 30 days. Since 
the implied volatility is the forward looking volatility, the VIX can be seen as a predictor 
for uncertain times (Shaikh & Padhi, 2015). This confirms Whaley’s (2000) opinion, 
because when the volatility and the VIX increases it is possible that fear among investors 
increases and that is why the VIX is also called the investor fear gauge. This statement is 
supported by Sarwar (2012), his study discovered a strong relation between changes in 
the VIX and daily stock market returns in U.S. Brazil between 1993 and 2007. This study 
also concluded that the VIX responded much more aggressive to negative changes in stock 
10
market returns than that the VIX responds to positive changes in stock market returns. 
This suggests that the VIX is a gauge for of investors fear (Sarwar, 2012). This makes the 
VIX a good predictor of potential market crashes as it measures investor fears and 
confidence.
2.2.2 Private information among investors 
While trading stocks and setting up investment strategies, having information is 
very important. It is easier to predict future outcomes using specific information. Previous 
research concludes that investors who have access to private information executes many 
profitable transactions as a result of the information they have at their disposal (Bushee & 
Goodman, 2007). As discussed earlier, the VIX is derived from call and put options of the 
S&P 500. As a result of that, it is possible for investors to cash in their private information 
as much as possible through options.
Tsai, Chiu & Wang (2015) also conducted research on the value of private 
information related to investing. In the end, they presented evidence regarding the VIX 
index options. They conclude that traders wish to act on the information that they possess 
in the VIX options market. When investors have specific information they are likely to 
choose to sell their shares using limit orders, as opposed to marketable orders (Tsai, Chiu, 
& Wang, 2015). Investors uses limit orders instead of market orders to limit execution 
price uncertainty. In addition to this conclusion, other researchers have investigated 
whether informed options investors predict stock returns. Chang, Hsieh & Lai have 
evidence from the Taiwan stock exchange market. They investigated the influence of 
options on predictability and concluded that the group of informed traders provided the 
largest predictability in the middle horizon options and the near the money options (Chang, 
Hsieh, & Lai, 2009). This makes it easier for this group of investors to predict future returns 
and makes it more likely that this group will make better investment decisions.
Earlier in this chapter it was stated that the VIX is forward looking. As a result of 
that, it is possible to see the VIX as a possible predictor for future returns. This makes this 
variable an interesting variable for investors. It is also possible that investors have private 
information and as a result of that perform various actions. An example is when some of 
the investors have private information indicating that potentially bad economic times are 
approaching. Investors can take advantage of this through options and gain potentially 
high returns. Since the VIX is an implied volatility index derived from put and call options 
of the S&P 500, it is possible that the VIX might change significantly due to private 
information among investors. If so, the VIX is a good estimator for future returns. This 
makes this research whether the VIX and the returns of the S&P 500 index have a 
relationship economically interesting for many investors and companies. In addition, it is 
11
also economically interesting to investigate whether the VIX can be used to set up an 
investment strategy.
2.2.3 S&P 500 Index
Besides that the VIX is a good predictor according to investors, the market on which 
the VIX is based, is also very interesting. The VIX is based on the S&P 500 market index. 
The S&P 500 index is a stock market index that measures the performance of the largest 
500 companies, which are listed on the stock market in the United states. This index is one 
of the most important equity indices in the world and many investors and companies 
consider this index as one of the best representations of the stock markets in the United 
States (Wang, 2008). 
The importance of the S&P 500 makes it economically interesting to use the VIX as 
the main variable in this study, as many investors are using the S&P 500 as a key index in 
the US equity markets. During this thesis, the predictive value of the VIX is analysed. What 
the VIX is and why the VIX is chosen was described in the previous section on the basis of 
papers.
2.3 Exchange market crashes
During this thesis it is investigated whether there is a relationship between the VIX 
and exchange market crashes. Since the VIX exists since 1993, there is only data available 
from this date. As a result of that, research in this thesis will be conducted from 1993. As 
of 1993, there have been three major stock U.S. market crashes. These were the dot-com 
bubble in 2000 and the Financial crisis in 2008 (Barro & Ursuá, 2017). The third market 
crash was the coronavirus stock market crash in 2020.
2.3.1 Dot-com Bubble
In the late 1990s, the internet became more accessible to more people around the 
world. During that period, investors focused on these internet based companies. As a result
of that, the value of companies in the internet sector rose sharply. In addition, many new 
companies were started up and went public during this period. In 1999, 446 internet based 
start-ups went public and they gain an average return of 70 percent on the first day. The 
degree of investment in internet based companies and the desire to grow internet startups quickly lead to the highest ranking of the NASDAQ ever. On March 10, 2000 the 
NASDAQ peaked at 5048.62. This was the highest value of the NASDAQ during the Dotcom Bubble (Goonight & Green, 2010).
On March 13, the NASDAQ opens 4.5% lower. Analysts view this lower opening as 
a market correction, however the NASDAQ's decline continued. During April 2020 the 
internet index lost 19 percent of its value. The market value of internet companies declined 
12
form €1 trillion in March 2000 to only €572 billion in December 2000. The NASDAQ also 
collapsed in 2000 as a result of the Dot-com Bubble. At the end of 2000, NASDAQ recorded 
2470.52, which is a decrease of 52 percent from March 2000 (Goonight & Green, 2010). 
When the bubble burst in 2000, it caused a global recession that was unexpectedly 
protracted in some Western countries.
2.3.2 Financial crisis
The Financial crisis can be divided into two phases. The first phase runs from August 
2007 to August 2008, this limited phase stemmed from losses in one relatively small 
segment in the U.S. financial system, namely subprime mortgages. Despite this disruption 
to financial markets, caused by the subprime mortgages, the real GDP in the United States 
continued to rise into the second quarter of 2008 and analysts only predicted a small 
recession (Mishkin, 2011). 
The second phase is the global financial crisis. The bankruptcy of Lehman Brothers 
on Monday, 15th of September is considered as the start of the global financial crisis. Since 
the bankruptcy of Lehman Brothers, much uncertainty has arisen among investors. This 
financial crisis led to a worldwide recession (Mishkin, 2011). The crisis peaked in October 
2008 and ended in 2011. From 2010, the main concerns shifted from the housing market 
crisis to the worrisome financial positions of governments, for example Greece (D.Gibson, 
G.Hall, & S.Tavlas, 2012). 
2.3.3. Coronavirus stock market crash 
The most recent crisis is the stock market crash of 2020. With regard to this crisis, 
the Coronavirus appears to be the black swan. The Coronavirus has led to major losses 
among investors around the whole world. Large indexes lost about 10 percent of their 
value on March 9, 2020. The largest stock market declines since September 9, 2001 have 
occurred on this day. The losses on March 9, 2020 even exceed the losses in 2008 during 
the financial crisis due to the bankruptcy of Lehman Brothers (Daube, 2020 (working 
paper)). In addition to the Corona crisis, there is another aspect that contributed to stock 
market crash. This aspect was the oil war between Saudi Arabia and Russia. These two 
factors lead to the stock market crash in March 2020 and subsequent high unemployment 
in the United States. 
Since the data that is being investigated is only available from 1993, the analysis 
in this thesis is done from this period. The three events have been named and described 
to indicate the impact on the stock market when a crash occurs. In addition, these events 
have also been described in order to gain insight into when data relating to the VIX must 
strongly change from the average value.
13
2.4 Predicting market returns or exchange market downturns
During this part of the literature review, it is analysed which important information 
with regard to predicting returns in the past has already been collected. Firstly, the 
relationship between volatility and stock market returns is analysed. Thereafter it is 
examined what is already known in the literature about the VIX as a predictor of stock 
market returns. Finally, the economic value of predicting stock market returns and volatility 
is discussed. 
2.4.1 Volatility and stock market returns
In the past, a lot of research has been done into the relationship between volatility 
and stock market returns. French & Schwert (1987) analysed a possible relationship 
between stock returns and the stock market volatility. They concluded that they found 
evidence for a positive relationship between the market risk premium and the predictability 
of the volatility of stock returns. In addition, French & Schwert (1987) also found evidence 
for a negative relationship between unexpected stock market returns and unexpected 
changes in the volatility of stock market returns. They considered this as indirect evidence 
for a positive relationship between expected risk premiums of stock and the volatility of 
these stocks. 
Baillie & DeGennaro (1990) stated that most asset pricing models also suggest a 
positive relation between portfolio’s expected returns and risk. This risk is often measured 
using the variance. This makes sense since the investor requires reward for the risk 
incurred. However, Baillie & DeGennaro (1990) concluded after estimating a variety of 
models from daily and monthly return that the relationship between mean returns and 
standard deviation is weak. As a result of their results Baillie & DeGennaro ( 1990) suggests 
that investors consider other risk measures instead of the variance of standard deviation 
during their investment decisions.
Following on from the above paragraph, Guo & Savickas conducted further research 
and have additional information from previous research into volatility and stock market 
returns. Guo & Savickas (2012) find that the idiosyncratic stock volatility and the aggregate 
stock market volatility together exhibit a strong predictive power for stock return markets. 
Guo & Savickas (2012) also concluded that a high level of idiosyncratic volatility is usually 
associated with low expected future stock returns. The combination between risk and 
return is positive as mentioned earlier, however idiosyncratic volatility is negative related 
to stock market returns (Guo & Savickas, 2012). 
Ang et al. (2009) have also researched the relationship between idiosyncratic 
volatility and future returns. The results of this research reinforce the results of the 
conclusion mentioned earlier. Ang et al (2009) conducted research based on 23 developed 
14
countries and concluded that stocks with recent past high idiosyncratic volatility have low 
future average returns around these 23 countries. In addition, this conclusion is significant 
in the G7 countries (Ang et al. , 2009). This conclusion is logical, since in finance 
idiosyncratic risk is seen as a diversifiable risk. As a result of that, investors are not 
compensated for idiosyncratic risk.
The literature mentioned earlier refers to the relationship between stock market 
returns and volatility. Important research has been conducted in the past into this 
relationship between volatility and stock market returns. During my thesis I will compare 
the relationship between the VIX and stock market returns, this is also a known relationship 
but based on the VIX. This thesis extends research between volatility and returns as the 
VIX is also volatility but of the entire S&P 500 index.
2.4.2 The VIX and stock market returns
As mentioned earlier in the literature review, the VIX is also used as a predictor for 
stock market returns. The VIX is known as a investors fear index. This VIX is the riskneutral expected stock market variance for the U.S. S&P 500 options, the VIX is calculated 
using implied volatility from the options of the S&P 500 index (Whaley, 2000). Previous 
research also supports to use implied volatility and VIX as predictor instead of for example 
historical volatility.
Szakmary et al. (2003) conducted research into the predictive power of implied 
volatility. During the research, they involved many different futures markets in the 
research. Thirty five futures were analysed in the study, including the S&P 500 index, which 
is the VIX. Szakmary et al (2003) concluded that implied volatility is a better predictor of 
realized volatility compared to historical volatility. Since in the majority of futures markets, 
the prediction of the implied volatility of the realized volatility was better than the historical 
volatility. 
Szakmary et. Al (2003) concluded that implied volatility was a good predictor of 
realized volatility based on thirty five different futures markets. One of these thirty five 
futures markets was the S&P 500. Ederington & Guan (2002) have also researched the
implied volatility as a predictor. During their analyses they decided to use only data from 
the S&P 500 index options. Based on this data, Ederington & Guan wanted to find out 
whether the implied volatility is an efficient and effective predictor of future volatility. 
Ederington & Guan (2002) concluded that the implied volatility has a strong 
predictive power. They also concluded that prediction results and efficiency results are 
sensitive to the forecasted horizon and when the data covers a stock market crash, for 
example the stock market crash of 1987 (Ederington & Guan, 2002). This conclusion 
15
confirms that the implied volatility of the S&P 500 index options is a good predictor of 
realized volatility.
Bekaert & Hoerova (2014) re-examined and further expand the predictive power of 
the volatility index VIX. Unlike to other researchers, Bekaert & Hoerova first decomposed 
the squared VIX into two components: the conditional variance of the stock market and 
the equity premium variance. The equity variance premium is the difference between the 
squared VIX and the conditional variance of the stock market (Variance premium = squared 
VIX – conditional variance of the stock market). Eventually Bekaert & Hoerova concluded 
that the variance premium is a significant predictor of future returns. In addition, they 
conclude that the conditional variance of the stock market predicts negative economic 
activity and that the conditional variance of stock markets has a high predictive power of 
financial instability (Bekaert & Hoerova, 2014).
Despite the fact that many papers mention the predictive power of the VIX and 
implied volatility, there are also papers with doubt about the VIX as a predictor for returns 
and realized volatility. Kownastki (2016) questioned how good the VIX is as a predictor for 
market risk. Kownastki (2016) concluded that during the most critical time periods, for 
example the Financial crisis in 2008, the VIX does not perform as promised. He concluded 
that the VIX understates realized volatility by about 180 basis points on average. He also 
concluded that poor timing increases possible forecast errors in the future (Kownatzki, 
2016).
Based on this literature review, I still think that the VIX will be the best main variable 
during my research. Since the VIX is generally regarded as one of the best predictors by 
investors. in addition, several papers and researchers have confirmed this assumption in 
the literature review above. The literature described above also provides a good basis for 
my thesis. Several papers show that the VIX has a predictive power for stock market 
returns, I will test this hypothesis in the rest of the thesis.
2.4.3 Economic value of predicting volatility and stock market returns
Forecasting market returns and volatility is economically interesting for investors, 
using this forecasts, investors can make profits and avoid losses. Investors can use 
different strategies while investing. 
Marqueing & Verbeek (2004) analysed the economic value of predicting stock 
returns and volatility. They examine several investment strategies, using data from 1970 
until 2001. They conclude that for a mean-variance investor, predicting volatility is 
profitable, even if transaction costs are very high and short sales are not allowed during 
the investment strategies. 
16
During the research in my thesis, it is tested whether there is a relationship between 
the VIX and returns of the S&P 500 index. Furthermore it is tested whether the VIX has 
predictive power of predcting of returns of the S&P 500 index. This is economically
interesting for many investors since the VIX is based on the S&P 500, which is one of the 
most important stock exchange markets in the world. In addition, many investors see the 
VIX as a fear gauge and as a result of that they use the VIX during their investment 
decisions. 
17
3. Dataset and descriptive statistics
Chapter 3 is divided into three different sections. The first paragraph explains the 
sample selection. The second paragraph describes the institutional features of the market
in addition, the data sources are listed, including the datasets used in this thesis. Finally, 
the descriptive statistics are presented in the last paragraph.
3.1 sample selection
Before this study describes the relationship between the VIX and the returns of the 
S&P 500 index, a brief summary of the institutional setting is helpful to put things into 
perspective. In order to compare the performance of stock markets with the VIX, the data 
regarding the S&P 500 is being used in this thesis. The choice to make the comparison of 
the VIX as a predictor using data from the S&P 500 is economically interesting, since the 
S&P 500 consists of the largest publicly traded companies within the United States.
The data which is used in this thesis is extracted for the time period 1993 until May 
2020. During this period three major financial events occurred. These events had major 
influence on the VIX and stock markets around the world. These three events were: The 
Dot-com Bubble in the late 1990s, the Financial Crisis in 2007 and 2008 and the 
Coronavirus stock market crash in 2020.
The data will be investigated from 1993, because the VIX is only available from this 
period (Whaley, 2000). In addition, it is decided to investigate the data up to and including 
May 2020, so that the performance of the VIX during the Coronavirus crisis in March 2020 
can be included in the investigation. The starting sample consists of 6,902 observations in 
the period 1993 until May 2020. 
3.2 Institutional features and datasets
The institutional details of the S&P 500 are provided during this section of the 
chapter. The chapter also identifies the data sources and datasets, which are used during 
the analysis.
3.2.1 Institutional features S&P 500
The S&P 500 index is a market-capitalization weighted index consisting of the 500 
largest publicly traded companies in the United States. The S&P 500 index is also called 
Standard & poor’s 500 index. The index is considered the most important United States
equity index worldwide, because this index represents the largest publicly traded 
corporations in the United States (Wang, 2008). 
18
The S&P 500 consists of the 500 largest publicly traded companies in the United 
States. Only the top 10 largest companies are listed on the Standard & Poor website. Many 
of the top 10 companies are technology companies or financial companies. For example, 
Microsoft, Apple, Facebook and JP Morgan Chase & Co. Investors prefer the S&P 500 to 
other US indices because this index has more stocks than, for example, the Dow Jones 
Industrial Average (500 versus 30).
3.2.2 Data sources and datasets
I use two different data sources to collect the data for my research. I use Wharton 
Research Data Service (WRDS) to get most of my datasets, namely the data from 1993 to 
2019. WRDS provides leading business intelligence, research platform, and data analytics 
to global institutions, historical analysis and insight into the latest innovations in research 
(WRDS, 2020). Since I also want to include the impact of the coronavirus crisis during my 
analysis, I decided to also collect data from January 2020 to May 2020. This data is
collected through Yahoo Finance and added to the data collected through WRDS. Yahoo 
Finance provides free stock quotes, up-to-date news, portfolio management, and 
international market data (Yahoo Finance, 2020)
During my analysis I use three different datasets. The first dataset is called CBOE 
S&P 500 Volatility Index (VIX) and consists of data from January 1993 through May 2020. 
The second dataset is called S&P 500 index daily return and also consists of data from 
January 1993 to May 2020. Finally, the third dataset is a combination of the two previously 
mentioned datasets. 
3.3 Descriptive statistics
The sample consists of 6,902 observations of the two different variables. The data 
refers to daily data of trading days on the US stock exchange market from January 1993 
through May 2020. As previously reported, the datasets are obtained through WRDS and 
are merged into a dataset that will be used during the analysis. 
Looking at the main variable in this thesis which is the VIX, the mean is 19.38.
Furthermore, the minimum value of the VIX 9.14 and the maximum value of the VIX 82.69. 
This maximum value is a major outlier when the mean is compared to the standard 
deviation, which indicates that the maximum values of the VIX are more extreme than the 
minimum values of the VIX. These high values mainly occur during uncertain times on the 
stock market.
The other variable, daily return of the S&P 500 in percentages, is collected to 
determine the value of the VIX using investing in the S&P 500 index. From 1993 the 
average daily return of the S&P 500 index is 0.035%. It is true that there might be large 
outliers of daily returns, which are from the minimum and maximum value. By means of 
19
this data, I try to determine an investment strategy using the VIX, which outperforms a 
strategy when the investor always remain in the market. The performance of this strategy 
is compared on the basis of the returns of the restricted and unrestricted strategy. 
Figure 1: Summary statistics 
The summary statistics regarding the data from January 1993 until May 2020 are shown in the table below. The 
variables are Volatility Index VIX and the daily return of the S&P 500 index.
Variable Obs Mean Std. Dev. Min Max
VIX 6,902 19.377 8.394 9.14 82.69
DailyReturn 6,902 0.00035 .012 -.12 .116
20
4. Empirical model
In this chapter of the thesis, the empirical models used during the analysis are 
described. In addition to the empirical models, the estimators are also described during 
this part of the thesis. First, the simple regression model is described and elaborated. One
variable is then added to this simple regression model to test whether it helps predicting
the value of this added variable. Thereafter, a rule of the thumb is added to the analysis 
and the rule of thumb is further explained during this part of the thesis. Finally, an 
investment strategy based on the VIX is tested during the analysis. 
4.1 Simple regression model
During the analysis of the thesis, I predict the value of the VIX by comparing two 
different models. One model excluding the lagged VIX and another model including the 
lagged VIX. To determine the predictive power of the VIX, a reference point must first be 
drawn up for comparison. This reference point is an estimation of the returns on the S&P 
500 index (𝑅𝑚t) based on the historical returns on the S&P 500 index (𝑅𝑚t-1). To estimate
returns based on historical returns, historical returns are regressed on t+1. The term used 
for the lag t+1 is one month. In addition, a model is also regressed based on a one day 
lag. This leads to the following simple regression model:
𝑅𝑚t = β0 + β1 * 𝑅𝑚t-1 + ut (I)
4.2 Multivariate regression model
After using the simple regression model as a reference point, the multivariate 
regression model is created. This model consists of the simple regression model as 
mentioned earlier, with a new variable added, namely the VIX. The lagged VIX is added to 
the model to assess whether the VIX has predictive power for the S&P 500's returns. The 
term used for the lag t+1 of the VIX is also one month. In addition, a model is also 
regressed based on a one day lag. This leads to the following multivariate regression 
model:
𝑅𝑚t = β0 + β1 * 𝑅𝑚t-1 + β2 * VIXt-1 + ut (II)
Ultimately, this model is used to analyse whether the VIX has predictive power 
regarding the returns of the S&P 500. To analyse whether the VIX has predictive power, 
the adjusted R-squared of the simple regression model and multiple regression model are 
compared. In addition, is it also possible to look at the loading of the coefficient of the VIX
and it is also possible to use the information criteria in Stata to select the best model in 
Stata. When the coefficient of the VIX is relatively high, this coefficient contributes more 
to predicting returns in comparison when the loading on the coefficient is low. 
21
4.3 Rule of thumb
During the analysis of the thesis, a rule of thumb is drawn up based on one of the 
four models. Before the rule is drawn up, a choice must first be made between the simple 
regression models and the multivariate regression models. The model which will be chosen 
is more valuable as a predictor of the returns of the S&P 500 index in comparison with the 
other models.
The choice of model is based on two different aspects. This concerns the adjusted 
R-squared per model and the information criteria. Based on these aspects it is decided 
which model is used during the rule of thumb. 
Subsequently, the values are calculated in Excel by using one of the models. These 
values are then plotted for the graphical display. Finally, a rule is drawn up. Based on the 
values, which are known by the model, this rule indicates moments when to enter and 
invest in the S&P 500 index, as well as times to exit and sell the investments.
4.4 Investment strategy using the VIX
After testing the predictive power of VIX using the four different models, the VIX is 
used to test an investment strategy, which is based on the value of the VIX. Before the 
investment strategy is tested, a scatter plot of the value of the VIX and the returns of the 
S&P 500 index is added. This scatter plot indicates whether there might be a relationship 
between the VIX and the performance of the returns of the S&P 500 index. In addition, a 
regression is also added which predicts returns based on the lagged VIX.
The investment strategy that is tested in the thesis is one based on the data from 
January 1993 to May 2020 of the VIX. The mean of the VIX over this period of 6,902 
observations is 19.38 (see Figure 1: Summary statistics). The standard deviation of the 
VIX over this period of 6,902 observations is 8.39 (see Figure 1: Summary statistics). The 
investment strategy which I want to test in the thesis is to get out of the market when the 
VIX is higher than the value of the mean plus one standard deviation. This means that I 
will exit the market if the VIX has a value higher than 27.77 (19.38 + 8.39) and that I will 
return and enter the market again when the VIX is lower than 27.77. 
The next step is to compare the returns of the restricted strategy and the 
unrestricted strategy. During this step, the returns for the restricted strategy and the 
unrestricted strategy are first calculated. Subsequently, the average returns of both 
strategies is calculated. Based on these average returns I conclude whether the strategy 
based on the VIX achieve better results than if the investor always stays in the market.
Finally, the results are tested whether they are significant.
22
5. Results
During this part of thesis, the analysis is performed and the results are analysed. 
First, the simple regression models are created. Then the multivariate regression models 
are created. Thereafter, this chapter of the thesis explains the rule of the thumb, this rule 
of thumb is based on a the simple regression model or on a multivariate regression model. 
The choice of the model is based on the predictive power and the use in practice. Finally, 
an investment strategy based on the VIX is performed and tested.
5.1 Simple regression model
During the thesis four different models are compared, this concerns two simple 
regression models and two multivariate regression models. First, the simple regression 
model is described and interpreted. Using the simple regression model, returns of the S&P 
500 index are predicted based on lagged historical returns of the S&P 500 index. This leads 
to the following simple regression model:
𝑅𝑚t = β0 + β1 * 𝑅𝑚t-1 + ut (I)
𝑅𝑚t-1 are the historical returns of the S&P 500 index lagged by 1 month. By means 
of Stata the daily data was first adjusted to monthly data. Subsequently, these monthly 
data were lagged with 1 month using Stata. The lagged historical returns of the S&P 500 
index are chosen as estimator to provide a reference point to compare with the multivariate 
regression model in which the lagged VIX is included.
Based on the lagged historical returns of the S&P 500 index, the table (see Figure 
2) below is generated in Stata by predicting the returns of the S&P 500 index based on the 
one month lagged returns of the S&P 500 index.
Figure 2: Simple regression model based on historical returns lagged with one 
month
(1)
VARIABLES Rmt
Rm_Lagged 0.03603
(0.065)
Constant 0.00659***
(2.79)
Observations 328
Adjusted Rsquared- 0.0018
This table shows the result of one regression from the period May 1993 until January 2020. The dependent 
variable is return of the market (S&P 500 index) and the independent variable is the one month lag of return of 
the market (S&P 500 index). The numbers in the parentheses are the t-statistics. *, **, *** indicates the 
significance levels of 0.10, 0.05 and 0.01. 
23
Based on the table in figure 2 it is possible to make two different interpretations:
• 1 Percentage point increase in the monthly lagged return of the S&P 500 index 
results in an expected increase of 3.603 percentage points in the return of the S&P 
500 index.
• If the lagged returns of the S&P 500 index is zero, expected return of the S&P 500 
index is 0.659 percentage point.
β1 is not statistically significant since the t-statistic is 0.65. This means that it is not 
possible to conclude that this coefficient is statistically significant even at 10 percent. The 
constant factor is statistically significant at 1 percent, since the t-statistic is 2.79. This 
means that the coefficient is statistically significant at 1 percent.
The adjusted R-squared of the simple regression model in figure 2 is –0.0018 which 
is even negative, this indicates the variation in the model is not much explained by the 
model. This makes sense as the stock market is unpredictable. When the market is 
predictable, it is possible for any individual to predict the market and generate big profits.
As mentioned earlier, the model is regressed based on historical returns lagged with
one month. I also decide to regress the regression model bases on historical returns with 
a lag of one day to determine which form of lag allows the model to perform best. The 
results of this regression are shown in the table below (see figure 3).
Figure 3: Simple regression model based on historical returns lagged with one 
day
(1)
VA