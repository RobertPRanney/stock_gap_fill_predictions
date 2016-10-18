###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: cluster_attempt.py
# USAGE: tbd
# DESCR: will hopefulley allows some cluster visulization of entire dataset
#        after cluster algorthm performed on aws.
# START DATE: 10/15/16
# CHANGE LOG:
#           10/15/16 - initial attempt to try and cluster 340 feature data set
###--------------------------------------------------------------------------###

# IMPORT SECTION
import pandas as pd
from sklearn.cluster import KMeans
from helper_functions import merge_float_df_to_candles, day_split
from helper_functions import float_chart_to_candle_chart
from chart_plotter import build_candle_chart
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.offsetbox import AnchoredText
import sys
import cPickle as pickle
import numpy as np
import random

# MAIN DRIVER CODE
if __name__ == '__main__':
    try:
        data_pickle = sys.argv[1]
        cluster_pickle = sys.argv[2]
    except:
        print "ERROR Usage: python visualize_clusters.py <df_path> <cluster_path>"
        sys.exit(-1)

    # Load in data
    df = pd.read_pickle(data_pickle)
    X, y = day_split(df)
    cluster = pickle.load( open(cluster_pickle, 'rb') )

    # Create dictionary of cluster sizes
    sizes = Counter(cluster.labels_)

    # Create dataframe of cluster centers converted to candles
    centers = pd.DataFrame(cluster.cluster_centers_)
    centers = merge_float_df_to_candles(centers)

    # See some clusters
    for i in range(0,centers.shape[0],50):
        inds = X[cluster.labels_==i].index.tolist()
        first = float_chart_to_candle_chart(X.iloc[random.choice(inds), : ])
        second = float_chart_to_candle_chart(X.iloc[random.choice(inds), : ])
        cluster_chart = centers.iloc[i,:]
        fig, ax = plt.subplots()

        build_candle_chart(fig, ax, cluster_chart)
        build_candle_chart(fig, ax, first, color='sec', alpha=0.35)
        build_candle_chart(fig, ax, second, color='ter', alpha=0.35)
        anchored_text = AnchoredText("Cluster {}, Size: {}".format(i, sizes[i]), loc=2)
        ax.add_artist(anchored_text)
        plt.show()
