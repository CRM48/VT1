from pathlib import Path

from portfolio_system.adapters.local_decision_repo import LocalDecisionRepository
from portfolio_system.core.processing import process_event
from harness.replay_orchestrator.event_generator import generate_events


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "AAPL_1d_prices.csv"
OUTPUT_PATH = PROJECT_ROOT / "experiments" / "raw" / "EXP-LOCAL-REPLAY-001-decisions.jsonl"


def main() -> None:
    experiment_id = "EXP-LOCAL-REPLAY-001"
    architecture_id = "A0-local"

    repository = LocalDecisionRepository(OUTPUT_PATH)

    # Remove output from any earlier run with the same experiment ID.
    repository.clear()

    events = generate_events(csv_path=CSV_PATH, experiment_id=experiment_id, architecture_id=architecture_id)

    previous_prices: dict[str, float] = {}

    processed_count = 0
    skipped_count = 0

    for event in events:
        if event.asset not in previous_prices:
            # The first event has nothing to compare against.
            previous_prices[event.asset] = event.price
            skipped_count += 1
            continue

        decision = process_event(event=event, previous_price=previous_prices[event.asset], repository=repository)

        print(decision)
        print()

        # The current price becomes the previous price for the next event.
        previous_prices[event.asset] = event.price

        processed_count += 1

    print("Replay complete:")
    print(f"  Decisions created = {processed_count}")
    print(f"  Events skipped = {skipped_count}")
    print(f"  Results saved to = {OUTPUT_PATH}")


if __name__ == "__main__":
    main()