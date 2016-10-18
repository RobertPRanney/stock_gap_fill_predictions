###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: pull_all_data.py
# USAGE: python pull_all_data <save_file_name> <symb_start_ind> <symb_end_ind>
# DESCR: functions to pull whole desired data set off of bar chart and store in
#        a desired format
# START DATE: 10/8/16
# CHANGE LOG:
#           10/8/16 - file initiated
###--------------------------------------------------------------------------###

# IMPORT SECTION
import datetime
import pull_chart
from pull_chart import CANDLES_IN_DAY, NUM_OF_NEXT_DAY_TO_KEEP
import csv
from time import time
from concurrent.futures import ThreadPoolExecutor
import sys

# CONSTANTS
STOCK_SYMBOLS_FILE = 'SP_stock_symbols.txt'


def get_stock_symbols(file_name):
    """
    DESCR: from a text file of just symbols on their own lines create list of
           symbols for use
    INPUT:
        file_name - str - location to text file
    OUTPUT:
        stocks - list - [str, str] - symbols
    """
    with open(file_name, 'r') as f:
        stocks = f.read().strip().split('\n')

    return stocks


def pull_and_record_chart(writer, symb, minutes, date_pair):
    """
    DESCR: pull a desired stock and write to given csv
    INPUT:
        writer - csv_writer_ojbect - where will chart go
        symb - str - stock desigator
        minutes - int - canclestick interval length
        date_pair - tuple - (date_start, date_end)
    OUTPUT: none
    """
    try:
        data, meta = pull_chart.pull_one_chart(symb,
                                    minutes,
                                    date_pair[0].month,
                                    date_pair[0].day,
                                    date_pair[0].year,
                                    date_pair[1].month,
                                    date_pair[1].day,
                                    date_pair[1].year)
        data.append(meta)
        writer.writerow( data )
    except Exception as e:
        print e


if __name__ == '__main__':
    save_name = sys.argv[1]
    start_ind = int(sys.argv[2])
    end_ind = int(sys.argv[3])

    # Get all symols for data collection
    symbols = get_stock_symbols(STOCK_SYMBOLS_FILE)
    symbols = symbols[start_ind:end_ind]

    # Designate data collections ranges
    start_date = datetime.datetime(2014, 1, 1)
    end_date = datetime.datetime(2016, 10, 1)
    gap = end_date - start_date
    days_gap = gap.days
    weekdays = set([0,1,2,3,4])

    # Create a list of date pairs to query data from
    date_list = [start_date + datetime.timedelta(days=x) for x in range(0, days_gap) if (start_date + datetime.timedelta(days=x)).weekday() in weekdays]
    date_pairs = zip(date_list[:-1], date_list[1:])


    # Create csv header row
    header_row = [str(x) for x in range(CANDLES_IN_DAY+NUM_OF_NEXT_DAY_TO_KEEP)]
    header_row.append('meta')

    # Make a csv writer object
    f = open(save_name, 'wt')
    writer = csv.writer(f)
    writer.writerow(header_row)

    start_time = time()

    for symb in symbols:
        # Make 10 threads to grab and record all of this
        with ThreadPoolExecutor(max_workers=5) as executor:
            for num, date_pair in enumerate(date_pairs):
                executor.submit(pull_and_record_chart, writer, symb, 5, date_pair)
                print "\n\n Chart {}: Getting info for {}".format(num, date_pair)

    f.close()

    end_time = time()

    print "  Stock pull in: {}".format(end_time-start_time)
