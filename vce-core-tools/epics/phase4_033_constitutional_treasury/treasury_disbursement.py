from dataclasses import dataclass


@dataclass(frozen=True)
class TreasuryDisbursementRecord:
    disbursement_id: str
    treasury_id: str
    disbursement_amount: int
    purpose: str

    def __post_init__(self):
        if not self.disbursement_id:
            raise ValueError(
                "disbursement_id is required"
            )

        if not self.treasury_id:
            raise ValueError(
                "treasury_id is required"
            )

        if self.disbursement_amount <= 0:
            raise ValueError(
                "disbursement_amount must be positive"
            )

        if not self.purpose:
            raise ValueError(
                "purpose is required"
            )
