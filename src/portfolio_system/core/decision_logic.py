from datetime import datetime, timezone

from portfolio_system.core.validation import validate_market_event
from portfolio_system.domain.decisions import DecisionAction, PortfolioDecision
from portfolio_system.domain.events import MarketEvent
import time

"""
Generate a decision from a market event
Base decision: If price increases by 1% BUY, or decreases by 1% SELL, otherwise HOLD

How it works:
- Calculate percentage change
- Determine if percentage change was above +- threshold
- Make decision
- Generate decision output
    - Create DecisionAction based on calculation
    - Create basic reasoning
    - Use time=now for timestamp
    - Use event data for all other variables
"""


def generate_decision(event: MarketEvent, previous_price: float, threshold_percentage: float = 0.01,) -> PortfolioDecision:

    validate_market_event(event)

    if previous_price <= 0:
        raise ValueError("previous_price must be greater than zero.")

    if threshold_percentage < 0:
        raise ValueError("threshold_percentage must not be negative.")

    percentage_change = (event.price - previous_price) / previous_price

    if percentage_change > threshold_percentage:
        action = DecisionAction.BUY
        reason = f"Price increased by {percentage_change:.2%}."

    elif percentage_change < -threshold_percentage:
        action = DecisionAction.SELL
        reason = f"Price decreased by {abs(percentage_change):.2%}."

    else:
        action = DecisionAction.HOLD
        reason = f"Price changed by {percentage_change:.2%}, within the threshold."

    #time.sleep(5)

    return PortfolioDecision(
        event_id=event.event_id,
        asset=event.asset,
        action=action,
        reason=reason,
        processed_at=datetime.now(timezone.utc),
        experiment_id=event.experiment_id,
        architecture_id=event.architecture_id,
    )