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
        tds = tr('td')
        if len(tds) > 2:
            tickers.append(str(tds[2].text))

    return tickers


def scrape_all_ishare_etfs():
    tickers = []

    results = requests.get(
        "http://us.ishares.com/product_info/fund/index.htm")
    soup = BeautifulSoup(results.text)

    for tr in soup.findAll('tr'):
        tds = tr('td')
        if len(tds) > 0:
            s = str(tds[0].text)
            m = re.search(r'\(([A-Z]+)\)', s)
            tickers.append(m.group(1))

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
