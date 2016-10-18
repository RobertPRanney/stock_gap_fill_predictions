###--------------------------------------------------------------------------###
# AUTHOR: Robert Ranney
# FILE: cluster_attempt.py
# USAGE: tbd
# DESCR: initial attempt to cluster charts
# START DATE: 10/15/16
# CHANGE LOG: python cluster_attempt.py <data_pickle> <cluster_save_path>
#                                       <num_clusters> -flags
#           10/15/16 - initial attempt to try and cluster 340 feature data set
###--------------------------------------------------------------------------###

# IMPORT SECTION
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import warnings
import cPickle as pickle
import sys
from helper_functions import day_split
from scipy.spatial.distance import pdist, cosine, euclidean
from copy import copy
from collections import Counter

# CONSANT SECTION
RANDOM_STATE = 42
RECOGNIZED_FLAGS = ["-weight", "-all"]

# FUNCTION SECTION
def weight_features(X, adjust=0.03):
    """
    DESCR: Attempt to weight feature matrix so that features near start of day
           matter less that features near end of day
    """
    # Create potentail weights vector
    weights = []
    adjust = adjust
    for i in range(X.shape[1] / 4):
        weights.extend([adjust]*4)
        adjust = adjust * (1-adjust)
    weights.reverse()
    weights = np.array(weights)

    return X.apply(axis=1, func=lambda x: x * weights)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    try:
        data_pickle = sys.argv[1]
        cluster_save_path = sys.argv[2]
        num_clusters = int(sys.argv[3])
        flags = []
        if len(sys.argv) > 4:
            flags = sys.argv[4:]
            for flag in flags:
                if flag not in RECOGNIZED_FLAGS:
                    print "{} not recognized".format(flag)
    except:
        print "ERROR Usage: python cluster_attempt.py <data_pickle> <cluster_save_path> <num_clusters>"
        sys.exit(-1)


    # Load in data
    print "Loading in data..."
    df = pd.read_pickle(data_pickle)
    print "   Data has shape: {}".format(df.shape)

    # Split into cluster features and target day
    print "Data split to X and y"
    X, y = day_split(df)
    X_old = copy(X)

    if "-weight" in flags:
        print "Weighting Feature Matrix..."
        X = weight_features(X)

    if "-all" not in flags:
        # Initialize cluster object
        cluster = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10,
                         max_iter=300, tol=0.0001, precompute_distances=True,
                         verbose=1,random_state=RANDOM_STATE, copy_x=True,
                         n_jobs=-1)

        # Fit to feature matrix
        cluster.fit(X)

        # Calc metrics
        sizes = Counter(cluster.labels_)

        X_mean_distance = np.mean([np.mean(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        X_max_distance = np.mean([max(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        X_min_distance = np.mean([np.min(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])

        X_mean_sim = np.mean([np.mean(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        X_max_sim = np.mean([max(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        X_min_sim = np.mean([min(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])

        y_mean_distance = np.mean([np.mean(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        y_max_distance = np.mean([max(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        y_min_distance = np.mean([np.min(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)])

        y_mean_sim = np.mean([np.mean(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        y_max_sim = np.mean([max(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])
        y_min_sim = np.mean([min(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)])

        min_size = min(sizes.values())
        max_size = max(sizes.values())
        mean_size = np.mean(sizes.values())

        print "                      SUMMARY                             "
        print "      X_min    X_max    X_mean    y_min   y_max    x_mean"
        print "euc:  {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}    ".format(X_min_distance, X_max_distance, X_mean_distance, y_min_distance, y_max_distance, y_mean_distance)
        print "sim:  {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}    ".format(X_min_sim, X_max_sim, X_mean_sim, y_min_sim, y_max_sim, y_mean_sim)
        print "mean size: {}, min_size: {}, max_size: {}".format(mean_size, min_size, max_size)

        # Save
        pickle.dump(cluster, open(cluster_save_path, 'wb') )

    else:
        X_mean_distances = []
        X_max_distances = []
        X_min_distances = []
        X_mean_sims = []
        X_max_sims = []
        X_min_sims = []
        y_mean_distances = []
        y_max_distances = []
        y_min_distances = []
        y_mean_sims = []
        y_max_sims = []
        y_min_sims = []
        min_sizes = []
        max_sizes = []
        mean_sizes = []

        for i in range(25,num_clusters,25):
            # Initialize cluster object
            print "K = {}".format(i)
            cluster = KMeans(n_clusters=i, init='k-means++', n_init=10,
                             max_iter=300, tol=0.0001, precompute_distances=True,
                             verbose=0,random_state=RANDOM_STATE, copy_x=True,
                             n_jobs=-1)

            # Fit to feature matrix
            cluster.fit(X)

            # Calc metrics
            sizes = Counter(cluster.labels_)

            X_mean_distances.append(np.mean([np.mean(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            X_max_distances.append(np.mean([max(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            X_min_distances.append(np.mean([np.min(pdist(X[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))

            X_mean_sims.append(np.mean([np.mean(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            X_max_sims.append(np.mean([max(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            X_min_sims.append(np.mean([min(pdist(X[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))

            y_mean_distances.append(np.mean([np.mean(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            y_max_distances.append(np.mean([max(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            y_min_distances.append(np.mean([np.min(pdist(y[cluster.labels_==i],euclidean)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))

            y_mean_sims.append(np.mean([np.mean(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            y_max_sims.append(np.mean([max(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))
            y_min_sims.append(np.mean([min(pdist(y[cluster.labels_==i],cosine)) if sizes[i] > 1 else 0 for i in range(num_clusters)]))

            min_sizes.append(min(sizes.values()))
            max_sizes.append(max(sizes.values()))
            mean_sizes.append(np.mean(sizes.values()))
