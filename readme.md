# CryptoTradingPlatform_python

## Overview
An effort to perform data analysis on crypto exchanges to see if any interesting insights could be found.
Note this work does not contribute financial advice, it is simply my own analysis of incoming data and stating facts. Please feel free to use this, but at your own risk :)

## Requirements
- Python 3.8 or above
- MongoDb installed and working
- Working knowledge of python

## What it does so far
- Gathers data from binance and coinbase using their publically available REST API
- Stores data in community version of MongoDb
- Runs a single algorithm over gathered data from previous five hours to see if a trade is recommended
- Store logs about the application in either the MongoDb (for permanent logging) or app.log (for test logging)
- Getting data from coinbase and binance and analysing incoming data for buy recommendations multithreaded
- Basic command line interface created, although it needs heaps more work

## What is up next?
1. Implementation of confirmation analysis. I.e. are these trading recommendations historically more effective than HODLing?
2. Dynamic parallelization of analysis
3. Integration with the GolemProject for massive parallelization of the algorithm checking. This is particularly intersting with the Golem TaskAPI: https://taskapi.docs.golem.network/#task-api
4. Implementation of more algorithms
5. Turn into a self contained binary for ease of use

## What is Algorithm One
- Hypothesis: If the price of a token _in any currency_ rises by more than a specified value for two hours, it will rise in the third hour
- Options: User specifies tolerance 
### What exists so far
1. Can analyse incoming data against previous five hours to see if a buy recommendation should be made. For ~818 tokens this takes ~90 seconds

## Usage
Usage is pretty basic so far, and not yet setup for those not confident with Python and basic setup. Clone into a directory using git clone commands. 
Make sure you have MongoDB installed
Run main.py with `python3 main.py`
Install whatever extra libraries you might need
Play around feel free to provide feedback
