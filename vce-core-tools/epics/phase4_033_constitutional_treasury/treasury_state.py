from dataclasses import dataclass

from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


@dataclass(frozen=True)
class TreasuryState:
    total_allocated: int
    total_disbursed: int
    remaining_capacity: int

    @classmethod
    def from_records(
        cls,
        allocations,
        disbursements,
    ):
        total_allocated = sum(
            a.allocation_amount
            for a in allocations
        )

        total_disbursed = sum(
            d.disbursement_amount
            for d in disbursements
        )

        return cls(
            total_allocated=total_allocated,
            total_disbursed=total_disbursed,
            remaining_capacity=(
                total_allocated
                - total_disbursed
            ),
        )
