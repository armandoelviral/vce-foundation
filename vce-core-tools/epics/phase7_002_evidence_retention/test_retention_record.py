from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)


def test_retention_record_creation():
    record = RetentionRecord(
        retention_id="ret.001",
        evidence_id="evidence.001",
        retention_years=25,
    )

    assert record.retention_years == 25


def test_requires_retention_id():
    try:
        RetentionRecord(
            "",
            "evidence.001",
            25,
        )
        assert False
    except ValueError as exc:
        assert "retention_id" in str(exc)
