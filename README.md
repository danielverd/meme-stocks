##Companion data and code files for the paper 'Influence of Twitter social network graph topologies on traditional and meme stocks during the 2021 GameStop short squeeze'.

Each subdirectory corresponds to one of the stocks included in the paper. The contents are named as follows:

XYZdedgelist.csv - the retweet graph for stock XYZ on the d-th day of the dataset 

The data and code subdirectory includes the tweet ids for the raw dataset. You can hydrate them using a tool such as twarc. It also includes files named 'XYZ.csv' for a stock XYZ. These include historical data from Yahoo Finance during our data collection timeframe. Finally, we include three code files:

createRTlist.py - generates a list of retweets from the raw data, which are used to build the retweet graph

daily-edgelists.py - generates a series of daily graphs from the raw data, calculates the relevant topological metrics, and exports as a dataframe

xyz-analysis.ipynb - Jupyter notebook used to do model fitting, prediction, plotting and validation
