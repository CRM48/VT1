import csv
from datetime import datetime
from pathlib import Path
from typing import Iterator

from portfolio_system.domain.events import MarketEvent

"""
Generate a MarketEvent for each row in a csv file.
"""


def generate_events(csv_path: Path, experiment_id: str = "EXP-LOCAL-001", architecture_id: str = "A0-local") -> Iterator[MarketEvent]:
    with csv_path.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=1):
            event = MarketEvent(
                event_id=f"{experiment_id}-event-{row_number:06d}",
                asset=row["asset"],
                price=float(row["price"]),
                market_timestamp=datetime.fromisoformat(row["timestamp"]),
                experiment_id=experiment_id,
                architecture_id=architecture_id,
            )

            yield event