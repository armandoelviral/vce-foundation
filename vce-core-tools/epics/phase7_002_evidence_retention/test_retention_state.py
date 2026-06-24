from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)
from epics.phase7_002_evidence_retention.retention_state import (
    RetentionState,
)


def test_builds_retention_state():
    records = [
        RetentionRecord(
            "ret.001",
            "evidence.001",
            25,
        ),
        RetentionRecord(
            "ret.002",
            "evidence.002",
            10,
        ),
    ]

    state = RetentionState.from_records(records)

    assert state.total_records == 2
    assert state.total_years == 35


def test_empty_retention_state():
    state = RetentionState.from_records([])

    assert state.total_records == 0
    assert state.total_years == 0
