---
url: https://www.wu.ac.at/fileadmin/wu/d/ri/isk/VSFX_2021/Papers/20230910_Commodity_Prices_and_Currencies_Jeanneret_Sokolovski_SSRNlink.pdf
title: [PDF] Commodity Prices and Currencies
domain: misc
crawled_at: 2026-02-04T01:09:23.132398+00:00
source: exa_search
chart_count: 0
image_links:
outbound_links:
---

Commodity Prices and Currencies*
Alexandre Jeanneret
UNSW Business School
Valeri Sokolovski
University of Alberta
September 10, 2023
Abstract
We introduce an empirical approach to identify commodity currencies as those with signi-
cant commodity price exposure. This categorization aligns with the importance of a country's
commodity sector across multiple dimensions. Studying these currencies, we nd that monthly
changes in a country's commodity export prices predict its exchange rate, especially when uncertainty is high. This predictability extends to the carry trade and is driven exclusively by
investments in commodity-exposed currencies. These results hold out-of-sample, surpassing the
random walk benchmark, particularly for emerging currencies. We explain our ndings using a
model incorporating heterogeneous beliefs among agents regarding the informativeness of news.
Keywords: Exchange rates, commodities, predictability, carry trade, FX volatility.
JEL codes: C32, F31, G15.
*We are grateful for comments and suggestions from Patrick Augustin, Geert Bekaert, Philippe Cote, Pasquale
Della Corte, Christian Dorion, Mathieu Fournier, Mark Huson, Òscar Jordá, Richard Levich, Lubos Pástor, Ella Patelli, 
Steven Riddiough (discussant), Nick Roussanov, Ivan Shaliastovich (discussant), Kirsten Smart, Elvira Sojli, Fabricius
Somogyi, Simon Van Norden, Pascale Valery, Adrien Verdelhan, Robert Vigfusson (discussant), Colin Ward, Masahiro
Watanabe, and seminar participants at the 2019 JPMCC International Symposium, Fulcrum Asset Management,
2023 Frontiers in Finance Conference, 2021 Vienna Symposium on Foreign Exchange Markets, 2021 FIRN, and HEC
Montréal. Alexandre Jeanneret (corresponding author) is with the School of Banking and Finance, UNSW Business
School. Email: a.jeanneret@unsw.edu.au. Website: www.alexandrejeanneret.net. Valeri Sokolovski is with the Alberta
Business School, University of Alberta. E-mail: vsokolov@ualberta.ca; Website: www.valerisokolovski.com.
Electronic copy available at: https://ssrn.com/abstract=4564504
Commodity Prices and Currencies
Abstract
We introduce an empirical approach to identify commodity currencies as those with signi-
cant commodity price exposure. This categorization aligns with the importance of a country's
commodity sector across multiple dimensions. Studying these currencies, we nd that monthly
changes in a country's commodity export prices predict its exchange rate, especially when uncertainty is high. This predictability extends to the carry trade and is driven exclusively by
investments in commodity-exposed currencies. These results hold out-of-sample, surpassing the
random walk benchmark, particularly for emerging currencies. We explain our ndings using a
model incorporating heterogeneous beliefs among agents regarding the informativeness of news.
Keywords: Carry trade, exchange rates, commodities, FX volatility, predictability.
JEL codes: C32, F31, G15.
Electronic copy available at: https://ssrn.com/abstract=4564504
1 Introduction
The exchange rate is arguably the most important price in an open economy. Yet the literature has often struggled to empirically connect exchange rates with economic fundamentals. This phenomenon
is broadly known as the exchange rate disconnect, and it remains one of the most persistent puzzles
in international nance (Obstfeld and Rogo, 2000; Itskhoki and Mukhin, 2021). In the short term,
exchange rate moves are hard to explain and even harder to predict (Meese and Rogo, 1983). In
this paper, we reexamine short-term exchange rate predictability by focusing on a distinct set of
currencies for which the link between exchange rates and fundamentals is empirically strong and
theoretically unambiguous: the commodity currencies.1
To illustrate this connection, Figure 1 shows how the Norwegian krone (NOK) and the Russian
ruble (RUB) perform in relation to the price of oil (their main commodity export). Despite the NOK
being a developed G10 currency and the RUB an emerging currency, both exchange rates closely
track the oil price over the long term (2004-2020) as well as around exogenous short-term shocks
to oil prices, like during the Russia-Saudi Arabia oil price war.2In contrast, it is dicult to think of
another variable that would be as closely related to, for example, the Swiss franc or the Japanese
yen. The primary reason for this tight link is that commodities play a vital role in multiple sectors of
these economies, naturally driving their exchange rates.3
Figure 1 [about here]
Although commodity prices signicantly inuence these exchange rates, participants in the foreign
exchange (FX) market are strongly heterogeneous, face asymmetric information, and are likely to
trade for a variety of idiosyncratic reasons (Ranaldo and Somogyi, 2021). Their trades could stem
from shifts in other fundamentals, monetary policies, market sentiment, corporate decisions, or even
noise. Consequently, it is reasonable to expect that uctuations in commodity prices would only
be gradually incorporated into the exchange rates of commodity-producing countries. This gradual
information diusion may result in short-term predictability for these countries' exchange rates,
especially for the less frequently traded currencies.
1
Commodity currencies are typically dened as currencies of countries in which primary commodities constitute a
signicant share of production and exports (we provide our formal denition later in the paper). Chen and Rogo (2003)
introduced this term in their paper titled Commodity Currencies, nding that commodity prices strongly inuence the
real exchange rates of Australia, Canada, and New Zealand.
2This conict stemmed from a breakdown in negotiations between the Organization of the Petroleum Exporting
Countries (OPEC) and Russia over proposed oil production cuts amid the COVID-19 crisis. On 8 March 2020, Saudi
Arabia unexpectedly announced discounts of $6 to $8 per barrel to international customers. This announcement led to
a 30% drop in oil prices and a depreciation of the NOK and the RUB. On 2 April 2020, US President Trump threatened
to withdraw military support unless OPEC and its allies reduced production. Oil prices surged by about 25% that day,
and both currencies subsequently appreciated.
3For example, commodity exports constitute 67% of Norway and Russia's exports; commodity-related revenue
accounts for 19% and 33% of their total scal revenue, respectively; and commodity-linked companies constitute 47%
and 69% of their total stock market capitalization, respectively.
1
Electronic copy available at: https://ssrn.com/abstract=4564504
Commodity producers' currencies are interesting for another critical reason. These currencies
typically oer high-interest rates (Ready, Roussanov, and Ward, 2017), and thus tend to play a
crucial role in the currency carry trade - a highly popular FX strategy involving borrowing in lowinterest rate countries and investing in high-interest rate countries. The protability of this strategy
has puzzled nancial researchers and spawned an extensive literature (see, e.g., Daniel, Hodrick, and
Lu, 2017). While substantial progress has been made to explain unconditional carry trade returns
and the cross-sectional dierences in currency returns (see Hassan and Zhang (2021) for a survey),
there has been limited exploration of carry trade predictability to date.
This paper makes four key contributions to the FX literature. First, we develop a simple model
showing how changes in commodity prices could impact the contemporaneous and future exchange
rates of commodity-exporting countries, especially in times of elevated uncertainty. Second, we
introduce a new empirical approach to identifying currencies with signicant exposure to their countries' exported commodities. Third, we exploit changes in country-level commodity export prices to
provide evidence of unconditional and conditional exchange rate predictability for commodity currencies, both in and out-of-sample. Fourth, we show that commodity price uctuations are valuable for
predicting the performance the carry trade, but that this predictability is driven exclusively by a small
set of less-traded commodity currencies, mostly from emerging markets. This evidence of currency
predictability has signicant implications for investment and policy decisions, which depend highly on
the ability to forecast exchange rates.
We start with a motivating, information-based model to study predictability in the FX market.
Building on existing models that consider dierences of opinion among traders, we explore how new
information could drive exchange rate predictability in an economy with heterogenous agents.4 We
nd that, when there is disagreement about the informativeness of public news (e.g., commodity
price movements), agents trade based on their diering beliefs. Consequently, this news is only
gradually incorporated into exchange rates, resulting in short-term predictability. The model's key
insight is that variations in commodity prices (i.e., fundamental shocks for commodity producers)
aect both current and future exchange rate changes. This information-based model provides key
predictions about short-term exchange rate dynamics, complementing the macro-nance literature
on currency risk premiums.
Guided by these theoretical insights, we empirically investigate the role of commodity export prices
in exchange rate predictability. We start by identifying a set of commodity-exposed currencies, using
a sample of 41 (developed and emerging market) currencies and country-specic commodity export
price indexes spanning from January 1985 to April 2020.5 Thus far, the denition of a commodity
currency in existing literature has often lacked consistency, with studies frequently analyzing small
4Related models with heterogenous investors include Bacchetta and Van Wincoop (2006) and Cespa, Gargano,
Riddiough, and Sarno (2022).
5The country-specic commodity export price indexes are constructed as the export-weighted changes in international market prices of up to 45 individual commodities. The weights are time-varying to ensure that changes in the
price indexes reect variations in the relevant commodity prices for each country at any given point in time.
2
Electronic copy available at: https://ssrn.com/abstract=4564504
sets of reasonable but arbitrarily chosen candidates from major commodity producers (e.g., Chen
and Rogo, 2003; Chen, Rogo, and Rossi, 2010; Ferraro, Rogo, and Rossi, 2015; Ready et al.,
2017). In contrast, we propose a formal denition of a commodity currency as a country's currency
with a positive and statistically signicant covariance (beta) with its commodity export prices. In
other words, a currency that, on average, tends to appreciate when commodity export prices rise
and depreciate when they fall.
Upon examining our sample of 41 currencies, we nd nine countries whose currencies display a
positive and statistically signicant commodity price beta: Australia, Brazil, Canada, Mexico, New
Zealand, Norway, Peru, Russia, and South Africa. We show that our market-based categorization
helps capture the importance of a country's commodity sector across multiple dimensions, including
exports, GDP, nancial markets, and scal revenue. And it does so using a single measure. In
contrast, none of these economic measures alone are sucient for adequate identication of the
commodity currencies. For instance, while Colombia has the highest share of commodity exports
(68%) in our sample, it does not display a statistically or economically signicant commodity price
beta once we account for the US dollar eect.6In comparison, Mexico displays a strongly signicant
commodity price beta, yet commodities reect a relatively modest fraction of its total exports (18%).
However, commodity-related revenue constitutes a substantial portion of Mexico's government's
income: 55% in 2007 and 28% in 2017 (OECD, 2020). We thus oer the rst formal identication
of commodity currencies, which can dier from those of the largest commodity exporters.
Next, we examine how variations in country-level commodity export prices help predict exchange
rates for this set of currencies. Our analysis focuses on one-month-ahead predictability using nonoverlapping data. We nd that these currencies appreciate, both statistically and economically,
following an increase in commodity export prices. A one-standard-deviation rise in a country's commodity export prices predicts a 0.37% currency appreciation over the next month (equivalent to 4.4%
per annum). Notably, this predictability is short-lived, disappearing after four months. This supports
an information-based mechanism where news is gradually reected in exchange rates. Furthermore,
considering the full cross-section of commodity price betas, we nd that predictability increases with
the currency's commodity beta. This is in line with our model. Intuitively, if commodity shocks have
no contemporaneous eect on a currency (zero beta), we should not see a predictive eect either.
We also provide evidence of superior out-of-sample exchange rate predictability relative to the
traditional benchmark random walk model. The FX market is considered as one of the most active,
liquid, and ecient markets in the world, and predicting short-term exchange rates is known to
be notoriously dicult.7 Consistent with this view, we nd limited out-of-sample predictability for
6As commodity prices are typically denominated in US dollars, a dollar depreciation tends to mechanically increase
commodity prices and appreciate other currencies vis-a-vis the US dollar. Controlling for the dollar factor helps isolate
the portion of exchange rate changes unaected by these eects. Unsurprisingly, ignoring the dollar factor generates
unreasonable predictions. For example, one would erroneously categorize the Singapore dollar and the Swedish krona,
currencies from countries with minimal commodity export shares, as commodity currencies.
7While there is ample evidence of exchange rate predictability at medium to long-term horizons (see, e.g., Mark
(1995a), Engel, Mark, and West (2007), Balduzzi and Chiang (2019), and Eichenbaum, Johannsen, and Rebelo
3
Electronic copy available at: https://ssrn.com/abstract=4564504
highly-traded currencies, such as the Australian and Canadian dollar. However, we do nd robust
predictability for the less-liquid commodity currencies, especially those from emerging markets. For
instance, predictability is particularly strong for the Brazilian real and Russian ruble, two currencies
whose average trading volume is around seven times smaller than that of the Australian dollar.
More generally, we uncover a signicant inverse relationship between a currency's out-of-sample
predictability and its average daily trading volume, in line with a delayed reaction channel.
Our empirical approach mitigates endogeneity concerns by ensuring that exchange rate and commodity export price changes are not driven by variations in nancial market conditions. Specically,
we control for a number of exchange rate predictors, including each country's interest rate dierential
(Fama, 1984), aggregate FX volatility (Bakshi and Panayotov, 2013; Menkho, Sarno, Schmeling,
and Schrimpf, 2012; Karnaukh, Ranaldo, and Söderlind, 2015), funding liquidity (Mancini, Ranaldo,
and Wrampelmeyer, 2013), aggregate market uncertainty (Brunnermeier, Nagel, and Pedersen, 2008;
Lustig, Roussanov, and Verdelhan, 2011), and a US recession indicator to account for the aggregate
commodity declines during global economic slowdowns. Hence, the commodity export prices we
exploit contain unique information unspanned by the factors considered in the extant FX literature.8
Our ndings remain robust regardless of the chosen base currency. While we primarily focus
on exchange rates from the US investors' perspective, commodity export price changes also predict
the future performance of commodity-exposed currencies relative to the euro, Swiss franc, and
Japanese yen. This dismisses the concern that the exchange rate predictability we document is
merely driven by US dollar eects. Furthermore, through a counterfactual analysis, we conrm that
the predictive relation between commodity export prices and exchange rates is not present for the
set of currencies unrelated to commodity prices. This strengthens our argument against omitted
variables (e.g., reecting global economic conditions) potentially driving our ndings. In sum, we nd
that commodity export prices hold valuable predictive information for only the commodity-exposed
currencies' exchange rates, regardless of the base currency.
Next, we explore conditional exchange rate predictability during normal and stressed FX market conditions. Our model predicts that higher FX uncertainty reduces trading among risk-averse
agents. This suggests that newly available information takes more time to be incorporated into
the exchange rate, leading to stronger predictability. Following this theoretical prediction, we assess
the conditional impact of commodity export prices on future exchange rates in a regime-switching
environment, using Jordà (2005)'s local projection method. We nd that exchange rate predictability is concentrated in times of elevated FX uncertainty, as measured by either realized volatility or
dispersion in professional FX forecasts. Thus, the level FX uncertainty plays a key role in conditional
exchange rate predictability.
(2021)), most economic variables fail to predict exchange rates at short horizons (i.e., monthly). See Rossi (2013)
for a comprehensive literature review. Forward-looking nancial measures, however, sometimes have more success in
predicting short-term exchange rates (see, e.g., Londono and Zhou, 2017; Della Corte, Jeanneret, and Patelli, 2023)
Nevertheless, a common assumption is that exchange rates follow a random walk at short horizons.
8Our results are thus unlikely to be inuenced by investors jointly trading commodities and currencies, adjusting
their positions in both assets as global nancial conditions change.
4
Electronic copy available at: https://ssrn.com/abstract=4564504
One may be concerned that time variations in FX uncertainty are linked to broader global market
changes rather than being specic to the FX market itself. For example, aggregate liquidity tends to
evaporate when FX volatility increases (e.g., Karnaukh et al., 2015). Similarly, FX volatility tends to
surge when investor fears (VIX) increase, such as during periods of nancial turmoil (e.g., Menkho
et al., 2012). Currencies can also become riskier when FX dealers face tighter funding constraints and
money-market premiums increase (e.g., Brunnermeier et al., 2008; Ranaldo and Söderlind, 2010), as
indicated by a higher TED spread. However, we nd that exchange rate predictability of commodity
export prices remains statistically signicant and concentrated in times of elevated FX volatility, after
orthogonalizing the latter to FX illiquidity, the VIX, and the TED spread.
Lastly, we explore our results' implications for the carry trade. We expand upon previous research
on the predictability of carry trade returns using commodity prices in several ways, all of which support
our economic narrative.9 First, we nd that the investment component of our strategy is heavily
concentrated in emerging currencies, complementing previous work based on G10 currencies (Bakshi
and Panayotov, 2013). For example, in contrast to common belief, we nd that the investment
portfolio rarely contains the Australian dollar, but frequently includes the Brazilian real, the Russian
ruble, and the South African rand. Eectively, our carry trade strategy invests in G10 currencies
only 6.4% of the time, indicating little overlap with Bakshi and Panayotov (2013). Second, we
provide evidence that carry trade predictability arises largely from the consideration of countryspecic commodity export prices. Even when accounting for global commodity price indices (from
CRB, Goldman Sachs, or the oil price), commodity export prices maintain their predictive power,
while these global predictors do not. Third, we delve into the origin of carry trade predictability (both
theoretically and empirically), a question largely left unaddressed by the existing literature. We form
interest-rate-sorted currency portfolios and nd that their return predictability signicantly increases
with their average commodity currency membership. For example, commodity currencies represent
an average of 36.8% of the investment leg (top quintile), but only 5.8% of the short leg (bottom
quintile). Consequently, commodity prices' predictive power for carry trade returns is driven solely
by the currencies with signicant commodity price betas that are part of the investment portfolio.
Additionally, we nd that predictability is concentrated in times of elevated FX volatility, mirroring our
ndings for individual exchange rates. Furthermore, we exploit our large cross-section of currencies
and consider a counterfactual carry trade strategy that excludes commodity currencies. While this
alternative strategy remains unconditionally almost as protable as the unconstrained carry trade, it
no longer exhibits commodity export price predictability. In sum, we nd that the predictability of
the carry trade with commodity prices is purely driven by the exchange rate predictability of a few
commodity currencies, which we study in this paper, not because commodity prices capture a global
risk factor or because commodity investing coincides with an appetite for risk-taking.
9Bakshi and Panayotov (2013) study the predictability of carry trade returns using global predictors such as FX
volatility, funding liquidity, and the Commodity Research Bureau (CRB) commodity price index. Relatedly, Opie and
Riddiough (2020) study international portfolio hedging using FX factors and document the predictability of Lustig et al.
(2011)'s carry trade factor with the CRB index, before using it for portfolio optimization.
5
Electronic copy available at: https://ssrn.com/abstract=4564504
Our paper also contributes to the literature on the relationship between commodity prices and
exchange rates. Amano and Van Norden (1998) nds that oil prices Granger-cause the real US dollar
exchange rate, while Chen and Rogo (2003) provide evidence that commodity prices are in-sample
predictors of quarterly exchange rates for Australia, Canada, and New Zealand. Chen et al. (2010)
add two more countries (Chile and South Africa) to their analysis and nd that exchange rates predict
global commodity prices, but that the reverse does not hold out-of-sample. In contrast, Ferraro et al.
(2015), analyzing ve commodity-producing countries (Australia, Canada, Norway, Chile and South
Africa), nd signicant out-of-sample predictability (with oil, copper, or gold prices), but only at the
daily frequency. We expand on these earlier studies on multiple key dimensions. First, we consider
a large cross-section of currencies, which allows us to (i) analyze previously ignored currencies, (ii)
identify commodity currencies in a systematic way, (iii) relate commodity exposures to a broad set of
economic fundamentals, and (iv) to conduct counterfactual exercises utilizing the full cross-section.
Second, in contrast to Chen et al. (2010), we nd evidence of signicant monthly predictability,
especially for emerging market currencies. This predictability, however, is short-lived, aligning with
the earlier ndings of no quarterly predictability (Chen et al., 2010) and signicant daily predictability
at (Ferraro et al., 2015). Third, we oer a tractable model that explains why short-term exchange
rate predictability with commodity export prices is concentrated in periods of high FX uncertainty.
Lastly, we demonstrate our results' critical implications for the carry trade.
Our work is closely related to Ready et al. (2017). Their general-equilibrium model shows
that (i) commodity-exporting countries have lower aggregate risk and thus higher interest rates,
compared to countries producing nal goods; and (ii) commodity currencies appreciate in good
times and depreciate in bad times, thereby earning a risk premium. Their model thus rationalizes
why commodity currencies have relatively higher interest rates and oer higher returns, particularly
when goods markets are more segmented due to higher trade costs. The authors empirically validate
their model's cross-sectional implications and the theoretical prediction that shipping costs positively
forecast carry trade returns. Our paper diers from this inuential work in several ways. First,
we consider an information-based explanation for exchange rate predictability, where exchange rates
slowly adjust to commodity price changes. This contrasts with Ready et al. (2017)'s risk-based
model, which explicitly predicts no short-term predictability. Our results support our model, showing
strong predictability at short horizons, particularly during high FX uncertainty and among emerging
currencies. Second, their complete markets model applies elegantly to developed economies, where
aggregate consumption is expected to be relatively stable. Our framework, on the other hand, is
well-suited to emerging currencies which appear to be less liquid and thus more likely to incorporate
information with a delay. This is important because, when considering a large cross-section of
currencies, emerging currencies constitute the bulk of the investment side of the carry trade. Overall,
the dierences between our work and that of Ready et al. (2017) provide complementary insights
into the role of commodity prices in carry trade predictability.
More broadly, we contribute to the understanding of the carry trade performance. Existing
literature has identied various common risk factors that help explain the cross-section of currency
6
Electronic copy available at: https://ssrn.com/abstract=4564504
returns and thus the unconditional carry trade protability.10 Our work complements this strand
of the literature by providing evidence that changes in country-specic commodity export prices
can explain the time variation in exchange rate changes and, in turn, the conditional carry trade
performance. Additionally, our ndings revisit the connection between the carry trade and individual
currency returns. For example, Verdelhan (2018) suggests that the carry trade exposes investors to
global risk factors, such that a currency that is more exposed to the carry trade factor is viewed as
riskier and earns a higher expected return. Our ndings emphasize that individual exchange rates
are subject to currency-specic shocks, which in turn could aect the carry trade performance.
This is because the carry trade's long portfolio is heavily concentrated in a small set of commodity
currencies, whose uctuations cannot be fully diversied away.11 Our work therefore highlights a
new individual FX returns to carry trade channel that complements the existing carry trade to
individual FX returns channel.
The remainder of the paper is organized as follows. Section 2 presents a simple model that
provides guidance on exchange rate predictability. Section 3 describes the data and identies the set
of commodity currencies. Sections 4 and 5 discuss our main empirical ndings on the unconditional
and conditional exchange rate predictability, respectively. Section 6 extends the analysis to the carry
trade, while Section 7 provides an out-of-sample analysis. Section 8 concludes.
2 Motivating theory
We present a stylized model of exchange rate determination with heterogeneous agents to explore
how variation in commodity export prices can generate exchange rate predictability. The setting builds
on existing equilibrium models with dierences of opinion among traders.12 In our model, agents
agree to disagree on the relevance of using commodity export prices for predicting exchange rates,
even if they have access to the same publicly available information. When agents trade based on
their dierent beliefs, we nd that new information is slow to reect in exchange rates. This delay
then results in future exchange rates being predictable by changes in commodity export prices.
Our framework departs from the existing macro-nance literature, which has developed models to
uncover sources of currency risk premiums. This literature focuses primarily on the cross-sectional
analysis of currency excess returns or on long-term predictability.13 In contrast to existing risk
10Unconditional currency (excess) returns reect compensation for investors' exposure to global factors, such as
consumption growth risk (Lustig and Verdelhan, 2007), consumption habits (Verdelhan, 2010), average excess returns
(Lustig et al., 2011), systematic FX volatility (Menkho et al., 2012), systematic liquidity (Mancini et al., 2013), global
imbalance risk (Della Corte, Riddiough, and Sarno, 2016), crash risk (Chernov, Graveline, and Zviadadze, 2018), the
business cycle (Colacito, Riddiough, and Sarno, 2020), and FX liquidity risk (Söderlind and Somogyi, 2023).
11Fluctuations in country-specic commodity export prices, similar to rm-specic shocks in a granular economy
(Gabaix, 2011), have signicant implications for aggregate asset pricing.
12See, for example, Harrison and Kreps (1978), Harris and Raviv (1993), Kandel and Pearson (1995), Cao and
Ou-Yang (2008), Banerjee, Kaniel, and Kremer (2009), Banerjee and Kremer (2010), Bhamra and Uppal (2014),
Dumas, Lewis, and Osambela (2017), and Atmaz and Basak (2018) for theoretical models of stock prices.
13See the references cited in footnote 7. Notable exceptions are the early literature on the protability of technical
7
Electronic copy available at: https://ssrn.com/abstract=4564504
premium explanations, we consider an information-based model to study how public news becomes
incorporated into exchange rates, both contemporaneously and with a delay, thereby generating
short-term predictability. The proposed framework is particularly well-suited for understanding how
current and future exchange rates of commodity exporters should vary with the prices of commodity
exports, which are arguably an important source of revenue for such countries. The model provides
new testable predictions, which we use to guide our empirical analysis.
2.1 Environment
Consider a three-date, two-period economy with dates indexed by t = 0, 1, 2. We dene the (log)
exchange rate st as the date-t price in US dollars of a unit of foreign currency. At date 2, the
exchange rate is given by
s2 = ¯s + Φ, (1)
where s¯ determines the initial exchange rate level, which is known at date 0. Φ is a normally
distributed variable with mean 0 and volatility σ. The component Φ reects fundamental information
on the date-2 exchange rate level, such that Φ > 0 (Φ < 0) represents an appreciation (depreciation)
of the foreign currency. The distribution of s2, including its parameters, is common knowledge to
all agents. Risk-free rates are set to 0 for convenience, i.e., we abstract from the role of UIP.
Additionally, money supply plays no role in the model, so we need not specify a two-country economy.
2.2 Heterogenous beliefs
It is well established that the FX market involves dierent categories of market participants such
as corporates, commercial banks, or asset managers.14 Each participant has a distinct objective
depending on (i) the extent to which the agent exploits available information, and (ii) whether the
agent is a liquidity maker or taker.
Building on this insight, we consider three types of agents in the market. First, there is a
research-intensive informed agent (hereafter the Informed trader), who learns about the fundamental exchange rate component Φ using public information available at date 1. Second, there is an
uninformed agent (Uninformed trader, thereafter), who oers liquidity in the market, akin to a market maker. This agent views the exchange rate as a random walk in the spirit of Meese and Rogo
(1983) and thus does not attempt to learn about Φ. Third, there is a Noise trader buying/selling
analysis in the currency market (see, e.g., Levich and Thomas III, 1993) and the recent work by Cespa et al. (2022),
which nds that trading volume helps predict one-day-ahead exchange rate changes.
14Heterogeneity in agents' information is a strong feature of the FX market due to its opaque OTC nature characterized by a decentralized network and dealership structure. The rise of electronic trading and settlement in recent
years has also amplied market fragmentation and asymmetric information across market participants. See Ranaldo
and Somogyi (2021) for recent empirical evidence, and King, Osler, and Rime (2012) for a comprehensive review of
the FX market structure.
8
Electronic copy available at: https://ssrn.com/abstract=4564504
currencies for exogenous reasons (e.g., a corporate), which reects any non-informational trading in
the FX market.
All agents are ex-ante identical, trade competitively, and have common knowledge about each
other's views. Additionally, all agents have the same initial prior of s¯ for the future exchange rate
level, therefore s0 = ¯s. Heterogeneity across agents arises due to dierences in beliefs about the
usefulness of public information released at date 1, which we describe below. That is, only a fraction
of agents have the ability or willingness to process new information and trade on it, consistent with
Cespa et al. (2022), among others.15
2.3 News and expectations
At date 1, the Informed trader (identied by the subscript I) learns about the fundamental component
Φ from the public news
p ≡ Φ + ϵ, (2)
where p is an unbiased, albeit noisy, signal for the fundamental component Φ, and ϵ is a normally
distributed noise term with mean zero and variance σ
2
ϵ
.
In the case of a commodity-exporting country like Australia, for example, the spot exchange rate
s reects the number of US dollars per Australian dollar. For a country like this, an important piece
of public news is the price of its exported commodities. This price tells us much about the country's
terms of trade and gives us insights into its exchange rate.16
The Informed trader processes the public news p and uses Bayesian updating to form new beliefs
about s2:
EI,1 [s2] = ¯s + ηp (3)
VI,1 [s2] = (1 − η) σ
2
, (4)
where Ei,1 ≡ Ei[·|Fi,1] and Vi,1 ≡ Vi[·|Fi,1] denote the conditional expectation and variance given
the agent i's information set Fi,t at time t, while η is the informativeness (or signal-to-noise ratio)
of the public news p:
η =
COVI,1[p, Φ]
VI,1 [p]
=
σ
2
σ
2 + σ2
ϵ
∈ (0, 1), (5)
15See Menkho, Sarno, Schmeling, and Schrimpf (2016) for evidence that dierent groups of FX market participants
dier markedly in their predictive ability.
16There exists a long-standing literature on the terms in trade's role in explaining exchange rates, particularly for
commodity exporters. See Neary (1988) for an early discussion. See also Chen and Rogo (2003) and Chen et al.
(2010) and the references therein.
9
Electronic copy available at: https://ssrn.com/abstract=4564504
where COVI,1
[p, Φ] denotes the covariance between the public news p and the fundamental Φ, as
measured by the Informed agent at date 1. The Informed trader thus learns about the fundamental
level of the exchange rate and takes a position in the market based on the new publicly available
information.
The Uninformed trader (identied by the subscript U), however, either does not believe that
news p contains any valuable information or is unable to process it. The expected exchange rate for
the Uninformed trader at date 1 is
EU,1 [s2] = ¯s ̸= EI,1 [s2] = ¯s + ηp (6)
VU,1 [s2] = σ
2 > VI,1 [s2] = (1 − η) σ2
. (7)
Both agents I and U agree to disagree on the relevant information set and, thus, on the expected
exchange rate level. Each agent believes that no other agent holds information of any additional
value to his or her information set, following classic models based on dierences of opinions (e.g.,
Harrison and Kreps, 1978). The fact that agents have heterogeneous beliefs has long been accepted
as a key feature in nancial and FX markets, as sophisticated investors, analysts, and economists
often publicly disagree about their forecasts.
Note that the dierence in expectations across agents given by EI,1 [s2] − EU,1 [s2] = σ
2
σ2+σ2
ϵ
p
increases with the level of exchange rate uncertainty σ
2
. A higher σ means the Informed trader
has a stronger informational advantage of using the public news (the signal-to-noise ratio increases,
see Equation 5). However, as the public news becomes pure noise, σ
2
σ2+σ2
ϵ
→ 0 , this informational
advantage vanishes.
2.4 Optimal demand and equilibrium exchange rate
All agents maximize CARA utility over terminal wealth, with risk-aversion set to one for notational
simplicity, as in Banerjee and Kremer (2010) and Cespa et al. (2022), among others. Optimal
demand for agent i = I, U at date 1 is
xi,1 =
Ei,1 [s2] − s1
Vi,1 [s2]
, (8)
while the aggregate demand/supply of the noise trader, denoted by xN,t, is normally distributed with
mean 0 and volatility σN . In our model, the role of the noise trader's shocks is to allow exchange
rates to also vary for non-fundamental reasons, as one would expect in the data.
Imposing market clearing conditions, the equilibrium exchange rate at date 1 (i.e., after the
10
Electronic copy available at: https://ssrn.com/abstract=4564504
public news p is revealed) is equal to (see Internet Appendix A.1)
s1 = ¯µs + ¯σ
2
sxN,1 (9)
with
µ¯s = ωIEI,1 [s2] + ωU EU,1 [s2] = ¯s + ωIη
|{z}
<1
p (10)
σ¯
2
s = ωIVI,1 [s2] + ωUVU,1 [s2] = (1 − ωIη)
| {z }
<1
σ
2
, (11)
where ωI and ωU reect the relative weights of the Informed and Uninformed traders, respectively,
while σ¯
2
s
is the aggregate degree of uncertainty about exchange rate s2. Note that σ¯
2
s
reects the
uncertainty perceived by the average agent, which diers from the true level of exchange rate
uncertainty, σ
2
.
From Equation (11), the equilibrium exchange rate corresponds to the average valuation across
agents and, thus, only partially reects the available public information about Φ. When there is
disagreement across agents, the average agent puts a weight on the public news that is lower
than the informativeness of p, given that ωIη < 1. Hence, the equilibrium exchange rate at date 1
underreacts to new public information.
2.5 Impact on contemporaneous and future exchange rate changes
Let ∆s1 ≡ s1 − s0 be the rst-period (log) exchange rate change. From Equation (9) and s0 = ¯s,
it follows that:
∆s1 =

