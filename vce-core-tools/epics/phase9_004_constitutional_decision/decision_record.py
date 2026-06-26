from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    proposal_id: str
    outcome: str

    def __post_init__(self):
        if not self.decision_id:
            raise ValueError("decision_id is required")

        if not self.proposal_id:
            raise ValueError("proposal_id is required")

        if not self.outcome:
            raise ValueError("outcome is required")
