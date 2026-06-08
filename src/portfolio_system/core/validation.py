from datetime import datetime

from portfolio_system.domain.events import MarketEvent


"""
Simply checks the validity of an Event instance
If an event is invalid, raise an error relating to the reason

Does not do context checking (e.g., valid date, relative to previous dates)
Only checks that the event instance has all information and is in correct formatting
"""
class InvalidMarketEventError(ValueError):
    """Raised when an incoming market event is invalid."""


def validate_market_event(event: MarketEvent) -> None:

    # not a valid event instance
    if not isinstance(event, MarketEvent):
        raise InvalidMarketEventError("Event must be a MarketEvent object.")

    # missing event ID
    if not event.event_id.strip():
        raise InvalidMarketEventError("Missing Event ID")

    # missing asset code
    if not event.asset.strip():
        raise InvalidMarketEventError("Missing Asset")

    # invalid price
    if event.price <= 0:
        raise InvalidMarketEventError("Price must be greater than zero")

    # invalid timestamp type
    if not isinstance(event.market_timestamp, datetime):
        raise InvalidMarketEventError("Timestamp must be a datetime object")

    # 
    if not event.experiment_id.strip():
        raise InvalidMarketEventError("Missing Experiment ID")

    if not event.architecture_id.strip():
        raise InvalidMarketEventError("Missing architecture ID")
    