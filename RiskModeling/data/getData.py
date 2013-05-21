import requests
import datetime
import re
from BeautifulSoup import BeautifulSoup


def scrape_free_etfs():
    tickers = []

    results = requests.get(
        "https://www.firstrade.com/content/en-us/freeetfs")
    soup = BeautifulSoup(results.text)
    tags = soup(
        "a",
        {"class": re.compile(r"^.*free_etf.*$")})

    for tag in tags:
        tickers.append(str(tag.text))

    return tickers


def get_ticker_history(tickers=["^GSPC"]):
    enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(365*4)

    for ticker in tickers:
        results = requests.get(
            "http://ichart.finance.yahoo.com/table.csv",
            params={'s': ticker,
                    'a': startdate.month-1,
                    'b': startdate.day,
                    'c': startdate.year,
                    'd': enddate.month-1,
                    'e': enddate.day,
                    'f': enddate.year,
                    'g': 'd',
                    'ignore': '.csv'})
        filehandle = open('data/' + ticker + '.csv', 'w')
        filehandle.write(results.text)
        filehandle.close()


if __name__ == "__main__":
    get_ticker_history(scrape_free_etfs())
