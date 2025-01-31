# src/main.py

import argparse
from src.modules.datafeed.data_feed import DataFeed


def fetch_rest_data(data_feed):
    """Fetch market data via REST API."""
    # Fetch real-time market data
    market_data = data_feed.fetch_market_data(exchange_name="binance", symbol="BTC/USDT")
    print("Market Data:", market_data)

    # Fetch historical market data
    historical_data = data_feed.fetch_historical_data(
        exchange_name="binance", symbol="BTC/USDT", timeframe="1h", limit=100
    )
    print("Historical Data (First 5 Candlesticks):", historical_data[:5])


def stream_websocket_data(data_feed):
    """Stream market data via WebSocket."""
    # Start WebSocket for real-time data streaming on Binance
    data_feed.start_websocket(exchange_name="binance", symbol="BTCUSDT")

    # Start WebSocket for Coinbase
    data_feed.start_websocket(exchange_name="coinbase", symbol="BTC-USD")

    # Start WebSocket for Kraken
    data_feed.start_websocket(exchange_name="kraken", symbol="BTC/USD")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Market Data Fetcher")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["rest", "websocket"],
        required=True,
        help="Mode to run the data feed: 'rest' for REST API or 'websocket' for WebSocket streaming",
    )
    args = parser.parse_args()

    # Initialize the DataFeed module
    data_feed = DataFeed(config_path="src/config/config.yaml", secrets_path="src/config/secrets.yaml")

    # Run the appropriate workflow based on the mode
    if args.mode == "rest":
        fetch_rest_data(data_feed)
    elif args.mode == "websocket":
        stream_websocket_data(data_feed)


if __name__ == "__main__":
    main()