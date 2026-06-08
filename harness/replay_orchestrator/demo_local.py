from datetime import datetime, timezone

from portfolio_system.core.decision_logic import generate_decision
from portfolio_system.domain.events import MarketEvent


def main() -> None:
    event = MarketEvent(
        event_id="evt-demo-001",
        asset="AAPL",
        price=103.0,
        market_timestamp=datetime.now(timezone.utc),
        experiment_id="EXP-LOCAL-DEMO-001",
        architecture_id="A0-local",
    )

    decision = generate_decision(
        event=event,
        previous_price=100.0,
    )

    print(event)
    print()
    print(decision)


if __name__ == "__main__":
    main()