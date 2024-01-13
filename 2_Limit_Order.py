
"""     Strategy
Buy and hold a stock or Exchange Traded Fund (ETF) with a stop loss executed when the security drops to 5%
below its present price. If the stop loss is hit, exit the position the resume trading after a business-week.
The wait is time given for the instrument to step out of the prevailing trend.

"""

from AlgorithmImports import *


class TradingStrategy2(QCAlgorithm):

    def Initialize(self):
        self.StartDate(2023, 1, 1)
        self.EndDate(2023, 12, 31)
        self.SetCash(100000)

        self.qqq = self.AddEquity("QQQ", Resolution.Hour).Symbol

        # ticket objects are used to access
        self.entryTicket = None
        self.stopMarketTicket = None  # the stop order is a market order; executes at the closest possible prices
        self.entryTime = datetime.min  # earliest possible date, since no orders have been filled yet
        self.stopMarketOrderFillTime = datetime.min
        self.higherPrice = 0  # needed to evaluate when to execute the trailing stop loss order

        # to ensure that there is always a buffer of cash in the account/ there is always buying power
        self.Settings.FreePortfolioValuePercentage = 0.05

    
    def OnData(self, data: Slice):
        # check whether 30 days since the last exit have elapsed
        if (self.Time - self.stopMarketOrderFillTime).days < 7:
            return

        price = self.Securities[self.qqq].Price

        # send limit order (buy)
        # an order ticket is the object you get after creating an object of any kind: tracks, accesses, edits order
        # this is returned in stead of an order object because order execution is asynchronous
        if not self.Portfolio.Invested and not self.Transactions.GetOpenOrders(self.qqq):
            quantity = self.CalculateOrderQuantity(self.qqq, 0.9)
            self.entryTicket = self.LimitOrder(self.qqq, quantity, price, "Entry order")
            self.entryTime = self.Time


        # move the limit price higher (since we are buying) if order is not filled after a day
        # check whether 1 day has passed and check whether the order has been filled or not
        if (self.Time - self.entryTime).days > 1 and self.entryTicket.Status != OrderStatus.Filled:
            self.entryTime = self.Time
            updateFields = UpdateOrderFields()
            updateFields.LimitPrice = price
            self.entryTicket.Update(updateFields)

        # move up trailing stop loss price, if necessary
        # move stop loss price up to below 5% of current since must have been going up
        if self.stopMarketTicket is not None and self.Portfolio.Invested:
            if price > self.highestPrice:
                self.higherPrice = price
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = price * 0.95
                self.stopMarketTicket.Update(updateFields)

    
    # The onOrderEvent handler is called on every order event. Used here to send out a stop loss order
    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status != OrderStatus.Filled:
            return

        # send stop loss order if entry limit order is filled
        if self.entryTicket is not None and self.entryTicket.OrderId == orderEvent.OrderId:
            self.stopMarketTicket = self.StopMarketOrder(self.qqq, -self.entryTicket.Quantity,
                                            0.95 * self.entryTicket.AverageFillPrice)

        # save fill time of stop loss order: case where stop market order has been filled
        if self.StopMarketTicket is not None and self.stopMarketTicket.OrderId == orderEvent.OrderId:
            self.stopMarketOrderFillTime = self.Time
            self.higherPrice = 0  # since QQQ price may be lower a week from now