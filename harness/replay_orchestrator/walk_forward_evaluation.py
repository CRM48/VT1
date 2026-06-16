import csv
import json
from pathlib import Path
from datetime import datetime

from portfolio_system.core.feature_generation import (
    MINIMUM_HISTORY_LENGTH,
    generate_features,
)
from portfolio_system.core.price_buffer import PriceBuffer
from portfolio_system.ml.labels import calculate_label
from portfolio_system.ml.predict import load_model, predict_action


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_1d_prices.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_v1.joblib"
OUTPUT_PATH = PROJECT_ROOT / "experiments" / "raw" / "EXP-WALK-FORWARD-001-predictions.jsonl"



def load_price_rows(path: Path) -> list[dict[str, str]]:
    with path.open(mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main() -> None:
    model = load_model(MODEL_PATH)

    price_rows = load_price_rows(PRICE_DATA_PATH)

    buffer = PriceBuffer(max_history_length=MINIMUM_HISTORY_LENGTH)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()

    prediction_count = 0
    correct_count = 0
    skipped_count = 0

    with OUTPUT_PATH.open(mode="a", encoding="utf-8") as output_file:
        for index in range(len(price_rows) - 1):
            current_row = price_rows[index]
            next_row = price_rows[index + 1]

            asset = current_row["asset"]
            current_price = float(current_row["price"])
            next_price = float(next_row["price"])
            timestamp = datetime.fromisoformat(current_row["timestamp"])

            # The current price becomes available to the system.
            buffer.add_price(asset=asset, price=current_price, timestamp=timestamp)

            # Not enough history exists yet.
            if not buffer.has_enough_history(asset=asset, required_length=MINIMUM_HISTORY_LENGTH):
                skipped_count += 1
                continue

            prices = buffer.get_prices(asset)

            features = generate_features(asset=asset, timestamp=timestamp, prices=prices)

            predicted_label = predict_action(model=model, features=features)

            actual_label = calculate_label(current_price=current_price, next_price=next_price)

            is_correct = predicted_label == actual_label

            result = {
                "timestamp": current_row["timestamp"],
                "asset": asset,
                "current_price": current_price,
                "next_price": next_price,
                "predicted_label": predicted_label,
                "actual_label": actual_label,
                "correct": is_correct,
            }

            output_file.write(json.dumps(result) + "\n")

            prediction_count += 1

            if is_correct:
                correct_count += 1

    accuracy = (
        correct_count / prediction_count
        if prediction_count > 0
        else 0
    )

    print("Walk-forward evaluation complete:")
    print(f"  Predictions = {prediction_count}")
    print(f"  Correct = {correct_count}")
    print(f"  Skipped = {skipped_count}")
    print(f"  Accuracy = {accuracy:.3f}")
    print(f"  Results saved to = {OUTPUT_PATH}")


if __name__ == "__main__":
    main()