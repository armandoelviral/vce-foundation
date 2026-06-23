from dataclasses import dataclass


@dataclass(frozen=True)
class CreditRecord:
    credit_id: str
    borrower_id: str
    credit_amount: int
    obligation_reference: str

    def __post_init__(self):
        if not self.credit_id:
            raise ValueError("credit_id is required")

        if not self.borrower_id:
            raise ValueError("borrower_id is required")

        if self.credit_amount <= 0:
            raise ValueError("credit_amount must be positive")

        if not self.obligation_reference:
            raise ValueError("obligation_reference is required")
