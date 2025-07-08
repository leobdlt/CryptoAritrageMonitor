# Crypto Arbitrage Monitor

This Python script monitors real-time arbitrage opportunities between **Binance** and **Coinbase** for Bitcoin (BTC). It fetches live bid and ask prices, calculates potential arbitrage profits after trading fees, logs the data, and generates detailed plots for analysis upon exiting the script.

## How It Works

The script performs the following:

- **Live Price Fetching**  
  It retrieves real-time bid and ask prices for BTC/USDT from Binance and BTC-USD from Coinbase using the CCXT library.

- **Arbitrage Calculation**  
  It evaluates two potential arbitrage directions:
  - **Buy on Binance, Sell on Coinbase**
  - **Buy on Coinbase, Sell on Binance**  
  It adjusts prices to account for exchange fees and calculates profit margins.

- **Data Logging**  
  Every 30 seconds, the script logs:
  - Timestamps
  - Bid/ask prices from both exchanges
  - Arbitrage direction with the best potential
  - Potential profit percentage

- **Graphical Analysis Upon Exit**  
  When you stop the script (via `Ctrl+C`), it generates three time series plots:
  1. **BTC Bid/Ask Prices Over Time**
  2. **Exchange Spreads Over Time**
  3. **Arbitrage Profit Potential Over Time**  
  It also prints summary statistics, including:
  - Average potential profit
  - Maximum observed profit
  - Count of opportunities exceeding 0.1% profit

## Requirements

Install the required packages:

```bash
pip install ccxt pandas matplotlib
