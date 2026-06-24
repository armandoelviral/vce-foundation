from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)
from epics.phase8_001_temporal_validity.validity_state import (
    ValidityState,
)


def test_builds_validity_state():
    records = [
        ValidityRecord(
            "validity.001",
            "evidence.001",
            365,
        ),
        ValidityRecord(
            "validity.002",
            "evidence.002",
            730,
        ),
    ]

    state = ValidityState.from_records(records)

    assert state.total_records == 2
    assert state.total_days == 1095


def test_empty_validity_state():
    state = ValidityState.from_records([])

    assert state.total_records == 0
    assert state.total_days == 0
