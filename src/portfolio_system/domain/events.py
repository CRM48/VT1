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