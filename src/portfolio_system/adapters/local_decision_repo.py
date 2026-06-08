import json
from dataclasses import asdict
from pathlib import Path

from portfolio_system.domain.decisions import PortfolioDecision


class LocalDecisionRepository:
    """
    Saves portfolio decisions to a local JSONL file.

    JSONL means that each line contains one JSON object.
    """

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

        # Create the parent folder if it does not already exist.
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, decision: PortfolioDecision) -> None:
        """
        Append one decision to the output file.
        """

        decision_data = asdict(decision)

        # Enums and datetime objects must be converted before saving as JSON.
        decision_data["action"] = decision.action.value
        decision_data["processed_at"] = decision.processed_at.isoformat()

        with self.output_path.open(mode="a", encoding="utf-8") as file:
            file.write(json.dumps(decision_data) + "\n")

    def clear(self) -> None:
        """
        Delete previous results so a new experiment starts with an empty file.
        """

        if self.output_path.exists():
            self.output_path.unlink()