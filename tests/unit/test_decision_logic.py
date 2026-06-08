from datetime import datetime, timezone

import pytest

from portfolio_system.core.decision_logic import generate_decision
from portfolio_system.domain.decisions import DecisionAction
from portfolio_system.domain.events import MarketEvent


def make_event(price: float) -> MarketEvent:
    return MarketEvent(
        event_id="evt-001",
        instrument="AAPL",
        price=price,
        market_timestamp=datetime.now(timezone.utc),
    )


def test_buy_when_price_increases_above_threshold() -> None:
    event = make_event(price=103.0)

    decision = generate_decision(event, previous_price=100.0)

    assert decision.action == DecisionAction.BUY


def test_sell_when_price_decreases_below_threshold() -> None:
    event = make_event(price=97.0)

    decision = generate_decision(event, previous_price=100.0)

    assert decision.action == DecisionAction.SELL


def test_hold_when_price_change_is_within_threshold() -> None:
    event = make_event(price=100.5)

    decision = generate_decision(event, previous_price=100.0)

    assert decision.action == DecisionAction.HOLD


def test_invalid_previous_price_is_rejected() -> None:
    event = make_event(price=100.0)

    with pytest.raises(ValueError):
        generate_decision(event, previous_price=0.0)