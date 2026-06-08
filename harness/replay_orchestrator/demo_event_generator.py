import time
from itertools import islice
from pathlib import Path

from harness.replay_orchestrator.event_generator import generate_events


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_1d_prices.csv"


def main() -> None:
    events = generate_events(
        csv_path=CSV_PATH,
        experiment_id="EXP-LOCAL-DEMO-001",
        architecture_id="A0-local",
    )

    for event in islice(events, 5):
        print(event)
        time.sleep(2)


if __name__ == "__main__":
    main()