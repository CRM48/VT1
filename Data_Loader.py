import yfinance as yf
import matplotlib.pyplot as plt
import time

# 1. Fetch the historical stock data
ticker_symbol = "AAPL"
data = yf.download(ticker_symbol, start="2025-01-01", end="2026-01-01", interval="1h")
print(data.head())

data = data.reset_index()

data = data[["Datetime", "Open", "High", "Low", "Close", "Volume"]]
data.columns = ["timestamp", "open", "high", "low", "close", "volume"]


class YFinanceReplayEngine:
    def __init__(self, data, speed=1.0):
        self.data = data
        self.speed = speed

    def stream(self):
        for _, row in self.data.iterrows():

            event = {
                "timestamp": row["timestamp"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"]
            }

            yield event

            # simulate time passing
            time.sleep(1.0 / self.speed)

engine = YFinanceReplayEngine(data, speed=5)

for event in engine.stream():
    print(event)