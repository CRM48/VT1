from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


PROJECT_ROOT = Path(__file__).resolve().parents[3]
TRAINING_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_training_data.csv"
MODEL_OUTPUT_PATH = PROJECT_ROOT / "models" / "random_forest_v1.joblib"

FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "return_10d",
    "return_20d",
    "moving_average_ratio_5_20",
    "moving_average_ratio_10_20",
    "volatility_5d",
    "volatility_20d",
    "volatility_ratio_5_20",
    "price_position_20d",
]

LABEL_COLUMN = "label"

TRAINING_SPLIT_RATIO = 0.8


def load_training_data(path: Path) -> pd.DataFrame:

    data = pd.read_csv(path)

    required_columns = FEATURE_COLUMNS + [LABEL_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Training dataset is missing columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError("Training dataset is empty.")

    return data


def split_data_chronologically(data: pd.DataFrame, training_ratio: float = TRAINING_SPLIT_RATIO) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset without shuffling.

    Older rows are used for training.
    Newer rows are used for testing.
    """

    if not 0 < training_ratio < 1:
        raise ValueError("training_ratio must be between 0 and 1.")

    split_index = int(len(data) * training_ratio)

    if split_index == 0 or split_index == len(data):
        raise ValueError("Dataset is too small to split.")

    training_data = data.iloc[:split_index]
    testing_data = data.iloc[split_index:]

    x_train = training_data[FEATURE_COLUMNS]
    y_train = training_data[LABEL_COLUMN]

    x_test = testing_data[FEATURE_COLUMNS]
    y_test = testing_data[LABEL_COLUMN]

    return x_train, x_test, y_train, y_test


def train_model(x_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """
    Train the first classification model.
    """

    model = RandomForestClassifier(n_estimators=100, random_state=42,)

    model.fit(x_train, y_train)

    return model


def evaluate_model(model: RandomForestClassifier,x_test: pd.DataFrame,y_test: pd.Series,) -> None:
    """
    Print a simple performance summary.
    """

    predictions = model.predict(x_test)

    accuracy = accuracy_score(y_true=y_test,y_pred=predictions,)

    print("Model evaluation:")
    print(f"  Accuracy = {accuracy:.3f}")
    print()
    print(classification_report(y_test, predictions))


def save_model(model: RandomForestClassifier, output_path: Path) -> None:
    """
    Save the trained model so it can be loaded during prediction.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(value=model, filename=output_path,)


def main() -> None:
    data = load_training_data(TRAINING_DATA_PATH)

    x_train, x_test, y_train, y_test = (split_data_chronologically(data))

    print("Training dataset:")
    print(f"  Total rows = {len(data)}")
    print(f"  Training rows = {len(x_train)}")
    print(f"  Testing rows = {len(x_test)}")
    print()

    model = train_model(x_train=x_train, y_train=y_train,)
    evaluate_model(model=model, x_test=x_test,y_test=y_test)
    save_model(model=model, output_path=MODEL_OUTPUT_PATH)

    print()
    print(f"Saved model to: {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()