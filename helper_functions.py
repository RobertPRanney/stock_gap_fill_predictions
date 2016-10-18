###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: helper_functions.py
# USAGE: IPython: run helper_functions.py or from helper_functions import <func>
# DESCR: functions to play with charts
# START DATE: 10/11/16
# CHANGE LOG:
#           10/11/16 - Right now just need a spot to store normalizing functions
#                    - Can now extend end of day candle, can normalize
#                    - Can remove magnitude to only care about Sequence
#           10/12/16 - Added function to average a list of candles
#                    - Added fuction to average multiple charts
#           10/15/16 - Can flatten a recreate candles in df -- should help
#                      if only want to use built in ML algs
#           10/16/16 -
###--------------------------------------------------------------------------###

# IMPORT SECTION
from __future__ import division
from candlestick import CandleStick
import pandas as pd
from ast import literal_eval
from chart_plotter import build_candle_chart
import matplotlib.pyplot as plt

# CONSTANT SECTION
TEST_CHART1 = 333
TEST_CHART2 = 888
TEST_CHART3 = 1234

# FUNCTION SECTION
def end_of_day_adjust(row, ind=78):
    """
    DESCR: changes a chart so that final day price will also reflect overnight
           price movement
    INPUT:
        row - list-like of CandleSticks - un adjusted row
        ind - int - end of day candle needing adjustment
    OUTPUT:
        row - list-like of CandleSticks - end of day adjusted row
    """
    open_price = row[ind].open_price
    close_price = row[ind + 1].open_price
    if open_price <= close_price:
        low = open_price
        high = close_price
    else:
        low = close_price
        high = open_price
    row[ind] = CandleStick(open_price, high, low, close_price)

    return row


def normalize_chart(row):
    """
    DESCR: Normalize charts so that scale of changes is not part of the effect
    INPUT:
        row - array like of candles - raw magnitudes
    OUTPUT:
        row - arrat like of candles - normed magnitudes
    """
    top = max([candle.high for candle in row])
    bot = min([candle.low for candle in row])
    row = (row - bot)*100 / (top-bot)

    return row

def zero_chart(row):
    """
    DESCR: shift chart min to zero for better comparison
    INPUT:
        row - array like of candles - raw magnitudes`
    OUTPUT:
        row - array like of candles - candles minus min of chart
    """
    bot = min([candle.low for candle in row])
    row = row - bot

    return row


def average_candles(candles):
    """
    DESCR: can take a list of candles and return a single candle
    INPUT:
        candles - array like of candles
    OUTPUT:
        candle - CandleStick - all atributes averaged
    """
    number = len(candles)

    open_price = sum([candle.open_price for candle in candles]) / number
    high = sum([candle.high for candle in candles]) / number
    low = sum([candle.low for candle in candles]) / number
    close_price = sum([candle.close_price for candle in candles]) / number

    return CandleStick(open_price, high, low, close_price)

def average_charts(charts):
    """
    DESCR: Will average any number of provided charts
    INPUT:
        charts - df - dataframe full of candlesticks
    OUTPUT:
        chart - series - seires of candlesistkcs
    """
    return charts.apply(average_candles, axis=0)


def flatten_candle_df_to_float_df(df):
    """
    DESCR: Will take a dataframe of candles and turn it into a df of floats
    INPUT:
        df - dataframe, full of candle objects
    OUTPUT:
        df - dataframe, full of floats
    """
    original_cols = df.columns.tolist()

    for col in original_cols:
        name = col + '_' + 'o'
        df[name] = df[col].apply(lambda x: x.open_price)
        name = col + '_' + 'h'
        df[name] = df[col].apply(lambda x: x.high)
        name = col + '_' + 'l'
        df[name] = df[col].apply(lambda x: x.low)
        name = col + '_' + 'c'
        df[name] = df[col].apply(lambda x: x.close_price)

    df = df.drop(original_cols, axis=1)
    return df

def merge_float_df_to_candles(df):
    """
    DESCR: Will recombine 4 columns into one candle
    """
    original_cols = df.columns.tolist()
    new_cols = [str(col) for col in range(int(len(df.columns)/4))]

    for ind, col in enumerate(new_cols):
        df[col] = zip(df.iloc[:,ind*4],
                   df.iloc[:,(ind*4)+1],
                   df.iloc[:,(ind*4)+2],
                   df.iloc[:,(ind*4)+3])

    df = df.drop(original_cols, axis=1)
    df = df.applymap(func=lambda x: CandleStick(x[0],x[1], x[2], x[3]))

    return df

def day_split(df):
    """
    DESCR: takes dataframe and returns first day as X, and second as y
    """
    suffixes = ['_o', '_h', '_l', '_c']
    x_cols = [[str(x)+suffix for suffix in suffixes] for x in range(0,79,1)]
    x_cols = [col for sublist in x_cols for col in sublist]
    y_cols = [[str(x)+suffix for suffix in suffixes] for x in range(79,85,1)]
    y_cols = [col for sublist in y_cols for col in sublist]

    X = df.drop(y_cols, axis=1)
    y = df.drop(x_cols, axis=1)
    return X, y

