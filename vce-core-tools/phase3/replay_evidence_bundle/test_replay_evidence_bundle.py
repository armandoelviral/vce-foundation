from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


def test_bundle_starts_empty():

    bundle = ReplayEvidenceBundle()

    assert bundle.count() == 0


def test_bundle_accepts_record():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    assert bundle.count() == 1


def test_bundle_returns_records():

    bundle = ReplayEvidenceBundle()

    record = ReplayEvidenceRecord(
        evidence_id="policy-001",
        evidence_type="policy",
    )

    bundle.add(record)

    records = bundle.records()

    assert len(records) == 1
    assert records[0] == record


def test_bundle_serializes():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    assert bundle.to_dict() == {
        "count": 1,
        "records": [
            {
                "evidence_id": "policy-001",
                "evidence_type": "policy",
            }
        ],
    }
