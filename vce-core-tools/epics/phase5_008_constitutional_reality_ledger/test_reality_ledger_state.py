from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_state import (
    RealityLedgerState,
)


def test_builds_state():
    records = [
        RealityLedgerRecord(
            "ledger.001",
            "claim.001",
            "consensus.001",
        )
    ]

    state = RealityLedgerState.from_records(records)

    assert state.total_entries == 1