µ¯s + ¯σ
2
sxN,1

| {z }
s1
− s¯
|{z}
s0
(12)
= ωIηp + ¯σ
2
sxN,1
| {z }
noise
(13)
given that µ¯s = ¯s + ωIηp from Equation (10). The contemporaneous impact of the public news p
on ∆s1 can be expressed as δ∆s1
δp = ωIη > 0, which increases with the fraction of Informed traders
in the market (ωI ). It also increases with the informativeness of the news (η). The price impact of
trade is thus positively related to the asymmetric use of public information across FX traders, in line
with the empirical ndings of Ranaldo and Somogyi (2021).
We now discuss the implication for exchange rate predictability. The second-period (log) ex11
Electronic copy available at: https://ssrn.com/abstract=4564504
change rate change, ∆s2 ≡ s2 − s1, is given by:
∆s2 = ¯s + Φ | {z }
s2
−

µ¯s + ¯σ
2
sxN,1

| {z }
s1
(14)
= Φ − ωIηp − σ¯
2
sxN,1 (15)
= [1 − ωIη] p − ϵ − σ¯
2
sxN,1
| {z }
noise
, (16)
as the date-2 exchange rate is s2 = ¯s + Φ once the fundamental information is revealed. Given that
information is gradually incorporated into prices, the public news p released at date 1 becomes useful
for predicting the future exchange rate. In other words, δ∆s2
δp = 1 − ωIη > 0.
17
Despite being as parsimonious as possible, our model generates two insightful predictions: (i) an
increase in a country's commodity export prices p can only be informative about the future exchange
rate if it generates a contemporaneous currency appreciation ( δ∆s1
δp > 0). So, a commodity currency
should be a currency that has a positive and signicant exposure to current changes in commodity
export prices. (ii) For such currencies, equilibrium exchange rates slowly reect newly available
information when the FX market consists of participants with heterogenous beliefs. This gradual
diusion of new public information about commodity export prices into the exchange rate generates
short-term predictability ( δ∆s2
δp > 0).
2.6 Model discussion
The model developed above contains several simplifying assumptions that help provide a good balance
between tractability and realism. We focus on three periods only so that the news exploited by the
more informed agent is short-lived. This is arguably a reasonable assumption for three reasons.
First, it is equivalent to assuming a model with additional periods but with news that is identically
and independently distributed over time, as in Llorente, Michaely, Saar, and Wang (2002). Second,
Cespa et al. (2022) nds that short-term exchange rate predictability also arises in an overlappinggenerations (OLG) framework. Third, introducing persistence in the news would amplify rather than
weaken exchange rate predictability. Another assumption is that investors have CARA preferences
and exchange rates are lognormally distributed, which allows for a closed-form solution in the model.
This assumption precludes any income eect, as investors' positions are independent of wealth.
It could be a fruitful avenue for future research to consider more general agent preferences while
studying exchange rate predictability in a richer environment. Relaxing these assumptions is possible,
17The model implies the possibility of negative serial correlation (Cov(∆s1, ∆s2) < 0) due to noise trader shocks,
for example if xN,1 is large. However, the positive exposure of ∆s2 to the signal p is independent of the level of noise
trading, given that δ∆s2
δp = 1 − ωI η. Nevertheless, while the level of noise trading has no impact on the economic
relation of interest, i.e., the eect of p on ∆s2, noise trading increases the variance of ∆s2 and could thus reduce the
statistical signicance of this exposure once we estimate the empirical counterpart of Equation (16).
12
Electronic copy available at: https://ssrn.com/abstract=4564504
but we believe it adds little to the main message of the paper.
Our theoretical analysis is expected to be particularly relevant in the context of commodity
exporters' (e.g., Australia or Russia) currencies. The predictions suggest that uctuations in commodity export prices, a public and informative source of news for these countries, should impact
their contemporaneous and future exchange rate changes. In contrast, we should not expect to
observe any of these relations for countries with negligible commodity exports (e.g., Switzerland).
This is because commodity export prices should not be viewed as informative for their exchange
rates. Guided by these insights, we provide a comprehensive analysis of how changes in commodity
export prices predict exchange rate changes for a set of meaningful commodity currencies.
3 Identifying commodity currencies
In this section, we ask what constitutes a commodity currency. Countries that specialize in exporting
basic commodities are typically labeled as commodity countries, and their respective currencies are
often regarded as commodity currencies. However, there is some degree of arbitrariness in the
denition, with many studies analyzing just small sets of candidates.18 For example, what should
be the threshold to categorize a currency as a commodity currency? When a country's exports are
composed of more than 20% of commodities, or rather 30%, or even 50%? Additionally, shouldn't
the type of commodities matter? For example, is exporting dairy products comparable to exporting
oil and gas? Clearly, there is a lot of latitude as to what denes a commodity currency. However,
a reasonable classication approach should be clear, theoretically motivated, statistically sound, and
subject to minimal discretion in the criteria.
In light of this, we propose a formal identication of commodity currencies based on a marketbased approach. We rst provide a denition based on a currency's commodity price beta. Next, we
describe our data, after which we discuss the identied set of commodity currencies.
3.1 Denition
Guided by our theory, we dene a commodity currency as a currency that varies positively with its
country's commodity export prices (i.e., the currency appreciates when commodity export prices
increase and depreciates when they fall). This is in line with Ready et al. (2017)'s equilibrium
model showing that commodity currencies' exchange rates are positively correlated with commodity
prices. Our denition is economically intuitive; if a country's exports are a key factor (valuable public
18Chen and Rogo (2003) only consider Australia, Canada, and New Zealand; Chen et al. (2010) consider the three
countries in the sample of Chen and Rogo (2003) plus Chile and South Africa; Ferraro et al. (2015) consider Australia,
Canada, Chile, Norway, and South Africa; Ready et al. (2017) examine 21 developed countries and do not formally
categorize currencies as commodity currencies. However they do refer to a familiar group of commodity exporters
(Australia, Canada, New Zealand, and Norway) in their discussions.
13
Electronic copy available at: https://ssrn.com/abstract=4564504
information) for the traders of this currency, commodity export prices must contemporaneously aect
its exchange rate, i.e., the currency has a positive commodity price beta. A key advantage of this
approach is that the beta embeds all relevant information regarding the importance and type of a
country's commodity exports in one single metric.
3.2 Data
We now describe our primary data, which consists of individual foreign exchange rates and countryspecic commodity export price indexes. We discuss the auxiliary data when introducing it in our
analysis as well as in the Internet Appendix. The sample period runs from January 1985 to April
2020.
FX data We collect daily spot and one-month forward exchange rates relative to the US dollar
from WM/Reuters via Datastream. Exchange rates are dened as units of US dollars per unit of
foreign currency, so that an increase in the exchange rate indicates an appreciation of the foreign
currency. Monthly data are obtained by sampling end-of-month exchange rates. Our sample includes
41 developed and emerging market currencies. Namely, the currencies of Australia, Austria, Belgium,
Brazil, Bulgaria, Canada, Chile, Colombia, Croatia, Czechia, Denmark, Finland, France, Germany,
Greece, Hungary, India, Indonesia, Ireland, Italy, Japan, Malaysia, Mexico, the Netherlands, New
Zealand, Norway, Peru, the Philippines, Poland, Portugal, Russia, Singapore, Slovenia, South Africa,
South Korea, Spain, Sweden, Switzerland, Thailand, the United Kingdom, and the euro area. The
euro series starts in January 1999. After this date, euro area countries are excluded and only the
euro series remains. We lter these data following Lustig et al. (2011) and Dahlquist and Hasseltoft
(2020).
Our sample of currencies is similar to that of Lustig et al. (2011), but includes additional commodity exporters such as Colombia, Chile, and Peru. Our sample diers, however, from the work
of Ready et al. (2017), who also study commodity currencies but focus exclusively on developed
countries (this is because the equilibrium model they test requires sample countries to be nancially
integrated). We, on the other hand, do not need to restrict our sample, as our empirical analysis is
guided by a dierences of opinion theoretical framework which is applicable to all currencies.19
Commodity export prices We use commodity price data from the International Monetary Fund
(IMF) Commodity Term of Trade database, which provides country-specic commodity price indexes
for many countries. These indexes are constructed for each country as trade-weighted changes in the
international market prices of up to 45 individual commodities (including agricultural raw materials,
energy, food and beverages, and metals). Given our focus on commodity export prices, we use the
19Our framework may be especially relevant for emerging market currencies, as they are relatively less ecient,
potentially making dierences of opinion more prevalent (e.g., Pukthuanthong-Le and Thomas, 2008).
14
Electronic copy available at: https://ssrn.com/abstract=4564504
export-weighted indexes for each of the 41 countries in our sample. The weights are each country's
individual commodity exports, scaled by its overall commodity trade. To account for variations
in commodity trade over time, the weights are time-varying (specically, lagged three-year rolling
averages).20 The index methodology ensures that changes in the price indexes reect variations in
the relevant commodity export prices for each country at each point in time. It is thus well-suited
for our analysis.
3.3 Commodity price beta
To identify the set of commodity currencies, we estimate the following benchmark regression at a
monthly frequency for each individual currency:
∆si,t = αi + βi∆CEPi,t + γiDOLt + εi,t, (17)
where ∆si,t denotes the log change in nominal bilateral exchange rate in US dollar per unit of currency
i in month t (i.e., an increase corresponds to an appreciation of currency i), while ∆CEPi,t denotes
the log change in the commodity export price index of country i in month t. The dollar factor DOLi,t
is computed as the average change in exchange rates against the US dollar in month t, following
Verdelhan (2018).21 The coecient, βi, is the currency i's sensitivity to its country's c