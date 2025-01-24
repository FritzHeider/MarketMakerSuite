# path: trading_bot/system_architecture.py
from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Tuple, Optional


# Abstract Interfaces
class DataFeedInterface(ABC):
    """Abstract base class for data feed modules."""

    @abstractmethod
    async def connect(self) -> None:
        """Connect to the data source."""
        pass

    @abstractmethod
    async def update_price(self) -> None:
        """Fetch and update the latest market price."""
        pass

    @abstractmethod
    def get_current_price(self) -> float:
        """Get the current market price."""
        pass


class OrderManagementInterface(ABC):
    """Abstract base class for order management modules."""

    @abstractmethod
    async def place_order(self, price: float, quantity: float, order_type: str) -> str:
        """Place an order."""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> Dict:
        """Get the status of an order."""
        pass


# Concrete Implementation of DataFeedModule
class DataFeedModule(DataFeedInterface):
    def __init__(self, api_url: str, api_key: str, logger=None):
        self.api_url = api_url
        self.api_key = api_key
        self.current_price: Optional[float] = None
        self.logger = logger or self._default_logger()

    async def connect(self) -> None:
        try:
            await asyncio.sleep(1)  # Simulate connection
            self.logger.info("Connected to the Market Data API.")
        except Exception as e:
            self.logger.error(f"Error connecting to API: {e}")

    async def update_price(self) -> None:
        try:
            await asyncio.sleep(1)  # Simulate data fetch
            self.current_price = 100.0  # Replace with real API data
            self.logger.info(f"Market price updated: {self.current_price}")
        except Exception as e:
            self.logger.error(f"Error updating market price: {e}")

    def get_current_price(self) -> float:
        if self.current_price is None:
            raise ValueError("Market price not available yet.")
        return self.current_price

    @staticmethod
    def _default_logger():
        import logging
        logger = logging.getLogger("DataFeedModule")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        return logger


# Concrete Implementation of OrderManagementModule
class OrderManagementModule(OrderManagementInterface):
    def __init__(self, logger=None):
        self.orders: Dict[str, Dict] = {}
        self.logger = logger or self._default_logger()

    async def place_order(self, price: float, quantity: float, order_type: str) -> str:
        try:
            order_id = f"order_{len(self.orders) + 1}"
            self.orders[order_id] = {
                "price": price,
                "quantity": quantity,
                "type": order_type,
                "status": "placed"
            }
            await asyncio.sleep(0.5)  # Simulate order placement
            self.logger.info(f"Order placed: {order_id}")
            return order_id
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            raise

    async def cancel_order(self, order_id: str) -> bool:
        try:
            if order_id in self.orders:
                self.orders[order_id]["status"] = "cancelled"
                await asyncio.sleep(0.5)  # Simulate API call
                self.logger.info(f"Order cancelled: {order_id}")
                return True
            else:
                self.logger.warning(f"Order ID {order_id} not found.")
                return False
        except Exception as e:
            self.logger.error(f"Error cancelling order: {e}")
            raise

    def get_order_status(self, order_id: str) -> Dict:
        return self.orders.get(order_id, {"status": "not found"})

    @staticmethod
    def _default_logger():
        import logging
        logger = logging.getLogger("OrderManagementModule")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        return logger
