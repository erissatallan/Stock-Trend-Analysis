# Stock-Trend-Analysis
 Statistical analyses of the price movements of the most profitable stock indices of 2023 and the five years leading up to 2024.

## Algorithm 1
The SPY is an exchange-traded fund (ETF) that tracks the S&P 500 ETF. The algorithm SPY500 above trades this ETF by buying or selling 10% of the portolio in response to the corresponding market movement. A business-week period between the close of a trade to the opening of another is given to not enter a trade in the same conditions just left.

## Algorithm 2
Buy and hold a stock or Exchange Traded Fund (ETF) with a stop loss executed when the stock drops to 5% below its present price. If the stop loss is hit, exit the position then resume trading after a business-week. The one week wait is time given for the instrument to step out of the prevailing market trend.

## Algorithm 3
A trend-following moving average trading strategy. Evaluate the average of the closing prices of the stock of interest over two time intervals (windows), a longer one and a shorter one. If there is change over some threshold between these two windows, perform a corresponding trade on the stock.

## Algorithm 4
A moving average strategy designed to be deployed on Quantopian's LEAN engine.

## Algorithm 5
A mean-reverting trading strategy. Mean reversion strategies are based on the idea that asset prices tend to revert to their historical average or mean.
