###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: chart_plotter.py
# USAGE: import chart_plotter
# DESCR: Will Plot candles sticks, may add different charts in future
# START DATE: 10/7/16
# CHANGE LOG:
#           10/7/16 - Initiated a file to plot candlestick charts
#           10/11/16 - Changed to plot candlestick objects instead of lists
#           10/12/16 - Plot now excepts 3 different color pairs (prim, sec, ter)
###--------------------------------------------------------------------------###

# IMPORT SECTION
from candlestick import CandleStick
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from ast import literal_eval

# FUNCTION SECTION
def add_candle_to_plot(ax, open_price, high, low, close_price, x, color='prim', alpha=1):
    """
    DESCR: Add a single candle to a given axis
    INPUT:
        ax - matplotlib axes object - desire are to place candle
        open_price - float - start price
        high - float - highest price reached
        low - float - lowest reached
        close_price - float - final price
        x - int - relative location of candle
    OUTPUT: none
    """

    if color == 'prim':
        colors = ['g', 'r']
    elif color == 'sec':
        colors = ['limegreen', 'deeppink']
    else:
        colors = ['chartreuse', 'hotpink']

    if open_price < close_price:
        ax.add_patch(patches.Rectangle(xy=(x, open_price),
                                       width=1,
                                       height=close_price - open_price,
                                       facecolor=colors[0],
                                       edgecolor='k',
                                       alpha=alpha))
        ax.vlines(x=x+0.5, ymin=close_price, ymax=high, linewidth=1, color='k', alpha=alpha)
        ax.vlines(x=x+0.5, ymin=low, ymax=open_price, linewidth=1, color='k', alpha=alpha)

    else:
        ax.add_patch(patches.Rectangle(xy=(x, close_price),
                                       width=1,
                                       height=open_price - close_price,
                                       facecolor=colors[1],
                                       edgecolor='k',
                                       alpha=alpha))
        ax.vlines(x=x+0.5, ymin=open_price, ymax=high,  linewidth=1, color='k', alpha=alpha)
        ax.vlines(x=x+0.5, ymin=low, ymax=close_price,  linewidth=1, color='k', alpha=alpha)

def build_candle_chart(fig, ax, candles, color='prim', alpha=1):
    """
    DESCR: Takes a data series and fig/ax to place it on and adds all candles
    fig - matplotlib figure object
    ax - matplotibl axes object
    data - pandas series - (89,) - all candles and some metadata
    """
    candles = candles.values.tolist()[:]

    for ind, candle in enumerate(candles):
        add_candle_to_plot(ax,
                           candle.open_price,
                           candle.high,
                           candle.low,
                           candle.close_price,
                           ind,
                           color,
                           alpha)

    ax.relim()
    ax.autoscale_view()

# MAIN DRIVER CODE
if  __name__ == '__main__':
    # Load in test set
    df = pd.read_csv('test_set.csv')
    meta = df.pop('meta')
    df = df.applymap(literal_eval)
    df = df.applymap(lambda x: CandleStick(x[0], x[1], x[2], x[3]))

    # Single Chart
    test_data = df.iloc[436, : ]
    fig, ax = plt.subplots()
    build_candle_chart(fig, ax, test_data)
    plt.show()

    # Mutliple Chart
    first = df.iloc[5, : ]
    second = df.iloc[25, : ]
    fig, ax = plt.subplots()
    build_candle_chart(fig, ax, first)
    build_candle_chart(fig, ax, second, color='sec')
    plt.show()
