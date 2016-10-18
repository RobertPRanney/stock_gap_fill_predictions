###--------------------------------------------------------------------------###
# FILE: custom_candle_kmeans.py
# AUTHOR: Robert Ranney
# USAGE: tbd
# DESCR: Attempt to create kmeans algorithm using candle stick objects as
#        features.
# START DATE: 10/15/16
# CHANGE LOG:
#           10/15/16 - File initiated, using sklearn kmeans as roadmap
###--------------------------------------------------------------------------###

# IMPORT SECTION
import numpy as np
import numbers

# CONSTANTS



# functions
def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance
    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.
    Otherwise raise ValueError.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)

# class
class kmeans(object):
    def __init__(self, n_clusters=8, init='k-means++', n_init=10, max_iter=300,
                 tol=1e-4, precompute_distances='auto', verbose=0,
                 random_state=None, copy_x=True, n_jobs=1, algorithm='auto'):
        self.n_clusters = n_clusters
        self.init = init
        self.max_iter = max_iter
        self.tol=tol
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.verbose = verbose
        self.random_state = random_state
        self.copy_x = copy_x
        self.n_jobs = n_jobs
        self.algorithm = algorithm

    def _check_fit_data(self, X):
        """verfiy we have enough data ie samples > k"""
        #** skleanr checks array here, will not do
        if X.shape[0] < self.n_clusters:
            raise ValueError("n_samples={} should be >= n_clusers={}".format(
                              X.shape[0], self.n_clusters))
        return X

    def _check_test_data(self, X):
        #** skipping check array portion
        n_samples, n_features = X.shape
        expected_n_features = self.cluster_centers_.shape[1]
        if  not n_features == expected_n_features:
            raise ValueError("Incorrect number of features. "
                             "Got {} features, expected {}".format(
                             n_features, expected_n_features))
        return X

    def fit(self, X, y=None):
        """ Compute custom candle k_means clustering
        X: array-like, shape=(n_samples, n_features)
        """




# DRIVER CODE
if __name__ == '__main__':
    pass
