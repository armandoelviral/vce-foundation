from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)
from epics.phase7_004_evidence_durability.durability_state import (
    DurabilityState,
)


def test_builds_durability_state():
    records = [
        DurabilityRecord(
            "dur.001",
            "evidence.001",
            50,
        ),
        DurabilityRecord(
            "dur.002",
            "evidence.002",
            25,
        ),
    ]

    state = DurabilityState.from_records(records)

    assert state.total_records == 2
    assert state.total_years == 75


def test_empty_durability_state():
    state = DurabilityState.from_records([])

    assert state.total_records == 0
    assert state.total_years == 0
