import numpy as np
import pandas as pd
import ccxt
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize exchanges
binance = ccxt.binance()
coinbase = ccxt.coinbase()

data = {
    'timestamp': [],
    'binance_bid': [],
    'binance_ask': [],
    'coinbase_bid': [],
    'coinbase_ask': [],
    'arbitrage_opportunity': [],
    'potential_profit_pct': []
}


def get_price(exchange, symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return {
            'exchange': exchange.id,
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'timestamp': ticker['timestamp']
        }
    except Exception as e:
        print(f"Error fetching price from {exchange.id}: {e}")
        return None


def calculate_arbitrage_opportunity(binance_data, coinbase_data, fee_rate=0.001):
    """
    Calculate arbitrage opportunities in both directions
    """
    # Scenario 1: Buy on Binance, Sell on Coinbase
    buy_binance_cost = binance_data['ask'] * (1 + fee_rate)
    sell_coinbase_revenue = coinbase_data['bid'] * (1 - fee_rate)
    profit_1 = sell_coinbase_revenue - buy_binance_cost
    profit_pct_1 = (profit_1 / buy_binance_cost) * 100

    # Scenario 2: Buy on Coinbase, Sell on Binance
    buy_coinbase_cost = coinbase_data['ask'] * (1 + fee_rate)
    sell_binance_revenue = binance_data['bid'] * (1 - fee_rate)
    profit_2 = sell_binance_revenue - buy_coinbase_cost
    profit_pct_2 = (profit_2 / buy_coinbase_cost) * 100

    # Return the best opportunity
    if profit_pct_1 > profit_pct_2:
        return profit_1, profit_pct_1, "Buy Binance, Sell Coinbase"
    else:
        return profit_2, profit_pct_2, "Buy Coinbase, Sell Binance"


try:
    print("Starting arbitrage monitoring... Press Ctrl+C to stop and plot results.")

    while True:
        # Use same symbol for both exchanges (BTC/USD)
        price_binance = get_price(binance, symbol='BTC/USDT')  # Binance uses USDT
        price_coinbase = get_price(coinbase, symbol='BTC-USD')  # Coinbase Pro uses different format

        if price_binance and price_coinbase:
            timestamp = datetime.now()

            profit, profit_pct, direction = calculate_arbitrage_opportunity(
                price_binance, price_coinbase
            )

            # Store data
            data['timestamp'].append(timestamp)
            data['binance_bid'].append(price_binance['bid'])
            data['binance_ask'].append(price_binance['ask'])
            data['coinbase_bid'].append(price_coinbase['bid'])
            data['coinbase_ask'].append(price_coinbase['ask'])
            data['arbitrage_opportunity'].append(direction)
            data['potential_profit_pct'].append(profit_pct)

            print(f"Time: {timestamp.strftime('%H:%M:%S')}")
            print(f"Binance: Bid=${price_binance['bid']:.2f}, Ask=${price_binance['ask']:.2f}")
            print(f"Coinbase: Bid=${price_coinbase['bid']:.2f}, Ask=${price_coinbase['ask']:.2f}")
            print(f"Best opportunity: {direction}")
            print(f"Potential profit: {profit_pct:.4f}%")
            print("-" * 50)


        time.sleep(30)  # 30 seconds between requests

except KeyboardInterrupt:
    print("\nStopping data collection and generating plots...")

    if len(data['timestamp']) > 0:
        df = pd.DataFrame(data)

        # Create comprehensive plots
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))

        # Bid/Ask Prices
        axes[0].plot(df['timestamp'], df['binance_bid'], label='Binance Bid', color='blue', alpha=0.7)
        axes[0].plot(df['timestamp'], df['binance_ask'], label='Binance Ask', color='blue', linestyle='--', alpha=0.7)
        axes[0].plot(df['timestamp'], df['coinbase_bid'], label='Coinbase Bid', color='red', alpha=0.7)
        axes[0].plot(df['timestamp'], df['coinbase_ask'], label='Coinbase Ask', color='red', linestyle='--', alpha=0.7)
        axes[0].set_title('BTC Bid/Ask Prices Over Time')
        axes[0].set_ylabel('Price (USD)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Spread Analysis
        binance_spread = df['binance_ask'] - df['binance_bid']
        coinbase_spread = df['coinbase_ask'] - df['coinbase_bid']
        axes[1].plot(df['timestamp'], binance_spread, label='Binance Spread', color='blue')
        axes[1].plot(df['timestamp'], coinbase_spread, label='Coinbase Spread', color='red')
        axes[1].set_title('Exchange Spreads Over Time')
        axes[1].set_ylabel('Spread (USD)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # Arbitrage Opportunities
        axes[2].plot(df['timestamp'], df['potential_profit_pct'], label='Potential Profit %', color='green')
        axes[2].axhline(0, color='black', linestyle='-', alpha=0.3)
        axes[2].axhline(0.1, color='orange', linestyle='--', alpha=0.5, label='0.1% threshold')
        axes[2].set_title('Arbitrage Profit Potential Over Time')
        axes[2].set_ylabel('Profit Percentage (%)')
        axes[2].set_xlabel('Time')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        for ax in axes:
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()


        print(f"\nSummary Statistics:")
        print(f"Data points collected: {len(df)}")
        print(f"Average potential profit: {df['potential_profit_pct'].mean():.4f}%")
        print(f"Max potential profit: {df['potential_profit_pct'].max():.4f}%")
        print(f"Profitable opportunities (>0.1%): {len(df[df['potential_profit_pct'] > 0.1])}")

    else:
        print("No data collected to plot.")

except Exception as e:
    print(f"An error occurred: {e}")