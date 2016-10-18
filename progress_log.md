# STOCK PREDICTION PROJECT PROGRESS LOG

10/7/16:
* Talked to dad about potential ways to do this, for the meantime have settled on trying to predict opening day trend.
* Looked into barchart to pull data

10/8/16:
* Can pull charts from barchart
* can make a fairly ok looking plot of candles in matplotlib

10/9/16:
* After many hiccups got aws ec2 instance to start pulling data, first was
running out of memory, then relaunched but forgot I had altere code, finally
should be working now.
* created a test set of 2400 rows on my computer to mess with in time being
* started notebook to look thru data manipulation

10/10/16:
* Full data set pulled into aws, then transfered to local. 900MB, 315,000 charts
* AWS instance terminated
* Started into eda, and little bit of chart maniupulation such as normilzation
* EDA made implementing a candle stick class desirable, made a good start on it

10/11/16:
* Data Transformations underway
* Can extend end of day candle
* Can normalize to same scale
* Can lower to only care about seqeunce

10/12/16: Now work done today

10/13&14/16:
* Minor additions to data transformations and transformations summaary graph

10/15/16:
* Have most data transofmration done, just not chart rebuild after flooring
* Have file to performed desired transformations
* Initial attempts at clustering on test set
* Can visually recreate resultant cluster centers
* Cleaning of whole set on local needed splitting
* Clustering of 1/3 data only 100 cluster is slow, so all data with 1000
  clusters is going to be need to be left to aws. Will set up for tomorrow


 TODO:
 * graph Recreateation functions
 * test clustering on floor charts
 * get cleaning and clustering running on aws
 * Need within cluster metrics
 * Need to relate clusters to target cluster metrics
 * Need to test idea of weights vector
 * Look into linkage clustering maybe
 * Read more, lots of good time series clustering papers
 
