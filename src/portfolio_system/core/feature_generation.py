from datetime import datetime
from statistics import mean, pstdev

from portfolio_system.domain.model_features import ModelFeatures


MINIMUM_HISTORY_LENGTH = 21


def calculate_percentage_change(
    old_price: float,
    new_price: float,
) -> float:
    if old_price <= 0:
        raise ValueError("old_price must be greater than zero.")

    return (new_price - old_price) / old_price


def calculate_returns(prices: list[float]) -> list[float]:
    if len(prices) < 2:
        return []

    return [
        calculate_percentage_change(
            old_price=prices[index - 1],
            new_price=prices[index],
        )
        for index in range(1, len(prices))
    ]


def calculate_price_position(
    prices: list[float],
) -> float:
    lowest_price = min(prices)
    highest_price = max(prices)
    current_price = prices[-1]

    if highest_price == lowest_price:
        return 0.5

    return (current_price - lowest_price) / (highest_price - lowest_price)


def safe_ratio(
    numerator: float,
    denominator: float,
) -> float:
    if denominator == 0:
        return 0.0

    return numerator / denominator


def generate_features(
    asset: str,
    timestamp: datetime,
    prices: list[float],
) -> ModelFeatures:
    if len(prices) < MINIMUM_HISTORY_LENGTH:
        raise ValueError(
            f"At least {MINIMUM_HISTORY_LENGTH} prices are required."
        )

    recent_prices = prices[-MINIMUM_HISTORY_LENGTH:]
    recent_returns = calculate_returns(recent_prices)

    return_1d = calculate_percentage_change(
        old_price=recent_prices[-2],
        new_price=recent_prices[-1],
    )

    return_5d = calculate_percentage_change(
        old_price=recent_prices[-6],
        new_price=recent_prices[-1],
    )

    return_10d = calculate_percentage_change(
        old_price=recent_prices[-11],
        new_price=recent_prices[-1],
    )

    return_20d = calculate_percentage_change(
        old_price=recent_prices[-21],
        new_price=recent_prices[-1],
    )

    moving_average_5d = mean(recent_prices[-5:])
    moving_average_10d = mean(recent_prices[-10:])
    moving_average_20d = mean(recent_prices[-20:])

    moving_average_ratio_5_20 = safe_ratio(
        moving_average_5d,
        moving_average_20d,
    )

    moving_average_ratio_10_20 = safe_ratio(
        moving_average_10d,
        moving_average_20d,
    )

    volatility_5d = pstdev(recent_returns[-5:])
    volatility_20d = pstdev(recent_returns[-20:])

    volatility_ratio_5_20 = safe_ratio(
        volatility_5d,
        volatility_20d,
    )

    price_position_20d = calculate_price_position(
        recent_prices[-20:]
    )

    return ModelFeatures(
        asset=asset,
        timestamp=timestamp,
        return_1d=return_1d,
        return_5d=return_5d,
        return_10d=return_10d,
        return_20d=return_20d,
        moving_average_ratio_5_20=moving_average_ratio_5_20,
        moving_average_ratio_10_20=moving_average_ratio_10_20,
        volatility_5d=volatility_5d,
        volatility_20d=volatility_20d,
        volatility_ratio_5_20=volatility_ratio_5_20,
        price_position_20d=price_position_20d,
    )