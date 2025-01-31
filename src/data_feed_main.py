# src/modules/datafeed/data_feed.py

import ccxt
import yaml
from src.utils.logger import get_logger
from src.modules.datafeed.websocket_client import WebSocketClient
from tenacity import retry, stop_after_attempt, wait_fixed
import asyncio


class DataFeed:
    def __init__(self, config_path: str, secrets_path: str):
        """
        Initialize the DataFeed module with exchange APIs and WebSocket support.

        :param config_path: Path to the config.yaml file.
        :param secrets_path: Path to the secrets.yaml file.
        """
        self.logger = get_logger("DataFeed")
        self.config = self._load_yaml(config_path)
        self.secrets = self._load_yaml(secrets_path)
        self.exchanges = self._initialize_exchanges()
        self.websocket_client = None  # WebSocket client instance

    def _load_yaml(self, path: str):
        """Load a YAML file."""
        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Failed to load YAML file at {path}: {e}")
            return {}

    def _initialize_exchanges(self):
        """Initialize exchange clients using CCXT."""
        exchanges = {}
        for exchange_name, credentials in self.secrets.get("exchanges", {}).items():
            try:
                exchange_class = getattr(ccxt, exchange_name)
                exchanges[exchange_name] = exchange_class({
                    "apiKey": credentials["api_key"],
                    "secret": credentials["api_secret"]
                })
                self.logger.info(f"Initialized exchange: {exchange_name}")
            except Exception as e:
                self.logger.error(f"Failed to initialize {exchange_name}: {e}")
        return exchanges

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_market_data(self, exchange_name: str, symbol: str):
        """Fetch real-time ticker data via REST."""
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            self.logger.error(f"Exchange {exchange_name} not initialized.")
            return None

        try:
            ticker = exchange.fetch_ticker(symbol)
            self.logger.info(f"Fetched market data for {symbol} on {exchange_name}")
            return ticker
        except Exception as e:
            self.logger.warning(f"Error fetching market data: {e}")
            raise

    def start_websocket(self, exchange_name: str, symbol: str):
        """Start a WebSocket client for real-time data streaming."""
        ws_urls = {
            "binance": "wss://stream.binance.com:9443/ws",
            "coinbase": "wss://ws-feed.pro.coinbase.com",
            "kraken": "wss://ws.kraken.com"
        }

        if exchange_name not in ws_urls:
            self.logger.error(f"WebSocket not supported for {exchange_name}")
            return

        ws_url = ws_urls[exchange_name]
        self.websocket_client = WebSocketClient(
            exchange_name=exchange_name, ws_url=ws_url, symbol=symbol
        )
        asyncio.run(self.websocket_client.run())