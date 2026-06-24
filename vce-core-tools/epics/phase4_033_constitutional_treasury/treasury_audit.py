from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


def audit_treasury(
    allocations: list[TreasuryRecord],
    disbursements: list[TreasuryDisbursementRecord],
):
    return {
        "total_allocated": sum(
            a.allocation_amount
            for a in allocations
        ),
        "total_disbursed": sum(
            d.disbursement_amount
            for d in disbursements
        ),
    }
