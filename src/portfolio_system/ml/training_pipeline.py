from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv

from collections import Counter

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from portfolio_system.core.feature_generation import (
    MINIMUM_HISTORY_LENGTH,
    generate_features,
)
from portfolio_system.core.labels import calculate_label
from portfolio_system.ml.train_model import FEATURE_COLUMNS


@dataclass(frozen=True)
class TrainingSummary:
    model_name: str
    model_path: Path
    source_dataset_path: Path
    training_rows_path: Path
    injection_data_path: Path

    train_accuracy: float
    test_accuracy: float

    train_rows: int
    test_rows: int
    final_training_rows: int
    injection_rows: int

    label_horizon: int
    label_threshold: float

    train_start_timestamp: str
    train_end_timestamp: str
    injection_start_timestamp: str
    injection_end_timestamp: str


def load_price_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)

    required_columns = {"asset", "timestamp", "price"}
    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {missing_columns}")

    if data.empty:
        raise ValueError("Dataset is empty.")

    data = data.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data["price"] = data["price"].astype(float)

    data = data.sort_values("timestamp").reset_index(drop=True)

    return data


def split_price_data_for_training_and_injection(
    price_data: pd.DataFrame,
    development_ratio: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0 < development_ratio < 1:
        raise ValueError("development_ratio must be between 0 and 1.")

    split_index = int(len(price_data) * development_ratio)

    if split_index <= MINIMUM_HISTORY_LENGTH:
        raise ValueError(
            "Not enough rows in the model-development section."
        )

    development_data = price_data.iloc[:split_index].copy()
    injection_data = price_data.iloc[split_index:].copy()

    if injection_data.empty:
        raise ValueError("No injection rows were created.")

    return development_data, injection_data

def create_labelled_feature_rows(
    price_data: pd.DataFrame,
    label_horizon: int,
    label_threshold: float,
) -> pd.DataFrame:
    rows = []
    prices = []

    for index in range(len(price_data) - label_horizon):
        current_row = price_data.iloc[index]
        future_row = price_data.iloc[index + label_horizon]

        asset = str(current_row["asset"])
        timestamp = current_row["timestamp"]
        current_price = float(current_row["price"])
        future_price = float(future_row["price"])

        prices.append(current_price)

        if len(prices) < MINIMUM_HISTORY_LENGTH:
            continue

        features = generate_features(
            asset=asset,
            timestamp=timestamp.to_pydatetime(),
            prices=prices,
        )

        label = calculate_label(
            current_price=current_price,
            future_price=future_price,
            threshold=label_threshold,
        )

        rows.append(
            {
                "asset": asset,
                "timestamp": timestamp.isoformat(),
                "return_1d": features.return_1d,
                "return_5d": features.return_5d,
                "return_10d": features.return_10d,
                "return_20d": features.return_20d,
                "moving_average_ratio_5_20": features.moving_average_ratio_5_20,
                "moving_average_ratio_10_20": features.moving_average_ratio_10_20,
                "volatility_5d": features.volatility_5d,
                "volatility_20d": features.volatility_20d,
                "volatility_ratio_5_20": features.volatility_ratio_5_20,
                "price_position_20d": features.price_position_20d,
                "label": label,
            }
        )

    if not rows:
        raise ValueError("No labelled feature rows were created.")

    return pd.DataFrame(rows)

def split_train_test(
    labelled_rows: pd.DataFrame,
    train_ratio: float = 0.8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")

    split_index = int(len(labelled_rows) * train_ratio)

    train_rows = labelled_rows.iloc[:split_index].copy()
    test_rows = labelled_rows.iloc[split_index:].copy()

    if train_rows.empty or test_rows.empty:
        raise ValueError("Train and test splits must not be empty.")

    return train_rows, test_rows


def train_random_forest(
    rows: pd.DataFrame,
) -> RandomForestClassifier:
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(
        rows[FEATURE_COLUMNS],
        rows["label"],
    )

    return model


def evaluate_model(
    model,
    rows: pd.DataFrame,
) -> dict:
    predictions = model.predict(rows[FEATURE_COLUMNS])

    accuracy = accuracy_score(
        y_true=rows["label"],
        y_pred=predictions,
    )

    report = classification_report(
        rows["label"],
        predictions,
        zero_division=0,
    )

    return {
        "accuracy": accuracy,
        "actual_distribution": dict(Counter(rows["label"])),
        "prediction_distribution": dict(Counter(predictions)),
        "classification_report": report,
    }


def create_injection_data_with_warmup(
    development_data: pd.DataFrame,
    injection_data: pd.DataFrame,
) -> pd.DataFrame:
    warmup_rows = development_data.tail(MINIMUM_HISTORY_LENGTH).copy()
    warmup_rows["is_warmup"] = True

    real_injection_rows = injection_data.copy()
    real_injection_rows["is_warmup"] = False

    output = pd.concat(
        [warmup_rows, real_injection_rows],
        ignore_index=True,
    )

    return output


def append_model_registry(
    registry_path: Path,
    summary: TrainingSummary,
) -> None:
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "model_name": summary.model_name,
        "model_type": "Random Forest",
        "model_path": str(summary.model_path),
        "source_dataset_path": str(summary.source_dataset_path),
        "training_rows_path": str(summary.training_rows_path),
        "injection_data_path": str(summary.injection_data_path),
        "train_accuracy": summary.train_accuracy,
        "test_accuracy": summary.test_accuracy,
        "train_rows": summary.train_rows,
        "test_rows": summary.test_rows,
        "final_training_rows": summary.final_training_rows,
        "injection_rows": summary.injection_rows,
        "label_horizon": summary.label_horizon,
        "label_threshold": summary.label_threshold,
        "train_start_timestamp": summary.train_start_timestamp,
        "train_end_timestamp": summary.train_end_timestamp,
        "injection_start_timestamp": summary.injection_start_timestamp,
        "injection_end_timestamp": summary.injection_end_timestamp,
    }

    file_exists = registry_path.exists()
    file_is_empty = file_exists and registry_path.stat().st_size == 0

    with registry_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(row.keys()),
        )

        if not file_exists or file_is_empty:
            writer.writeheader()

        writer.writerow(row)

    file_exists = registry_path.exists()

    with registry_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(row.keys()),
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def run_training_pipeline(
    source_dataset_path: Path,
    model_name: str,
    model_output_dir: Path,
    training_rows_output_dir: Path,
    injection_output_dir: Path,
    registry_path: Path,
    development_ratio: float = 0.5,
    train_ratio: float = 0.8,
    label_horizon: int = 5,
    label_threshold: float = 0.02,
) -> TrainingSummary:
    price_data = load_price_data(source_dataset_path)

    development_data, injection_data = split_price_data_for_training_and_injection(
        price_data=price_data,
        development_ratio=development_ratio,
    )

    labelled_rows = create_labelled_feature_rows(
        price_data=development_data,
        label_horizon=label_horizon,
        label_threshold=label_threshold,
    )

    train_rows, test_rows = split_train_test(
        labelled_rows=labelled_rows,
        train_ratio=train_ratio,
    )

    evaluation_model = train_random_forest(train_rows)

    train_metrics = evaluate_model(
        model=evaluation_model,
        rows=train_rows,
    )

    test_metrics = evaluate_model(
        model=evaluation_model,
        rows=test_rows,
    )

    train_accuracy = train_metrics["accuracy"]
    test_accuracy = test_metrics["accuracy"]

    # Final model is trained on all model-development rows after
    # test accuracy has already been measured.
    final_model = train_random_forest(labelled_rows)

    model_output_dir.mkdir(parents=True, exist_ok=True)
    training_rows_output_dir.mkdir(parents=True, exist_ok=True)
    injection_output_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_output_dir / f"{model_name}.joblib"
    training_rows_path = training_rows_output_dir / f"{model_name}_training_rows.csv"
    injection_data_path = injection_output_dir / f"{model_name}_injection_prices.csv"

    if model_path.exists():
        raise ValueError(f"Model already exists: {model_path}")

    if training_rows_path.exists():
        raise ValueError(f"Training rows already exist: {training_rows_path}")

    if injection_data_path.exists():
        raise ValueError(f"Injection data already exists: {injection_data_path}")

    labelled_rows.to_csv(
        training_rows_path,
        index=False,
    )

    injection_with_warmup = create_injection_data_with_warmup(
        development_data=development_data,
        injection_data=injection_data,
    )

    injection_with_warmup.to_csv(
        injection_data_path,
        index=False,
    )

    model_package = {
        "model": final_model,
        "metadata": {
            "model_name": model_name,
            "source_dataset_path": str(source_dataset_path),
            "training_rows_path": str(training_rows_path),
            "injection_data_path": str(injection_data_path),
            "feature_columns": FEATURE_COLUMNS,
            "development_ratio": development_ratio,
            "train_ratio": train_ratio,
            "test_ratio": 1 - train_ratio,
            "label_horizon": label_horizon,
            "label_threshold": label_threshold,
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "train_actual_distribution": train_metrics["actual_distribution"],
            "train_prediction_distribution": train_metrics["prediction_distribution"],
            "test_actual_distribution": test_metrics["actual_distribution"],
            "test_prediction_distribution": test_metrics["prediction_distribution"],
            "test_classification_report": test_metrics["classification_report"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "final_model_training_policy": (
                "Test accuracy was measured using a model trained only on the "
                "training split. After accuracy was recorded, the final saved "
                "model was trained on all labelled rows from the model-development "
                "section before being used with injection data."
            ),
        },
    }

    joblib.dump(
        model_package,
        model_path,
    )

    summary = TrainingSummary(
        model_name=model_name,
        model_path=model_path,
        source_dataset_path=source_dataset_path,
        training_rows_path=training_rows_path,
        injection_data_path=injection_data_path,
        train_accuracy=train_accuracy,
        test_accuracy=test_accuracy,
        train_rows=len(train_rows),
        test_rows=len(test_rows),
        final_training_rows=len(labelled_rows),
        injection_rows=len(injection_data),
        label_horizon=label_horizon,
        label_threshold=label_threshold,
        train_start_timestamp=str(development_data["timestamp"].iloc[0]),
        train_end_timestamp=str(development_data["timestamp"].iloc[-1]),
        injection_start_timestamp=str(injection_data["timestamp"].iloc[0]),
        injection_end_timestamp=str(injection_data["timestamp"].iloc[-1]),
    )

    append_model_registry(
        registry_path=registry_path,
        summary=summary,
    )

    return summary