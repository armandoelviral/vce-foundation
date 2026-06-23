from dataclasses import dataclass

from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)


@dataclass(frozen=True)
class CreditState:
    credit_count: int
    total_credit: int

    @classmethod
    def from_credits(
        cls,
        credits: list[CreditRecord],
    ):
        return cls(
            credit_count=len(credits),
            total_credit=sum(
                credit.credit_amount
                for credit in credits
            ),
        )
