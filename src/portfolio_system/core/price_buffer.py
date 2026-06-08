from collections import deque
from datetime import datetime

from portfolio_system.domain.price_history import PricePoint


class PriceBuffer:
    def __init__(self, max_history_length: int = 20) -> None:
        if max_history_length <= 0:
            raise ValueError("max_history_length must be greater than zero.")

        self.max_history_length = max_history_length

        self._history: dict[str, deque[PricePoint]] = {}

    def add_price(self, asset: str, price: float, timestamp: datetime) -> None:
        if not asset.strip():
            raise ValueError("asset must not be empty.")

        if price <= 0:
            raise ValueError("price must be greater than zero.")

        if asset not in self._history:
            self._history[asset] = deque(
                maxlen=self.max_history_length
            )

        price_point = PricePoint(asset=asset, price=price, timestamp=timestamp)

        self._history[asset].append(price_point)

    def get_history(self, asset: str) -> list[PricePoint]:

        if asset not in self._history:
            return []

        return list(self._history[asset])

    def get_prices(self, asset: str) -> list[float]:

        return [
            price_point.price
            for price_point in self.get_history(asset)
        ]

    def has_enough_history(self, asset: str, required_length: int) -> bool:
        return len(self.get_history(asset)) >= required_length