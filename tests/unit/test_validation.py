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
        asset="AAPL",
        price=192.50,
        market_timestamp=datetime.now(timezone.utc),
        experiment_id="A0-test-001",
        architecture_id="A0"
    )

    validate_market_event(event)


def test_negative_price_is_rejected() -> None:
    event = MarketEvent(
        event_id="evt-002",
        asset="AAPL",
        price=-10.0,
        market_timestamp=datetime.now(timezone.utc),
        experiment_id="A0-test-002",
        architecture_id="A0"
    )

    with pytest.raises(InvalidMarketEventError):
        validate_market_event(event)


def test_empty_asset_is_rejected() -> None:
    event = MarketEvent(
        event_id="evt-003",
        asset="",
        price=192.50,
        market_timestamp=datetime.now(timezone.utc),
        experiment_id="A0-test-003",
        architecture_id="A0"
    )

    with pytest.raises(InvalidMarketEventError):
        validate_market_event(event)