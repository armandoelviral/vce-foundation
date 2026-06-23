from epics.phase4_031_constitutional_insurance.insurance_state import (
    InsuranceState,
)


def verify_insurance_state(
    state: InsuranceState,
) -> dict:
    return {
        "verified": state.remaining_coverage >= 0,
        "total_coverage": state.total_coverage,
        "total_claims": state.total_claims,
        "remaining_coverage": state.remaining_coverage,
    }
