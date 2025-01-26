class MultiExchangeDataFeed:
    def __init__(self, exchanges: Dict[str, Dict[str, str]]):
        """
        :param exchanges: A dictionary containing exchange-specific APIs and credentials.
        Example:
        {
            "binance": {"api_url": "https://api.binance.com", "api_key": "your_key"},
            "kraken": {"api_url": "https://api.kraken.com", "api_key": "your_key"}
        }
        """
        self.exchanges = exchanges
        self.prices = {}  # Store current prices by exchange and symbol

    async def fetch_prices(self, symbol: str):
        """
        Fetch the latest prices for a given symbol from all exchanges.
        :param symbol: Trading pair symbol (e.g., "BTC/USD").
        """
        for exchange_name, config in self.exchanges.items():
            try:
                # Simulate API fetch (replace with actual API calls)
                price = await self.simulate_price_fetch(exchange_name, symbol)
                self.prices[exchange_name] = price
                print(f"{exchange_name}: {symbol} price is {price}")
            except Exception as e:
                print(f"Error fetching price from {exchange_name}: {e}")

    async def simulate_price_fetch(self, exchange_name: str, symbol: str) -> float:
        """Simulate price fetching (replace with actual API call logic)."""
        await asyncio.sleep(0.1)
        return 100 + hash(exchange_name + symbol) % 50  # Randomized mock price
