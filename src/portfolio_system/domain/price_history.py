from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PricePoint:
    asset: str
    price: float
    timestamp: datetime