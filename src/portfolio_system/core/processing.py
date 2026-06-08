from portfolio_system.adapters.local_decision_repo import LocalDecisionRepository
from portfolio_system.core.decision_logic import generate_decision
from portfolio_system.domain.decisions import PortfolioDecision
from portfolio_system.domain.events import MarketEvent


def process_event(event: MarketEvent, previous_price: float, repository: LocalDecisionRepository) -> PortfolioDecision:
    decision = generate_decision(event=event, previous_price=previous_price,)

    repository.save(decision)

    return decision