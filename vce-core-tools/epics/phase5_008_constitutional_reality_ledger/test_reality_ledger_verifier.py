from epics.phase5_008_constitutional_reality_ledger.reality_ledger_state import (
    RealityLedgerState,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_verifier import (
    verify_reality_ledger,
)


def test_verifies_ledger():
    state = RealityLedgerState(
        total_entries=1,
    )

    result = verify_reality_ledger(state)

    assert result["verified"] is True
