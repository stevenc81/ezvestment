import getdata
import math
import numpy as np

#
# Constants
#
# yield from 3 months treasury
RFR = 0.05

# 2012 yeild for S&P 500
ERM = 13.4

BENCH_TICKER = '^GSPC'

dataPath = 'data/'


class StockModel():
    def __init__(self, ticker, ticker_history, bench_history, rfr, erm):
        self.ticker = ticker
        self.ticker_history = np.array(ticker_history)
        self.bench_history = np.array(bench_history)
        self.rfr = rfr
        self.erm = erm

        self.expected_return = 0
        self.daily_volatility = 0
        self.beta = 0

        self._calculate_performance()

    def get_ticker(self):
        return self.ticker

    def get_expected_return(self):
        return self.expected_return

    def get_daily_volatility(self):
        return self.daily_volatility

    def get_beta(self):
        return self.beta

    def _calculate_return(self):
        daily_returns = []

        for i in range(len(self.ticker_history) - 1):
            perc_return = math.log(self.ticker_history[i + 1] / self.ticker_history[i])
            daily_returns.append(perc_return)

        return np.array(daily_returns)

    def _calculate_beta(self, daily_returns):
        bench_returns, returns = self._make_same_size_array(self.bench_history, daily_returns)

        covarianceMatrix = np.cov(returns, bench_returns)
        covariance = covarianceMatrix[0][1]

        beta = covariance / np.var(bench_returns)

        return beta

    def _calculate_expected_return(self, beta):
        return self.rfr + beta * (self.erm - self.rfr)

    def _calculate_performance(self):
        daily_returns = self._calculate_return()
        self.daily_volatility = daily_returns.std()
        self.beta = self._calculate_beta(daily_returns)

        self.expected_return = self._calculate_expected_return(self.beta)

    def _make_same_size_array(self, x, y):
        #based on the assumption that every company has prices up to today...
        cutArray = []
        smallArray = []

        if len(x) > len(y):
            index = len(x) - len(y)
            cutArray = x[index:]
            smallArray = y
        elif len(x) < len(y):
            index = len(y) - len(x)
            cutArray = y[index:]
            smallArray = x
        else:
            return (x, y)

        return (cutArray, smallArray)


class PortfolioModel():
    def __init__(self, tickers, bench_ticker, rfr, erm):
        getdata.get_ticker_history(tickers)
        getdata.get_ticker_history([bench_ticker])

        bench_history = []
        with open('data/' + bench_ticker + '.csv', 'r') as f:
            lines = f.readlines()

        for row in range(1, len(lines)):
            date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose = \
                lines[row].strip().split(',')
            bench_history.append(float(adjClose))

        self.stocks = []
        for ticker in tickers:
            ticker_history = []
            with open('data/' + ticker + '.csv', 'r') as f:
                lines = f.readlines()

            for row in range(1, len(lines)):
                date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose = \
                    lines[row].strip().split(',')
                ticker_history.append(float(adjClose))

            self.stocks.append(
                StockModel(
                    ticker,
                    ticker_history,
                    bench_history,
                    rfr,
                    erm))

    def get_stocks(self):
        return self.stocks


if __name__ == "__main__":

    # get_ticker_history(['CHIQ', 'FSG', 'GLD', 'GMF', 'IPK', 'TAO', 'VGK', 'VPL', 'VWO'])
    portfolio = PortfolioModel(getdata.scrape_all_vanguard_etfs(), BENCH_TICKER, RFR, ERM)

    for stock in portfolio.get_stocks():
        print "".join([
            "Ticker: ",
            stock.get_ticker(),
            " Volatility: ", str(stock.get_daily_volatility()),
            " Beta: ", str(stock.get_beta()),
            " Return: ", str(stock.get_expected_return())])

        with open('data/result.csv', 'a') as f:
            f.write("".join([
                stock.get_ticker(), ',',
                str(stock.get_daily_volatility()), ',',
                str(stock.get_expected_return()), '\n']))