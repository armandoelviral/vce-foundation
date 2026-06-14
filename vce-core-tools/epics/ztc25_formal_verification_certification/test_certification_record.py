from epics.ztc25_formal_verification_certification.certification_record import (
    CertificationRecord,
)


def test_record_contains_certification_id():

    record = CertificationRecord(
        certification_id="cert-001",
        certified=True,
        reason="all_safety_properties_validated",
    )

    assert record.certification_id == "cert-001"


def test_record_contains_certification_status():

    record = CertificationRecord(
        certification_id="cert-001",
        certified=True,
        reason="all_safety_properties_validated",
    )

    assert record.certified is True


def test_record_contains_reason():

    record = CertificationRecord(
        certification_id="cert-001",
        certified=False,
        reason="safety_property_violation",
    )

    assert record.reason == "safety_property_violation"


def test_record_serializes():

    record = CertificationRecord(
        certification_id="cert-001",
        certified=True,
        reason="all_safety_properties_validated",
    )

    assert record.to_dict() == {
        "certification_id": "cert-001",
        "certified": True,
        "reason": "all_safety_properties_validated",
    }

