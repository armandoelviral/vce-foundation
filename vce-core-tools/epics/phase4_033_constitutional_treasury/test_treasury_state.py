from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_state import (
    TreasuryState,
)


def test_builds_treasury_state():
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

    state = TreasuryState.from_records(
        allocations=allocations,
        disbursements=disbursements,
    )

    assert state.remaining_capacity == 60


def test_empty_state():
    state = TreasuryState.from_records(
        allocations=[],
        disbursements=[],
    )

    assert state.remaining_capacity == 0
