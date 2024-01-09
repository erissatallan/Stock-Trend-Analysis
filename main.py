# region imports
from AlgorithmImports import *
# endregion

class SPY_TRADER(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2022, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)

        spy = self.AddEquity("SPY", Resolution.Daily)
        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)

        self.spy = spy.Symbol  # saving the symbol object of SPY into a new variable
        self.SetBenchmark("SPY")

        # a brokerage model adjusts the fee structure to that of the selected brokerage
        # cash account do not allow the use of leverage; margin accounts allow up to x4 leverage
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time  # when to re-enter a long SPY position

    # event handler called every time algorithm receives data: tick/ end bar
    def OnData(self, data: Slice):
        if not self.spy in data:
            return

        price = data[self.spy].Close

        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                # self.SetHoldings(self.spy, 1)
                self.MarketOrder(self.spy, -int(self.Portfolio.Cash / price))
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price

        # if entry price is either 10% below or above the current price, exit SPY position
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.Liquidate(self.spy)
            self.Log("SELL SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period # ensures we are in cash for a month