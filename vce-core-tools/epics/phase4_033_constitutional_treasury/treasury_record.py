from dataclasses import dataclass


@dataclass(frozen=True)
class TreasuryRecord:
    treasury_id: str
    authority_id: str
    allocation_amount: int
    reserve_reference: str

    def __post_init__(self):
        if not self.treasury_id:
            raise ValueError("treasury_id is required")

        if not self.authority_id:
            raise ValueError("authority_id is required")

        if self.allocation_amount <= 0:
            raise ValueError(
                "allocation_amount must be positive"
            )

        if not self.reserve_reference:
            raise ValueError(
                "reserve_reference is required"
            )
