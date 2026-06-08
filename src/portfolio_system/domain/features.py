from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ModelFeatures:
    asset: str
    timestamp: datetime
    return_1d: float
    return_5d: float
    moving_average_ratio_5_20: float
    volatility_5d: float
    volatility_20d: float

    def as_list(self) -> list[float]:
        return [
            self.return_1d,
            self.return_5d,
            self.moving_average_ratio_5_20,
            self.volatility_5d,
            self.volatility_20d,
        ]