# CryptoTradingPlatform_python

## Overview
An effort to perform data analysis on crypto exchanges to see if any interesting insights could be found
I plan to turn this into a small revenue gathering mechanism for myself, so open to suggestions on how this might occur

## Requirements
- Python 3.8 or above
- MongoDb installed and working
- Working knowledge of python

## What it does so far
- Gathers data from binance and coinbase using their publically available REST API
- Stores data in community version of MongoDb
- Runs a single algorithm over gathered data from previous four hours to see if a trade is recommended
- stores a variety of interesting infomration in app.log which will be created in the same directory as this is cloned to

## What is up next?
- Implementation of parallel processing. This will ensure that data gathering is performed separately from analysis
- Implementation of confirmation analysis. I.e. are these trading recommendations historically more effective than HODLing?
- Potential integration with the GolemProject once computer requirements start expanding. This is particularly exciting with their recent implementation of the TaskAPI
- Implementation of more algorithms

## What is Algorithm One
**Hypothesis: ** If the price of a token _in any currency_ rises by more than a specified value for two hours, it will rise in the third hour
**Options: ** User specifies tolerance 