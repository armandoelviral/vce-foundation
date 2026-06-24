from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)
from epics.phase8_002_trust_expiration.expiration_state import (
    ExpirationState,
)


def test_builds_expiration_state():
    records = [
        ExpirationRecord(
            "exp.001",
            "trust.001",
            365,
        ),
        ExpirationRecord(
            "exp.002",
            "trust.002",
            30,
        ),
    ]

    state = ExpirationState.from_records(records)

    assert state.total_records == 2
    assert state.total_remaining_days == 395


def test_empty_expiration_state():
    state = ExpirationState.from_records([])

    assert state.total_records == 0
    assert state.total_remaining_days == 0
