from dataclasses import dataclass
from datetime import datetime
from enum import Enum

"""
Define the structure of a decision output
Process an event and make a decision

Event ID: the event the decision relates to
Asset: the stock number
Action: buy/sell/hold
Reason: why decision was made
Processed: when the decision was made
Experiment ID: the experiment the decision relates to
Architecture ID: the architecture being tested
"""


class DecisionAction(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


@dataclass(frozen=True)
class PortfolioDecision:
    event_id: str
    asset: str
    action: DecisionAction
    reason: str
    processed_at: datetime
    experiment_id: str
    architecture_id: str