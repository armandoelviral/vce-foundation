from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)
from epics.phase5_003_physical_evidence.evidence_state import (
    EvidenceState,
)


def test_builds_evidence_state():
    records = [
        EvidenceRecord(
            "e1",
            "obs.001",
            "photo",
            "hash1",
        )
    ]

    state = EvidenceState.from_records(records)

    assert state.total_evidence == 1


def test_empty_state():
    state = EvidenceState.from_records([])

    assert state.total_evidence == 0
