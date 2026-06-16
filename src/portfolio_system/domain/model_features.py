from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ModelFeatures:
    asset: str
    timestamp: datetime
    return_1d: float
    return_5d: float
    return_10d: float
    return_20d: float
    moving_average_ratio_5_20: float
    moving_average_ratio_10_20: float
    volatility_5d: float
    volatility_20d: float
    volatility_ratio_5_20: float
    price_position_20d: float

    def as_list(self) -> list[float]:
        return [
            self.return_1d,
            self.return_5d,
            self.return_10d,
            self.return_20d,
            self.moving_average_ratio_5_20,
            self.moving_average_ratio_10_20,
            self.volatility_5d,
            self.volatility_20d,
            self.volatility_ratio_5_20,
            self.price_position_20d,
        ]