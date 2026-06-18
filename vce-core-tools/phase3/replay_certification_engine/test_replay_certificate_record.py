from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)


def test_record_contains_certificate_id():

    record = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    assert record.certificate_id == "cert-001"


def test_record_contains_replay_id():

    record = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    assert record.replay_id == "replay-001"


def test_record_contains_status():

    record = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    assert record.status == "PASS"


def test_record_serializes():

    record = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    assert record.to_dict() == {
        "certificate_id": "cert-001",
        "replay_id": "replay-001",
        "status": "PASS",
    }
