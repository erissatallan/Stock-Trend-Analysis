import pandas as pd
import numpy as np
import yfinance as yf
from IPython.display import display


def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start_date, end_date)
    return stock_data


def moving_average_strategy(stock_data, short_window, long_window):
    signals = pd.DataFrame(index = stock_data.index) # the index is the date column, the column will be the same for the two dfs
    
    signals['signal'] = 0.0

    # calculating the short-term moving average (short_mavg) of the closing prices and storing the result in the 'short_mavg' column
    signals['short_mavg'] = stock_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = stock_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # consider weighting the order by the fraction of total shares traded on that day
    # all values from the short_window index on will be assigned the value on the right
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] <
                                                 signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()  # only trade when there is a change in value, else hold position

    return signals


def backtest_strategy(signals, intial_capital=100000):
    positions = pd.DataFrame(index = signals.index).fillna(0.0)
    positions['TSLA'] = 100 * signals['signal']

    # to calculate the value of the portfolio based on the number of shares held and their respective adjusted closing prices
    portfolio = positions.multiply(stock_data['Adj Close'], axis=0)
    portfolio['holdings'] = portfolio.sum(axis=1)

    portfolio['cash'] = intial_capital - (positions.diff().multiply(stock_data['Adj Close'], axis=0)).sum(axis=1).cumsum()

    portfolio['total'] = portfolio['cash'] + portfolio['holdings']

    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio

    

if __name__ == '__main__':
    ticker = 'TSLA'
    start_date = '2021-1-1'
    end_date = '2023-12-31'
    short_window = 40
    long_window = 100

    stock_data = get_stock_data(ticker, start_date, end_date)
    print(f"Stock data: {stock_data}")

    signals = moving_average_strategy(stock_data, short_window, long_window)
    print(f"Signals: {signals}")

    portfolio = backtest_strategy(signals)

    print(portfolio.tail(10))


""" stock_data = yf.download('TSLA', '2023-1-1', '2023-1-5')
print(stock_data['Volume'])
info = stock_data.info
print(f"Total number of shares {info}")
display(stock_data) """