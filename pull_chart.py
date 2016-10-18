###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: pull_chart.py
# USAGE: tbd
# DESCR: holds functionality to scrape intraday stock info from barchart.com
# START DATE: 10/7/16
# CHANGE LOG:
#           10/7/16 - File started, quick experimentation with pulling data
#           10/8/16 - can successfuly pull the candlestick data for any given
#                     chart. Currently can write to csv, skeptical of this.
###--------------------------------------------------------------------------###

# IMPORTS
from bs4 import BeautifulSoup
import requests
import csv

# CONSTANTS
CANDLES_IN_DAY = 79
NUM_OF_NEXT_DAY_TO_KEEP = 6

# FUNCTIONS
def ugly_text_to_float(s):
    """
    DESCR: Probably the worst way ever to deal with strip out numbers from
           text. Strips both sides and returns the float.
    INPUT:
        s - str - something like '17.15000,'
    OUPTU:
        s - float - 17.15000
    """
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while s[0] not in nums:
        s = s[1:]
    while s[-1] not in nums:
        s = s[:-1]

    return float(s)


def pull_one_chart(symbol, minutes, start_month, start_day, start_year, end_month, end_day, end_year):
    """
    DESCR: grabs one chart worth of data
    INPUT:
        symbol - str - stock identifier ie 'AAPL'
        minutes - int - minutes of cande intervals
        start_month - int - piece of start date ie oct = 10
        start_day - int - number of day in month ie 15 = 15th
        start_year - int - ie 2016
        end_month - int
        end_day - int
        end_year - int
    OUTPUT:
        candles - list [[o,h,l,c], [o,h,l,c]]- list of cnadles
        meta - dict - meta data for chart
    """
    # build date header strings
    start_date = "{}%2F{}%2F{}".format(start_month, start_day, start_year)
    end_date = "{}%2F{}%2F{}".format(end_month, end_day, end_year)

    # Buld request url
    url = "http://www.barchart.com/chart.php?sym={}&style=technical&template=&p=I&d=L&im={}&sd={}&ed={}&size=S&log=0&t=CANDLE&v=0&evnt=1&late=1&o1=&o2=&o3=&sh=100&indicators=&addindicator=&submitted=1&fpage=&txtDate={}#jump".format(symbol, minutes, start_date, end_date, end_date)

    # Get a page response
    response = requests.get(url)

    if response.status_code != 200:
        with open('chart_pull_errors.txt', 'a') as f:
            f.write("ERROR: problem with {}".format(url))
            f.write("   Response code: {}".format(response.status_code))
        return -1
    else:
        # Make a soup
        soup = BeautifulSoup(response.text, "lxml")

        # pull out the chart candle objects
        print url
        rects = soup.find('center').find('map').findAll('area')

        # cut down to just data display info
        candles = [rect['onmousemove'] for rect in rects]

        # Confirm size
        if len(candles) < 156:
            with open('chart_pull_errors.txt', 'a') as f:
                f.write("ERROR: problem with {}".format(url))
                f.write("   Only contains {} candles\n".format(len(candles)))
            return -2

        else:

            # Why are these stupid things backwars?
            candles.reverse()

            # Split into useful stuff
            candles = [candle.split(', ')[2:] for candle in candles]

            # Save meta data
            meta = {}
            meta['first_day'] = candles[0][0][2:]
            meta['year'] = candles[0][1][:4]
            meta['symbol'] = candles[0][2][1:-1]
            meta['second_day'] = candles[79][0][2:]

            # Chop this now redundant stuff
            candles = [candle[3:] for candle in candles]

            # convert to nums
            candles = [[ugly_text_to_float(num) for num in candle] for candle in candles]

            if len(candles) == 157 or len(candles) == 156:
                if len(set(candles[78])) != 1:
                    new_candle = [candles[77][-1]]*4
                    candles = candles[:78] + [new_candle] + candles[78:]


            # Keep just the day and the desired next day
            candles = candles[:CANDLES_IN_DAY + NUM_OF_NEXT_DAY_TO_KEEP]

            return candles, meta





if __name__ == '__main__':
    """
    DESCR: Test of code to pull candlestick data
    """
    start_day = 6
    end_day = 7
    start_month = 3
    end_month = 3
    start_year = 2014
    end_year = 2014
    symbol = 'AAPL'
    minutes = 5

    candles, meta = pull_one_chart(symbol, minutes, start_month, start_day, start_year, end_month, end_day, end_year)
    candles.append(meta)


    # write to file
    header_row = [str(x) for x in range(CANDLES_IN_DAY+NUM_OF_NEXT_DAY_TO_KEEP)]
    header_row.append('meta')

    f = open('chart_csv.csv', 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow(header_row)
        writer.writerow( candles )

    finally:
        f.close()
