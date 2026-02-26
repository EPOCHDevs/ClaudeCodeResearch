#region imports
from AlgorithmImports import *
#endregion

class FuturesInfo():
    def __init__(self, quantpedia_future:Symbol) -> None:
        self.quantpedia_future:Symbol = quantpedia_future
        self.near_contract:FuturesContract = None
        self.distant_contract:FuturesContract = None

    def update_contracts(self, near_contract:FuturesContract, distant_contract:FuturesContract) -> None:
        self.near_contract = near_contract
        self.distant_contract = distant_contract

    def is_initialized(self) -> bool:
        return self.near_contract is not None and self.distant_contract is not None

# Custom fee model.
class CustomFeeModel():
    def GetOrderFee(self, parameters):
        fee = parameters.Security.Price * parameters.Order.AbsoluteQuantity * 0.00005
        return OrderFee(CashAmount(fee, "USD"))

# Quantpedia data.
# NOTE: IMPORTANT: Data order must be ascending (datewise)
class QuantpediaFutures(PythonData):
    _last_update_date:Dict[str, datetime.date] = {}

    @staticmethod
    def get_last_update_date() -> Dict[str, datetime.date]:
       return QuantpediaFutures._last_update_date

    def GetSource(self, config:SubscriptionDataConfig, date:datetime, isLiveMode:bool) -> SubscriptionDataSource:
        return SubscriptionDataSource("data.quantpedia.com/backtesting_data/futures/{0}.csv".format(config.Symbol.Value), SubscriptionTransportMedium.RemoteFile, FileFormat.Csv)

    def Reader(self, config:SubscriptionDataConfig, line:str, date:datetime, isLiveMode:bool) -> BaseData:
        data = QuantpediaFutures()
        data.Symbol = config.Symbol

        if not line[0].isdigit(): return None
        split = line.split(';')

        data.Time = datetime.strptime(split[0], "%d.%m.%Y") + timedelta(days=1)
        data['back_adjusted'] = float(split[1])
        data['spliced'] = float(split[2])
        data.Value = float(split[1])

        # store last update date
        if config.Symbol not in QuantpediaFutures._last_update_date:
            QuantpediaFutures._last_update_date[config.Symbol] = datetime(1,1,1).date()
        if data.Time.date() > QuantpediaFutures._last_update_date[config.Symbol]:
            QuantpediaFutures._last_update_date[config.Symbol] = data.Time.date()

        return data
