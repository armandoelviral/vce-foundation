from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)


def test_record_contains_entry_id():

    record = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    assert record.entry_id == "entry-001"


def test_record_contains_certificate_id():

    record = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    assert record.certificate_id == "cert-001"


def test_record_serializes():

    record = TransparencyCertificateRecord(
        entry_id="entry-001",
        certificate_id="cert-001",
    )

    assert record.to_dict() == {
        "entry_id": "entry-001",
        "certificate_id": "cert-001",
    }
