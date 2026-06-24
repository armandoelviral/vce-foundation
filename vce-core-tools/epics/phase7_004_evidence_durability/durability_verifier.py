from epics.phase7_004_evidence_durability.durability_state import (
    DurabilityState,
)


def verify_durability(
    state: DurabilityState,
):
    return {
        "verified": state.total_years > 0,
        "total_years": state.total_years,
        "total_records": state.total_records,
    }
