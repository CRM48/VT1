from dataclasses import dataclass
from datetime import datetime

"""
Define the structure of a market event
A market event is the input into the system (such as an updated price)

Event ID: Unique ID for each market event
Asset: The stock code, e.g., AAPL
Price: Current market price
Timestamp: when the event occured
Experiment ID: Which test run produced the event (architecture / type of test)
Architecture ID: Which architecture is being tested (four architectures)

Frozen ensures events can not be changed after they're created
"""

@dataclass(frozen=True)
class MarketEvent:
    event_id: str
    asset: str
    price: float
    market_timestamp: datetime
    experiment_id: str
    architecture_id: str

    def __str__(self) -> str:
        return (
            "Market Event:\n"
            f"    Event ID = {self.event_id}\n"
            f"    Asset = {self.asset}\n"
            f"    Price = {self.price}\n"
            f"    Time of Event = {self.market_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"    Experiment ID = {self.experiment_id}\n"
            f"    Architecture ID = {self.architecture_id}"
        )