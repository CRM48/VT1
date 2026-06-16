from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIRECTORY = PROJECT_ROOT / "data" / "processed"

"""
Download historical prices for one asset and save them as a CSV file.

Define:
    - The asset (using its ticker symbol)
    - Start date
    - End date
    - Interval between records

Returns:
    The path of the saved CSV file.
"""


def download_prices(asset: str, start_date: str, end_date: str, interval: str = "1d") -> Path:
    

    print(f"Downloading {asset} prices...")

    data = yf.download(
        tickers=asset,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=False,
        progress=False,
        multi_level_index=False,
    )

    if data.empty:
        raise RuntimeError(f"No price data was returned for {asset}.")

    timestamp_column = "Datetime" if "Datetime" in data.index.names else "Date"

    data = data.reset_index()

    if timestamp_column not in data.columns:
        raise RuntimeError("Could not find a timestamp column in the downloaded data.")

    cleaned_data = data[[timestamp_column, "Close"]].copy()

    cleaned_data = cleaned_data.rename(
        columns={
            timestamp_column: "timestamp",
            "Close": "price",
        }
    )

    cleaned_data.insert(0, "asset", asset)
    cleaned_data = cleaned_data.dropna()

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIRECTORY / f"{asset}_{interval}_prices.csv"

    cleaned_data.to_csv(output_path, index=False)

    print(f"Saved {len(cleaned_data)} rows to:")
    print(output_path)

    return output_path


def main() -> None:
    download_prices(asset="AAPL", start_date="2023-01-01", end_date="2026-01-01", interval="1d")


if __name__ == "__main__":
    main()