from pathlib import Path

from harness.replay_orchestrator.event_generator import generate_events


def test_generate_events_from_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample_prices.csv"

    csv_path.write_text(
        "asset,timestamp,price\n"
        "AAPL,2025-01-02,100.00\n"
        "AAPL,2025-01-03,103.00\n",
        encoding="utf-8",
    )

    events = list(
        generate_events(
            csv_path=csv_path,
            experiment_id="EXP-TEST-001",
            architecture_id="A0-local",
        )
    )

    assert len(events) == 2

    assert events[0].event_id == "EXP-TEST-001-event-000001"
    assert events[0].asset == "AAPL"
    assert events[0].price == 100.00

    assert events[1].event_id == "EXP-TEST-001-event-000002"
    assert events[1].asset == "AAPL"
    assert events[1].price == 103.00