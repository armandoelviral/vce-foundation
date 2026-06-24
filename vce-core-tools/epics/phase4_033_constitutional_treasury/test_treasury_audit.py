from epics.phase4_033_constitutional_treasury.treasury_audit import (
    audit_treasury,
)
from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


def test_treasury_audit():
    allocations = [
        TreasuryRecord(
            treasury_id="treasury.001",
            authority_id="council",
            allocation_amount=100,
            reserve_reference="reserve.001",
        )
    ]

    disbursements = [
        TreasuryDisbursementRecord(
            disbursement_id="d1",
            treasury_id="treasury.001",
            disbursement_amount=40,
            purpose="insurance support",
        )
    ]

    audit = audit_treasury(
        allocations,
        disbursements,
    )

    assert audit["total_allocated"] == 100
    assert audit["total_disbursed"] == 40


def test_empty_treasury_audit():
    audit = audit_treasury([], [])

    assert audit["total_allocated"] == 0
    assert audit["total_disbursed"] == 0
