import yfinance as yf
import pandas as pd

class YFinanceDataLoader:
    def __init__(self, ticker, start, end, interval="1h"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval

    def load(self):
        df = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            interval=self.interval
        )

        df = df.reset_index()

        # Standardise column names
        df.columns = [col.lower() for col in df.columns]

        # Ensure consistent ordering
        df = df.sort_values("datetime" if "datetime" in df.columns else "date")

        # Rename timestamp column consistently
        if "datetime" in df.columns:
            df = df.rename(columns={"datetime": "timestamp"})
        elif "date" in df.columns:
            df = df.rename(columns={"date": "timestamp"})

        # Remove missing rows
        df = df.dropna()

        return df