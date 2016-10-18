###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: clean_stock_streams.py
# USAGE: python clean_stock_streams.py <data_path> <save_path> <norm_flag>
#                                      <zero_flag> <lower_flag> <flatten>
#                                      <meta_flag>
# DESCR: Will perform desired alterations to conver csv stock data into a more
#             usable format for modeling algorithms
# START DATE: 10/9/16
# CHANGE LOG:
#           10/9/16 - not sure what to do, but first off will need to figure out
#                     how to put stocks on omparable scaling, and then work on
#                     modeling algorithm
#           10/12/16 - Not much progress here yet, but ensured that pickling a
#                      dataframe full of candlesticks does work
#           10/15/16 - Will load in given csv file and convert string data into
#                      candles, then adjust end of day candle. Other processing
#                      steps occur only if given flag is pass in command line
###--------------------------------------------------------------------------###

# IMPORT SECTION
import pandas as pd
from ast import literal_eval
import cPickle as pickle
from candlestick import CandleStick
import sys
from helper_functions import end_of_day_adjust, zero_chart, normalize_chart
from helper_functions import flatten_candle_df_to_float_df
from time import time

# CONSTANT SECTION
RECOGNIZED_FLAGS = ["-norm", "-zero", "-lower", "-flatten", "-meta"]

# FUNCTION SECTION

# MAIN DRIVER CODE
if __name__ == '__main__':
    start_time = time()

    # Load in the data file
    try:
        data_file = sys.argv[1]
        save_file = sys.argv[2]
        flags = []
        if len(sys.argv) > 3:
            flags = sys.argv[3:]
            for flag in flags:
                if flag not in RECOGNIZED_FLAGS:
                    print "{} not recognized".format(flag)
    except Exception as e:
        print "ERROR: Usage python clean_stock_streams.py <file_path> <save_path> <norm_flag> <zero_flag> <lower_flag> <flatten> <meta_flag>"
        print "Exception: {}".format(e)
        sys.exit(-1)

    try:
        print "READING IN DATA....."
        df = pd.read_csv(data_file)
        print "   READ IN {} rows and {} columns".format(df.shape[0], df.shape[1])

    except Exception as e:
        print "ERROR: problem on file open"
        print "EXCEPTION: {}".format(e)
        sys.exit(-2)

    # Pop off the meta data column
    print "Meta data column removed..."
    meta = df.pop('meta')

    # Convert to candles
    print "Converting String data to candles..."
    df = df.applymap(literal_eval)
    df = df.applymap(lambda x: CandleStick(x[0], x[1], x[2], x[3]))

    # Adjust end of day and reshow
    print "Adjusting end of candle..."
    df = df.apply(func=end_of_day_adjust, axis=1)

    # Zero (Whole chart lowered by min(chart))
    if "-zero" in flags:
        print "Zeroing all charts..."
        df = df.apply(func=zero_chart, axis=1)

    # Normalize (Whole chart shifted from min-max to 0-100 scale)
    if "-norm" in flags:
        print "Normalizing all charts..."
        df = df.apply(func=normalize_chart, axis=1)

    # Lower (all candles low point moved to 0)
    if "-lower" in flags:
        print "Lower all candles to zero..."
        df = df.applymap(lambda x: x.shift_to_zero())

    # Flatten (each candle o, h, l, c attributes expanded to own columns)
    if "-flatten" in flags:
        print "Flattening all columns to many colums..."
        df = flatten_candle_df_to_float_df(df)

    # Pickle altered data frame
    print "Saving altered dataframe as {}".format(save_file + ".pkl")
    df.to_pickle(save_file + ".pkl")

    # Save meta data
    if "-meta" in flags:
        print "Saving metadata as {}".format(save_file + "_meta.pkl")
        meta.to_pickle(save_file + "_meta.pkl")

    # Conversion time
    end_time = time()
    print "Conversion time: {} seconds".format(end_time-start_time)
