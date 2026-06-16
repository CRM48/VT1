from portfolio_system.domain.decisions import DecisionAction


DEFAULT_LABEL_THRESHOLD = 0.02


def calculate_future_return(
    current_price: float,
    future_price: float,
) -> float:
    if current_price <= 0:
        raise ValueError("current_price must be greater than zero.")

    if future_price <= 0:
        raise ValueError("future_price must be greater than zero.")

    return (future_price - current_price) / current_price


def calculate_label(
    current_price: float,
    future_price: float,
    threshold: float = DEFAULT_LABEL_THRESHOLD,
) -> str:
    if threshold < 0:
        raise ValueError("threshold must not be negative.")

    future_return = calculate_future_return(
        current_price=current_price,
        future_price=future_price,
    )

    if future_return > threshold:
        return DecisionAction.BUY.value

    if future_return < -threshold:
        return DecisionAction.SELL.value

    return DecisionAction.HOLD.value