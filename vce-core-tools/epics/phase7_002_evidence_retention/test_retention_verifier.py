from epics.phase7_002_evidence_retention.retention_state import (
    RetentionState,
)
from epics.phase7_002_evidence_retention.retention_verifier import (
    verify_retention,
)


def test_retention_verified():
    state = RetentionState(
        total_records=2,
        total_years=35,
    )

    result = verify_retention(state)

    assert result["verified"] is True


def test_empty_retention_not_verified():
    state = RetentionState(
        total_records=0,
        total_years=0,
    )

    result = verify_retention(state)

    assert result["verified"] is False
