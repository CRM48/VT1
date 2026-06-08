from datetime import datetime, timezone

import pytest

from portfolio_system.core.feature_generation import (
    calculate_percentage_change,
    calculate_returns,
    generate_features,
)


def test_calculate_percentage_change() -> None:
    result = calculate_percentage_change(
        old_price=100.0,
        new_price=105.0,
    )

    assert result == pytest.approx(0.05)


def test_calculate_returns() -> None:
    result = calculate_returns(
        prices=[100.0, 102.0, 101.0]
    )

    assert result[0] == pytest.approx(0.02)
    assert result[1] == pytest.approx(-0.00980392)


def test_generate_features_requires_enough_prices() -> None:
    with pytest.raises(ValueError):
        generate_features(
            asset="AAPL",
            timestamp=datetime.now(timezone.utc),
            prices=[100.0, 101.0],
        )


def test_generate_features_returns_expected_values() -> None:
    prices = [
        100.0,
        101.0,
        102.0,
        103.0,
        104.0,
        105.0,
        106.0,
        107.0,
        108.0,
        109.0,
        110.0,
        111.0,
        112.0,
        113.0,
        114.0,
        115.0,
        116.0,
        117.0,
        118.0,
        119.0,
        120.0,
    ]

    features = generate_features(
        asset="AAPL",
        timestamp=datetime.now(timezone.utc),
        prices=prices,
    )

    assert features.asset == "AAPL"

    assert features.return_1d == pytest.approx(
        (120.0 - 119.0) / 119.0
    )

    assert features.return_5d == pytest.approx(
        (120.0 - 115.0) / 115.0
    )

    assert features.moving_average_ratio_5_20 > 1.0

    assert len(features.as_list()) == 5