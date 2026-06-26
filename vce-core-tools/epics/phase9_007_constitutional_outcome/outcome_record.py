from dataclasses import dataclass


@dataclass(frozen=True)
class OutcomeRecord:
    outcome_id: str
    execution_id: str
    status: str

    def __post_init__(self):
        if not self.outcome_id:
            raise ValueError("outcome_id is required")

        if not self.execution_id:
            raise ValueError("execution_id is required")

        if not self.status:
            raise ValueError("status is required")