def float_chart_to_candle_chart(chart):
    """
    DESCR: Take a single chart (series) of floats and merge them to candles
    """
    candles = [chart[x:x+4] for x in range(0,len(chart),4)]
    candles = pd.Series([CandleStick(x[0], x[1], x[2], x[3]) for x in candles])
    return candles

if __name__ == '__main__':
    """
    DESCR: Test code for helper functions
    """
    # Plot to keep track of changes
    master_fig, master_ax = plt.subplots(nrows=3,
                                         ncols=3,
                                         sharex=True,
                                         figsize=(18,13))
    master_fig.text(0.5, 0.04, 'Time 5 Minute Intervals', ha='center')
    master_fig.text(0.04, 0.5, 'Price')

    # Load in data
    df = pd.read_csv("data/test_set.csv")

    # Pop off chart meta column
    meta = df.pop('meta')

    # Change strings to lists then to cnadles
    df = df.applymap(literal_eval)
    df = df.applymap(lambda x: CandleStick(x[0], x[1], x[2], x[3]))

    # Add an unaltered version to the chart
    test_row = df.iloc[TEST_CHART1, : ]
    build_candle_chart(master_fig, master_ax[0][0], test_row)
    master_ax[0][0].set_ylabel('Raw Price in USD')
    master_ax[0][0].set_title('Raw Un-Altered Data')

    # Adjust end of day and reshow
    df = df.apply(func=end_of_day_adjust, axis=1)
    test_row = df.iloc[TEST_CHART1, : ]
    build_candle_chart(master_fig, master_ax[0][1], test_row)
    master_ax[0][1].set_ylabel('Raw Price in USD')
    master_ax[0][1].set_title('End of Day Candle Altered')

    # See 2 chart comparison
    compare_row = df.iloc[TEST_CHART2, : ]
    build_candle_chart(master_fig, master_ax[0][2], test_row)
    build_candle_chart(master_fig, master_ax[0][2], compare_row, color='sec')
    master_ax[0][2].set_ylabel('Raw Price in USD')
    master_ax[0][2].set_title('Comparison of Raw Data')

    # Zero and recompare
    zeroed = df.apply(func=zero_chart, axis=1)
    zeroed1 = zeroed.iloc[TEST_CHART1, : ]
    zeroed2 = zeroed.iloc[TEST_CHART2, : ]
    build_candle_chart(master_fig, master_ax[1][0], zeroed1)
    build_candle_chart(master_fig, master_ax[1][0], zeroed2, color='sec')
    master_ax[1][0].set_ylabel('Prices Zeroed')
    master_ax[1][0].set_title('Comparison of Zeroed Data')

    # Normalize charts and recompare
    normed = df.apply(func=normalize_chart, axis=1)
    normed1 = normed.iloc[TEST_CHART1, : ]
    normed2 = normed.iloc[TEST_CHART2, : ]
    build_candle_chart(master_fig, master_ax[1][1], normed1)
    build_candle_chart(master_fig, master_ax[1][1], normed2, color='sec')
    master_ax[1][1].set_ylabel('Prices Normalized')
    master_ax[1][1].set_title('Comparison of Normalized Data')

    # Test averaging functions
    combined = normed.iloc[[TEST_CHART1, TEST_CHART2], :]
    single = average_charts(combined)
    build_candle_chart(master_fig, master_ax[1][2], single, color='ter')
    build_candle_chart(master_fig, master_ax[1][2], normed1, alpha=0.4)
    build_candle_chart(master_fig, master_ax[1][2], normed2, alpha=0.4, color='sec')
    master_ax[1][2].set_ylabel('Prices Normalized')
    master_ax[1][2].set_title('Averaged Normed Charts')

    # Only sequence of candles matters maybe
    desequenced = normed.applymap(lambda x: x.shift_to_zero())
    shifted1 = desequenced.iloc[TEST_CHART1, : ]
    shifted2 = desequenced.iloc[TEST_CHART2, : ]
    build_candle_chart(master_fig, master_ax[2][0], shifted1)
    build_candle_chart(master_fig, master_ax[2][1], shifted2)
    master_ax[2][0].set_ylabel('No Relative Magnitudes')
    master_ax[2][0].set_title('Look at Candle Sequence')
    master_ax[2][1].set_ylabel('No Relative Magnitudes')
    master_ax[2][1].set_title('Look at Candle Sequence')

    # Average Candle Sequence
    combined = desequenced.iloc[[TEST_CHART1, TEST_CHART2], :]
    sequence_average = average_charts(combined)
    build_candle_chart(master_fig, master_ax[2][2], sequence_average)
    master_ax[2][2].set_ylabel('No Relative dollars')
    master_ax[2][2].set_title('Averaged DeSeqeunced Charts')

    # See All changes
    plt.tight_layout()
    plt.show()

    # Test Flattening
    print "Normed df has {} features".format(normed.shape[1])
    flat = flatten_candle_df_to_float_df(normed)
    print "Flatened df has {} features".format(flat.shape[1])
    unflat = merge_float_df_to_candles(flat)
    print "Recreateation df has {} features".format(unflat.shape[1])

    # Test Pickling
    unflat.to_pickle("pickle_pile/df_pickle_test.pkl")

    reopen = pd.read_pickle("pickle_pile/df_pickle_test.pkl")
