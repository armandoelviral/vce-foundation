from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)


def test_validity_record_creation():
    record = ValidityRecord(
        validity_id="validity.001",
        evidence_id="evidence.001",
        valid_days=365,
    )

    assert record.valid_days == 365


def test_requires_validity_id():
    try:
        ValidityRecord(
            "",
            "evidence.001",
            365,
        )
        assert False
    except ValueError as exc:
        assert "validity_id" in str(exc)
