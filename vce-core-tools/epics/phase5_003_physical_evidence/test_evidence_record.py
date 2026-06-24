from epics.phase5_003_physical_evidence.evidence_record import (
    EvidenceRecord,
)


def test_evidence_record_creation():
    record = EvidenceRecord(
        evidence_id="evidence.001",
        observation_id="obs.001",
        evidence_type="photo",
        artifact_hash="abc123",
    )

    assert record.evidence_id == "evidence.001"
    assert record.observation_id == "obs.001"


def test_rejects_empty_evidence_id():
    try:
        EvidenceRecord(
            evidence_id="",
            observation_id="obs.001",
            evidence_type="photo",
            artifact_hash="abc123",
        )
        assert False
    except ValueError as exc:
        assert "evidence_id" in str(exc)


def test_rejects_empty_hash():
    try:
        EvidenceRecord(
            evidence_id="evidence.001",
            observation_id="obs.001",
            evidence_type="photo",
            artifact_hash="",
        )
        assert False
    except ValueError as exc:
        assert "artifact_hash" in str(exc)
