from datetime import date, datetime
from pathlib import Path
import re

import pandas as pd
import streamlit as st
import yfinance as yf

from common import DATA_DIR, initialise_session_state, show_sidebar
from constants import COMMON_STOCKS, StockOption


initialise_session_state()
show_sidebar()

st.title("1. Create Dataset")

st.write(
    "Download historical stock-price data from yfinance and save it as a "
    "fixed dataset for model training, evaluation, and experiments."
)


INTERVAL_OPTIONS = {
    "Daily": "1d",
    "Weekly": "1wk",
    "Monthly": "1mo",
    "3 Monthly": "3mo",
}


def format_stock_option(stock: StockOption) -> str:
    return f"{stock.ticker} — {stock.name}"


def normalise_dataset_name(
    ticker: str,
    user_input: str,
) -> str:
    ticker = ticker.upper().strip()

    cleaned = user_input.strip()

    cleaned = cleaned.replace(" ", "-")

    cleaned = re.sub(
        pattern=r"[^A-Za-z0-9_-]",
        repl="",
        string=cleaned,
    )

    if cleaned.upper().startswith(f"{ticker}-"):
        dataset_name = cleaned
    else:
        dataset_name = f"{ticker}-{cleaned}"

    return dataset_name


def validate_dataset_name(
    ticker: str,
    dataset_name: str,
    output_path: Path,
) -> list[str]:
    errors = []

    if not dataset_name.startswith(f"{ticker}-"):
        errors.append(f"Dataset name must start with `{ticker}-`.")

    suffix = dataset_name.removeprefix(f"{ticker}-")

    if not suffix:
        errors.append("Dataset name must include a name after the ticker.")

    if output_path.exists():
        errors.append("A dataset with this name already exists.")

    return errors


def download_dataset(
    ticker: str,
    start_date: date,
    end_date: date,
    interval: str,
    output_path: Path,
) -> pd.DataFrame:
    data = yf.download(
        tickers=ticker,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        interval=interval,
        auto_adjust=False,
        progress=False,
        multi_level_index=False,
    )

    if data.empty:
        raise ValueError(
            "No data was returned. Try a different ticker, date range, "
            "or interval."
        )

    data = data.reset_index()

    timestamp_column = "Datetime" if "Datetime" in data.columns else "Date"

    cleaned_data = data[[timestamp_column, "Close"]].copy()

    cleaned_data = cleaned_data.rename(
        columns={
            timestamp_column: "timestamp",
            "Close": "price",
        }
    )

    cleaned_data.insert(
        0,
        "asset",
        ticker,
    )

    cleaned_data = cleaned_data.dropna()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cleaned_data.to_csv(
        output_path,
        index=False,
    )

    return cleaned_data


sorted_stocks = sorted(
    COMMON_STOCKS,
    key=lambda stock: stock.ticker,
)

selected_stock = st.selectbox(
    "Stock",
    sorted_stocks,
    index=0,
    format_func=format_stock_option,
)

ticker = selected_stock.ticker

st.info(
    f"""
    **Ticker:** {selected_stock.ticker}  
    **Company:** {selected_stock.name}  
    **Data available from:** {selected_stock.suggested_start_date}
    """
)

st.divider()

st.subheader("Date range")

suggested_start_date = datetime.fromisoformat(
    selected_stock.suggested_start_date
).date()

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start date",
        value=max(
            suggested_start_date,
            date(2023, 2, 12),
        ),
        min_value=suggested_start_date,
        max_value=date.today(),
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=date(2024, 2, 11),
        min_value=start_date,
        max_value=date.today(),
    )

if end_date <= start_date:
    st.error("End date must be after start date.")

st.caption(
    "Note: yfinance treats the end date as exclusive, so the final row may "
    "be before the selected end date."
)

st.divider()

st.subheader("Interval")

interval_label = st.selectbox(
    "Download interval",
    list(INTERVAL_OPTIONS.keys()),
    index=0,
)

interval = INTERVAL_OPTIONS[interval_label]

st.write(f"Selected yfinance interval: `{interval}`")

st.divider()

st.subheader("Dataset name")

raw_dataset_name = st.text_input(
    "Dataset name",
    value=f"{ticker}-baseline",
    help=(
        f"The dataset name must start with {ticker}-. "
        "Spaces will be converted to hyphens."
    ),
)

dataset_name = normalise_dataset_name(
    ticker=ticker,
    user_input=raw_dataset_name,
)

output_filename = f"{dataset_name}_prices.csv"
output_path = DATA_DIR / output_filename

st.write("Preview filename:")
st.code(output_filename)

name_errors = validate_dataset_name(
    ticker=ticker,
    dataset_name=dataset_name,
    output_path=output_path,
)

for error in name_errors:
    st.error(error)

can_create = (
    end_date > start_date
    and len(name_errors) == 0
)

if st.button(
    "Create dataset",
    type="primary",
    disabled=not can_create,
):
    try:
        with st.spinner("Downloading data from yfinance..."):
            cleaned_data = download_dataset(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                interval=interval,
                output_path=output_path,
            )

        st.session_state.selected_dataset_path = str(output_path)
        st.session_state.selected_dataset_name = output_path.name
        st.session_state.selected_training_dataset_path = str(output_path)

        st.success("Dataset created successfully.")

        st.metric("Rows", len(cleaned_data))

        if "timestamp" in cleaned_data.columns:
            st.write(f"Start: `{cleaned_data['timestamp'].min()}`")
            st.write(f"End: `{cleaned_data['timestamp'].max()}`")

        st.write(f"Saved to: `{output_path}`")

        st.subheader("Preview")
        st.dataframe(cleaned_data.head(20))

        st.toast("Dataset created successfully.")

    except Exception as error:
        st.error(str(error))

st.divider()

if st.session_state.selected_dataset_path:
    st.subheader("Next step")

    st.write(
        f"Selected dataset: "
        f"`{st.session_state.selected_dataset_name}`"
    )

    if st.button("Train using this dataset"):
        st.switch_page("views/train_model.py")