from dataclasses import dataclass


@dataclass(frozen=True)
class CreditDefaultRecord:
    default_id: str
    credit_id: str
    reason: str

    def __post_init__(self):
        if not self.default_id:
            raise ValueError("default_id is required")

        if not self.credit_id:
            raise ValueError("credit_id is required")

        if not self.reason:
            raise ValueError("reason is required")
