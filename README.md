# stock_gap_fill_predictions

Just a fun project for myself

An attempt at playing with stock data

Work so far :
* Gathered 315,000 intra-day 5 minute candlestick charts for all SP 500 stocks
this ammounts to Jan 1st 2014 to the OCT 1 2016. Gathering done through web
scraping, although maybe not the best way I thought it was good practice.
* Recreation of chart on local machine looks like below

![[example candlestick]](./images/recreation.png)

* Some options for preprocessing this data have been explore, example shown below

![[dataprocess]](./images/data_alteration_example.png)

* Small test set of 2400 charts on my computer was been used to do some intial
modeling, start idea is to cluster charts and find succint trends, that then
also have succint following morning activity. This will take some time to get
right. Probably anything resembling 'results' is a few commits off
