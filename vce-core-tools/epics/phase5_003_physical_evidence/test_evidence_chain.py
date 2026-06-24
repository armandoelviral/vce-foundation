from epics.phase5_003_physical_evidence.evidence_chain import (
    build_evidence_chain,
)
from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)


def test_builds_evidence_chain():
    records = [
        EvidenceRecord(
            "e1",
            "obs.001",
            "photo",
            "hash1",
        ),
        EvidenceRecord(
            "e2",
            "obs.001",
            "video",
            "hash2",
        ),
    ]

    chain = build_evidence_chain(records)

    assert chain["evidence_count"] == 2


def test_empty_chain():
    chain = build_evidence_chain([])

    assert chain["evidence_count"] == 0
