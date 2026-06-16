def calculate_label(current_price: float, next_price: float, threshold: float = 0.01) -> str:
    future_return = (next_price - current_price) / current_price

    if future_return > threshold:
        return "BUY"

    if future_return < -threshold:
        return "SELL"

    return "HOLD"