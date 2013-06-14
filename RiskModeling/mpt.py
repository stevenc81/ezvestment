import getdata
import math
import numpy as np

#
# Constants (finicial magic numbers)
#
# yield from 3 months treasury
RFR = 0.05
# 2012 yeild for S&P 500
ERM = 13.4
# Ticker for benchmark
BENCH_TICKER = '^GSPC'
dataPath = 'data/'


class StockModel(object):
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
        self.daily_returns = self._calculate_return()
        self.daily_volatility = self.daily_returns.std()
        self.beta = self._calculate_beta(self.daily_returns)

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


class PortfolioModel(object):
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

        self.stocks = {}
        self.mix = {}
        self.tickers = tickers
        for ticker in tickers:
            ticker_history = []
            with open('data/' + ticker + '.csv', 'r') as f:
                lines = f.readlines()

            for row in range(1, len(lines)):
                date, openPrice, highPrice, lowPrice, closePrice, volume, adjClose = \
                    lines[row].strip().split(',')
                ticker_history.append(float(adjClose))

            self.stocks[ticker] = StockModel(
                ticker, ticker_history,
                bench_history,
                rfr,
                erm)

            self.mix[ticker] = 1 / len(tickers)

    def get_stocks(self):
        return self.stocks

    def evaluate_holdings(self):
        """ This method updates the return for the portfolio
            overall, based on the weights and returns of the components
            in the portfolio.  It returns a tuple of (variance,
            portfolio_expected_return)
        """

        port_return = 0.0

        for ticker in self.tickers:
            port_return += (self.stocks[ticker].expected_return * self.mix[ticker])

        self.portfolio_return = port_return

        # variance = self.calc_variance()
        return port_return

    def calculate_marginal_utility(self, rt=0.20):
        ''' using capm def of exoected return might be in correct in sharp's
        gradiant method '''
        e_ary = np.array([self.stocks[ticker].expected_return
                         for ticker in self.tickers])

        e = np.mat(e_ary).T

        ratelist = []

        for ticker in self.tickers:
            ratelist.append(self.stocks[ticker].daily_returns.tolist())

        rates = np.array(ratelist, dtype=float)

        cv = np.cov(rates)
        C = np.mat(cv)

        mix = np.array([self.mix[ticker]
                        for ticker in self.tickers])
        x = np.mat(mix).T

        mu = e - (1/rt)*2*C*x

        return mu

    def step_port_return(self, rt=0.20, lower_bound_weight=-2.0,
                         upper_bound_weight=2.0):

        mix = np.array([self.mix[ticker]
                        for ticker in self.tickers])
        x = np.mat(mix).T

        mu = self.calculate_marginal_utility(rt)

        mubuy = -1E200
        musell = 1E200
        ibuy = 0
        isell = 0

        for i in range(len(self.tickers)):
            if x[i] < upper_bound_weight: # possible buy
                if mu[i,0] > mubuy:
                    mubuy = mu[i,0]
                    ibuy = i

            if x[i] > lower_bound_weight:  # possible sell
                if mu[i,0] < musell:
                    musell = mu[i,0]
                    isell = i

        if (mubuy-musell)<=0.0001:
            ibuy=isell=0

        s = np.zeros(mu.shape)
        s[isell]=-1.0
        s[ibuy]=1.0
        s = np.mat(s)

        rates = np.array([self.stocks[ticker].daily_returns
            for ticker in self.tickers])
        C = np.mat(np.cov(rates))

        k0 = s.T*mu
        k1 = (s.T*C*s)/rt

        amat = k0/(2*k1)
        a = amat[0,0]

        # a change of weights according to 'a' will yield a utility
        # change as indicated below.  This is not currently returned or used anywhere,
        # but it's calculated here for potential future use.
        cu = k0*a - k1*(a**2)

        symb_sell = self.tickers[isell]
        symb_buy = self.tickers[ibuy]
        if symb_sell == symb_buy:
            a = 0.0

        # Keep within the bounds
        if self.mix[symb_sell] - a < lower_bound_weight:
            a = self.mix[symb_sell] - lower_bound_weight
        if self.mix[symb_buy] + a > upper_bound_weight:
            a = upper_bound_weight - self.mix[symb_buy]

        self.mix[symb_sell] = self.mix[symb_sell] - a
        self.mix[symb_buy] = self.mix[symb_buy] + a

        #print("Recommend Sell: %s" % symb_sell)
        #print("Recommend Buy: %s" % symb_buy)
        #print("Affect on Portfolio Return: %s" % cu)

        return a


if __name__ == "__main__":

    # get_ticker_history(['CHIQ', 'FSG', 'GLD', 'GMF', 'IPK', 'TAO', 'VGK', 'VPL', 'VWO'])
    portfolio = PortfolioModel(getdata.scrape_free_etfs(), BENCH_TICKER, RFR, ERM)

    for ticker, stock in portfolio.get_stocks().iteritems():
        print "".join([
            "Ticker: ",
            ticker,
            " Volatility: ", str(stock.get_daily_volatility()),
            " Beta: ", str(stock.get_beta()),
            " Return: ", str(stock.get_expected_return())])

        with open('data/result.csv', 'a') as f:
            f.write("".join([
                stock.get_ticker(), ',',
                str(stock.get_daily_volatility()), ',',
                str(stock.get_expected_return()), '\n']))

    rt = 0.1
    lower_bound_weight = -0.50
    upper_bound_weight = 1.5
    a = 1.0
    count = 0

    while a>0.00001:
        a = portfolio.step_port_return(rt, lower_bound_weight,
                                  upper_bound_weight)

        count+=1

    result = portfolio.evaluate_holdings()
    # variance = round(result[0],3)
    ret = round(result*100.,3)

    print("Optimization completed in [ %s ] iterations." % count)
    print("Ending weights:\n%s" % portfolio.mix)
    # print("Volatility: %s and Portfolio Return: %s%%" % (np.sqrt(variance), ret))
    # opt_rate_array = portfolio.calc_port_rates()
    # print("Portfolio Rate Array:%s\n" % opt_rate_array[:10])