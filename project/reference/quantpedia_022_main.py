# https://quantpedia.com/strategies/term-structure-effect-in-commodities/
#
# This simple strategy buys each month the 20% of commodities with the highest roll-returns and shorts the 20% of commodities with the lowest
# roll-returns and holds the long-short positions for one month. The contracts in each quintile are equally-weighted.
# The investment universe is all commodity futures contracts.
#
# QC implementation changes:

#region imports
import numpy as np
from AlgorithmImports import *
import data_tools
#endregion

class TermStructureEffectinCommodities(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2009, 1, 1)
        self.SetCash(100000)

        symbols: Dict[str, str] = {
            'CME_S1': Futures.Grains.Soybeans,
            'CME_W1': Futures.Grains.Wheat,
            'CME_SM1': Futures.Grains.SoybeanMeal,
            'CME_C1': Futures.Grains.Corn,
            'CME_O1': Futures.Grains.Oats,
            'CME_LC1': Futures.Meats.LiveCattle,
            'CME_FC1': Futures.Meats.FeederCattle,
            'CME_LN1': Futures.Meats.LeanHogs,
            'CME_GC1': Futures.Metals.Gold,
            'CME_SI1': Futures.Metals.Silver,
            'CME_PL1': Futures.Metals.Platinum,
            'CME_HG1': Futures.Metals.Copper,
            'CME_LB1': Futures.Forestry.RandomLengthLumber,
            'CME_NG1': Futures.Energies.NaturalGas,
            'CME_PA1': Futures.Metals.Palladium,
            # 'CME_DA1': Futures.Dairy.ClassIIIMilk,
            'CME_RB1': Futures.Energies.Gasoline,
            'ICE_WT1': Futures.Energies.CrudeOilWTI,
            'ICE_CC1': Futures.Softs.Cocoa,
            'ICE_O1': Futures.Energies.HeatingOil,
            'ICE_SB1': Futures.Softs.Sugar11CME,
        }

        self.futures_info: Dict[str, data_tools.FuturesInfo] = {}
        self.quantile: int = 5

        min_expiration_days: int = 2
        max_expiration_days: int = 360

        for qp_symbol, qc_future in symbols.items():
            # QP futures data:
            data: Security = self.AddData(data_tools.QuantpediaFutures, qp_symbol, Resolution.Daily)
            data.SetFeeModel(data_tools.CustomFeeModel())
            data.SetLeverage(5)

            # QC futures
            future: Future = self.AddFuture(qc_future, Resolution.Daily)
            future.SetFilter(timedelta(days=min_expiration_days), timedelta(days=max_expiration_days))

            self.futures_info[future.Symbol.Value] = data_tools.FuturesInfo(data.Symbol)

        self.recent_month: int = -1
        self.Settings.MinimumOrderMarginPortfolioPercentage = 0.

    def find_and_update_contracts(self, futures_chain, symbol) -> None:
        near_contract: FuturesContract = None
        dist_contract: FuturesContract = None

        if symbol in futures_chain:
            contracts: List = [contract for contract in futures_chain[symbol] if contract.Expiry.date() > self.Time.date()]

            if len(contracts) >= 2:
                contracts: List = sorted(contracts, key=lambda x: x.Expiry, reverse=False)
                near_contract = contracts[0]
                dist_contract = contracts[1]

        self.futures_info[symbol].update_contracts(near_contract, dist_contract)

    def OnData(self, slice: Slice) -> None:
        if slice.FutureChains.Count > 0:
            for symbol, futures_info in self.futures_info.items():
                # check if near contract is expired or is not initialized
                if not futures_info.is_initialized() or \
                    (futures_info.is_initialized() and futures_info.near_contract.Expiry.date() <= self.Time.date()):
                    self.find_and_update_contracts(slice.FutureChains, symbol)

        roll_return: Dict[Symbol, float] = {}
        rebalance_flag: bool = False

        # roll return calculation
        for symbol, futures_info in self.futures_info.items():
            # custom data is still coming
            if self.securities[futures_info.quantpedia_future].get_last_data() and \
                self.time.date() > data_tools.QuantpediaFutures.get_last_update_date()[futures_info.quantpedia_future]:
                self.liquidate()
                return

            # futures data is present in the algorithm
            if futures_info.quantpedia_future in slice and slice[futures_info.quantpedia_future]:
                # new month rebalance
                if self.Time.month != self.recent_month and not self.IsWarmingUp:
                    self.recent_month = self.Time.month
                    rebalance_flag = True

                if rebalance_flag:
                    if futures_info.is_initialized():
                        near_c: FuturesContract = futures_info.near_contract
                        dist_c: FuturesContract = futures_info.distant_contract

                        if self.Securities.ContainsKey(near_c.Symbol) and self.Securities.ContainsKey(dist_c.Symbol):
                            raw_price1: float = self.Securities[near_c.Symbol].Close
                            raw_price2: float = self.Securities[dist_c.Symbol].Close

                            if raw_price1 != 0 and raw_price2 != 0:
                                # KEY: roll return = near/distant - 1
                                # Positive = backwardation, Negative = contango
                                roll_return[futures_info.quantpedia_future] = raw_price1 / raw_price2 - 1

        if rebalance_flag:
            weights: Dict[Symbol, float] = {}
            long: List[Symbol] = []
            short: List[Symbol] = []

            if len(roll_return) >= self.quantile:
                # roll return sorting
                sorted_by_roll: List[Tuple] = sorted(roll_return.items(), key=lambda x: x[1], reverse=True)
                quantile: int = int(len(sorted_by_roll) / self.quantile)
                long = [x[0] for x in sorted_by_roll[:quantile]]
                short = [x[0] for x in sorted_by_roll[-quantile:]]

            # trade execution
            invested: List[Symbol] = [x.Key for x in self.Portfolio if x.Value.Invested]
            for symbol in invested:
                if symbol not in long + short:
                    self.Liquidate(symbol)

            for i, portfolio in enumerate([long, short]):
                for symbol in portfolio:
                    if symbol in slice and slice[symbol]:
                        # i=0 -> long (+1/N), i=1 -> short (-1/N)
                        self.SetHoldings(symbol, ((-1) ** i) / len(portfolio))
