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
    processing_duration_ms: float
    experiment_id: str
    architecture_id: str

    def __str__(self) -> str:
        return (
            "Portfolio Decision:\n"
            f"    Event ID = {self.event_id}\n"
            f"    Asset = {self.asset}\n"
            f"    Decision = {self.action.value}\n"
            f"    Reason = {self.reason}\n"
            f"    Time of Decision = {self.processed_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"    Time to make Decision = {self.processing_duration_ms}ms"
            f"    Experiment ID = {self.experiment_id}\n"
            f"    Architecture ID = {self.architecture_id}"
        )