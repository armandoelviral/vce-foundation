from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_registry import (
    TreasuryRegistry,
)
from epics.phase4_033_constitutional_treasury.treasury_state import (
    TreasuryState,
)
from epics.phase4_033_constitutional_treasury.treasury_verifier import (
    verify_treasury_state,
)


def test_end_to_end_treasury_flow():
    registry = TreasuryRegistry()

    registry.add(
        TreasuryRecord(
            treasury_id="treasury.001",
            authority_id="treasury.council",
            allocation_amount=100,
            reserve_reference="reserve.001",
        )
    )

    disbursement = TreasuryDisbursementRecord(
        disbursement_id="d1",
        treasury_id="treasury.001",
        disbursement_amount=40,
        purpose="insurance support",
    )

    state = TreasuryState.from_records(
        allocations=registry.records(),
        disbursements=[disbursement],
    )

    assert state.total_allocated == 100
    assert state.total_disbursed == 40
    assert state.remaining_capacity == 60

    verification = verify_treasury_state(state)

    assert verification["verified"] is True
