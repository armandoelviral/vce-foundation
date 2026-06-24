from epics.phase5_008_constitutional_reality_ledger.reality_ledger_state import (
    RealityLedgerState,
)


def verify_reality_ledger(
    state: RealityLedgerState,
):
    return {
        "verified": state.total_entries > 0,
        "total_entries": state.total_entries,
    }
