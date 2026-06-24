from epics.phase7_004_evidence_durability.durability_state import (
    DurabilityState,
)
from epics.phase7_004_evidence_durability.durability_verifier import (
    verify_durability,
)


def test_durability_verified():
    state = DurabilityState(
        total_records=2,
        total_years=75,
    )

    result = verify_durability(state)

    assert result["verified"] is True


def test_empty_durability_not_verified():
    state = DurabilityState(
        total_records=0,
        total_years=0,
    )

    result = verify_durability(state)

    assert result["verified"] is False
