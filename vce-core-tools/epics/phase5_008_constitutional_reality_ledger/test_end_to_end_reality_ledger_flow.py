from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_registry import (
    RealityLedgerRegistry,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_state import (
    RealityLedgerState,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_verifier import (
    verify_reality_ledger,
)


def test_end_to_end_reality_ledger_flow():
    registry = RealityLedgerRegistry()

    registry.add(
        RealityLedgerRecord(
            ledger_id="ledger.001",
            claim_id="claim.001",
            consensus_id="consensus.001",
        )
    )

    state = RealityLedgerState.from_records(
        registry.records()
    )

    verification = verify_reality_ledger(state)

    assert verification["verified"] is True
    assert verification["total_entries"] == 1
