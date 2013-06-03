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


def scrape_all_vanguard_etfs():
    tickers = []

    results = requests.get(
        "https://personal.vanguard.com/us/funds/etf/all")
    soup = BeautifulSoup(results.text)

    for tr in soup('tr', {'class': re.compile(r'wr|ar')}, index=re.compile(r'[0-9]+')):
        for index, value in enumerate(tr('td')):
            if index == 2:
                tickers.append(str(value.text))

    return tickers


def scrape_all_ishare_etfs():
    tickers = []

    results = requests.get(
        "http://us.ishares.com/product_info/fund/index.htm")
    soup = BeautifulSoup(results.text)

    table = soup('table', id='fundListTable')
    print len(table)
    print type(table)

    for tr in table.find_all('tr'):
        for index, value in enumerate(tr('td')):
            if index == 0:
                print value.text

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
        with open('data/' + ticker + '.csv', 'w') as f:
            f.write(results.text)

if __name__ == "__main__":
    scrape_all_ishare_etfs()
    # scrape_all_vanguard_etfs()
    # get_ticker_history(scrape_all_vanguard_etfs())
