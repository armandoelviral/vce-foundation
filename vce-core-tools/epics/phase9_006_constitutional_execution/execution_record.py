from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRecord:
    execution_id: str
    delegation_id: str
    status: str

    def __post_init__(self):
        if not self.execution_id:
            raise ValueError("execution_id is required")

        if not self.delegation_id:
            raise ValueError("delegation_id is required")

        if not self.status:
            raise ValueError("status is required")
