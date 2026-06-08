from datetime import datetime, timezone

import pytest

from portfolio_system.core.price_buffer import PriceBuffer


def test_add_and_retrieve_prices() -> None:
    buffer = PriceBuffer(max_history_length=3)

    timestamp = datetime.now(timezone.utc)

    buffer.add_price("AAPL", 100.0, timestamp)
    buffer.add_price("AAPL", 101.0, timestamp)

    assert buffer.get_prices("AAPL") == [100.0, 101.0]


def test_assets_have_separate_histories() -> None:
    buffer = PriceBuffer(max_history_length=3)

    timestamp = datetime.now(timezone.utc)

    buffer.add_price("AAPL", 100.0, timestamp)
    buffer.add_price("MSFT", 400.0, timestamp)

    assert buffer.get_prices("AAPL") == [100.0]
    assert buffer.get_prices("MSFT") == [400.0]


def test_oldest_price_is_removed_when_buffer_is_full() -> None:
    buffer = PriceBuffer(max_history_length=3)

    timestamp = datetime.now(timezone.utc)

    buffer.add_price("AAPL", 100.0, timestamp)
    buffer.add_price("AAPL", 101.0, timestamp)
    buffer.add_price("AAPL", 102.0, timestamp)
    buffer.add_price("AAPL", 103.0, timestamp)

    assert buffer.get_prices("AAPL") == [101.0, 102.0, 103.0]


def test_has_enough_history() -> None:
    buffer = PriceBuffer(max_history_length=20)

    timestamp = datetime.now(timezone.utc)

    buffer.add_price("AAPL", 100.0, timestamp)
    buffer.add_price("AAPL", 101.0, timestamp)

    assert buffer.has_enough_history("AAPL", required_length=2)
    assert not buffer.has_enough_history("AAPL", required_length=3)


def test_negative_price_is_rejected() -> None:
    buffer = PriceBuffer()

    timestamp = datetime.now(timezone.utc)

    with pytest.raises(ValueError):
        buffer.add_price("AAPL", -10.0, timestamp)