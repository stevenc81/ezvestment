from data.getdata import get_ticker_history, scrape_free_etfs
import os, glob
import math
import numpy as np

dataPath = 'data/'
sp500_returns = []


class StockModel():
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = []

        filehandle = open('data/' + ticker + '.csv', 'r')
        lines = filehandle.readlines()

        for row in range(1, len(lines)):
            date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose = lines[row].strip().split(',')
            self.data.append(float(adjClose))

        filehandle.close()

        self._calculate_performance()

    def _calculate_return(self):
        daily_returns = []

        for i in range(len(self.data) - 1):
            perc_return = math.log(self.data[i+1]/self.data[i])
            daily_returns.append(perc_return)

        return daily_returns

    def _calculate_beta(self):
        bench_returns, returns = make_same_size_array(np.array(sp500_returns), self.daily_returns)

        covarianceMatrix = np.cov(bench_returns, returns)
        covariance = covarianceMatrix[0][1]

        beta = covariance / np.var(bench_returns)

        return beta

    def _calculate_expected_return(self):
        beta = self.beta
        # yield from 10 yr treasury
        riskFreeRateOfInterest = 0.03
        expectedReturnMarket = 0.11

        expectedReturn = riskFreeRateOfInterest + beta*(expectedReturnMarket - riskFreeRateOfInterest)
        return expectedReturn

    def _calculate_performance(self):
        self.daily_returns = np.array(self._calculate_return())
        self.daily_volatility = self.daily_returns.std()
        self.beta = self._calculate_beta()
        self.expected_return = self._calculate_expected_return()


def make_same_size_array(x, y):

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

if __name__ == "__main__":
    get_ticker_history(scrape_free_etfs())
    get_ticker_history(['^GSPC'])

    filehandle = open('data/^GSPC.csv', 'r')
    lines = filehandle.readlines()
    for row in range(1, len(lines)):
            date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose = lines[row].strip().split(',')
            sp500_returns.append(float(adjClose))
    filehandle.close()

    for infile in glob.glob(os.path.join(dataPath, '*.csv')):
        ticker = infile.split('/')[1].split('.')[0]
        stockModel = StockModel(ticker)
        print "".join([
            "Ticker: ",
            stockModel.ticker,
            " Volatility: ", str(stockModel.daily_volatility),
            " Return: ", str(stockModel.expected_return)])
