import requests
import datetime
import re
from BeautifulSoup import BeautifulSoup


def scrapeFreeETFs():
    tickers = []

    results = requests.get("https://www.firstrade.com/content/en-us/freeetfs")

    # url = "https://www.firstrade.com/content/en-us/freeetfs"
    # page = urllib2.urlopen(url)
    soup = BeautifulSoup(results.text)
    tags = soup("a", {"class": re.compile(r"^.*free_etf.*$")})

    for tag in tags:
        tickers.append(str(tag.text))

    return tickers


def getHistory(picks=["BSV"]):
    enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(365*4)

    for pick in picks:
        results = requests.get(
            "http://ichart.finance.yahoo.com/table.csv",
            params={'s': pick,
                    'a': startdate.month-1,
                    'b': startdate.day,
                    'c': startdate.year,
                    'd': enddate.month-1,
                    'e': enddate.day,
                    'f': enddate.year,
                    'g': 'd',
                    'ignore': '.csv'})
        filehandle = open('data/'+pick+'.csv', 'w')
        filehandle.write(results.text)


if __name__ == "__main__":
    getHistory(scrapeFreeETFs())
    # tickers = scrapeFreeETFs()
    # print tickers
