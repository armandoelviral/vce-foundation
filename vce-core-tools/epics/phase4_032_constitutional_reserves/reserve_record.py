from dataclasses import dataclass


@dataclass(frozen=True)
class ReserveRecord:
    reserve_id: str
    institution_id: str
    reserve_amount: int
    source_reference: str

    def __post_init__(self):
        if not self.reserve_id:
            raise ValueError("reserve_id is required")

        if not self.institution_id:
            raise ValueError("institution_id is required")

        if self.reserve_amount <= 0:
            raise ValueError("reserve_amount must be positive")

        if not self.source_reference:
            raise ValueError("source_reference is required")
