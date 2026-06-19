from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)


def test_record_contains_revocation_id():

    record = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    assert record.revocation_id == "rev-001"


def test_record_contains_certificate_id():

    record = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    assert record.certificate_id == "cert-001"


def test_record_contains_reason():

    record = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    assert record.reason == "key_compromise"


def test_record_serializes():

    record = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    assert record.to_dict() == {
        "revocation_id": "rev-001",
        "certificate_id": "cert-001",
        "reason": "key_compromise",
    }
