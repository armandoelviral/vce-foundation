from epics.phase8_001_temporal_validity.validity_state import (
    ValidityState,
)
from epics.phase8_001_temporal_validity.validity_verifier import (
    verify_validity,
)


def test_validity_verified():
    state = ValidityState(
        total_records=2,
        total_days=1095,
    )

    result = verify_validity(state)

    assert result["verified"] is True


def test_empty_validity_not_verified():
    state = ValidityState(
        total_records=0,
        total_days=0,
    )

    result = verify_validity(state)

    assert result["verified"] is False
