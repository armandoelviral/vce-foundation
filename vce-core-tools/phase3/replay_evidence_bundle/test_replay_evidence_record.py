from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)


def test_record_contains_evidence_id():

    record = ReplayEvidenceRecord(
        evidence_id="policy-001",
        evidence_type="policy",
    )

    assert record.evidence_id == "policy-001"


def test_record_contains_type():

    record = ReplayEvidenceRecord(
        evidence_id="policy-001",
        evidence_type="policy",
    )

    assert record.evidence_type == "policy"


def test_record_serializes():

    record = ReplayEvidenceRecord(
        evidence_id="policy-001",
        evidence_type="policy",
    )

    assert record.to_dict() == {
        "evidence_id": "policy-001",
        "evidence_type": "policy",
    }
