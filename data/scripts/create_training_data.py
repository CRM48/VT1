import csv
from pathlib import Path

from datetime import datetime

from portfolio_system.core.feature_generation import generate_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_1d_prices.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_training_data.csv"


MINIMUM_HISTORY_LENGTH = 21
LABEL_THRESHOLD = 0.01


def calculate_label(current_price: float, next_price: float, threshold: float = LABEL_THRESHOLD) -> str:
    future_return = (next_price - current_price) / current_price

    if future_return > threshold:
        return "BUY"

    if future_return < -threshold:
        return "SELL"

    return "HOLD"


def load_price_rows(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def create_training_rows(price_rows: list[dict[str, str]],) -> list[dict[str, str | float]]:
    training_rows: list[dict[str, str | float]] = []

    prices: list[float] = []

    for index, row in enumerate(price_rows):
        current_price = float(row["price"])
        prices.append(current_price)

        if len(prices) < MINIMUM_HISTORY_LENGTH:
            continue

        if index + 1 >= len(price_rows):
            continue

        features = generate_features(asset=row["asset"], timestamp=datetime.fromisoformat(row["timestamp"]), prices=prices)

        next_price = float(price_rows[index + 1]["price"])

        label = calculate_label(
            current_price=current_price,
            next_price=next_price,
        )

        training_rows.append(
            {
                "asset": features.asset,
                "timestamp": features.timestamp,
                "return_1d": features.return_1d,
                "return_5d": features.return_5d,
                "moving_average_ratio_5_20": (
                    features.moving_average_ratio_5_20
                ),
                "volatility_5d": features.volatility_5d,
                "volatility_20d": features.volatility_20d,
                "label": label,
            }
        )

    return training_rows


def save_training_rows(training_rows: list[dict[str, str | float]],output_path: Path) -> None:
    if not training_rows:
        raise RuntimeError("No training rows were created.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "asset",
        "timestamp",
        "return_1d",
        "return_5d",
        "moving_average_ratio_5_20",
        "volatility_5d",
        "volatility_20d",
        "label",
    ]

    with output_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(training_rows)


def main() -> None:
    price_rows = load_price_rows(INPUT_PATH)

    training_rows = create_training_rows(price_rows)

    save_training_rows(training_rows=training_rows, output_path=OUTPUT_PATH)

    print("Training dataset created:")
    print(f"  Input rows = {len(price_rows)}")
    print(f"  Training rows = {len(training_rows)}")
    print(f"  Saved to = {OUTPUT_PATH}")


if __name__ == "__main__":
    main()