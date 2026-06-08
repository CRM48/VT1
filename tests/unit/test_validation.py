from datetime import datetime, timezone

import pytest

from portfolio_system.core.validation import (
    InvalidMarketEventError,
    validate_market_event,
)
from portfolio_system.domain.events import MarketEvent


def test_valid_event_passes_validation() -> None:
    event = MarketEvent(
        event_id="evt-001",
        instrument="AAPL",
        price=192.50,
        market_timestamp=datetime.now(timezone.utc),
    )

    validate_market_event(event)


def test_negative_price_is_rejected() -> None:
    event = MarketEvent(
        event_id="evt-002",
        instrument="AAPL",
        price=-10.0,
        market_timestamp=datetime.now(timezone.utc),
    )

    with pytest.raises(InvalidMarketEventError):
        validate_market_event(event)


def test_empty_instrument_is_rejected() -> None:
    event = MarketEvent(
        event_id="evt-003",
        instrument="",
        price=192.50,
        market_timestamp=datetime.now(timezone.utc),
    )

    with pytest.raises(InvalidMarketEventError):
        validate_market_event(event)