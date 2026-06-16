from data.scripts.create_training_data import calculate_label


def test_buy_label() -> None:
    assert calculate_label(
        current_price=100.0,
        next_price=102.0,
    ) == "BUY"


def test_sell_label() -> None:
    assert calculate_label(
        current_price=100.0,
        next_price=98.0,
    ) == "SELL"


def test_hold_label() -> None:
    assert calculate_label(
        current_price=100.0,
        next_price=100.5,
    ) == "HOLD"