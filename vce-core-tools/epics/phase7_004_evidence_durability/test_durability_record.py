from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)


def test_durability_record_creation():
    record = DurabilityRecord(
        durability_id="dur.001",
        evidence_id="evidence.001",
        durability_years=50,
    )

    assert record.durability_years == 50


def test_requires_durability_id():
    try:
        DurabilityRecord(
            "",
            "evidence.001",
            50,
        )
        assert False
    except ValueError as exc:
        assert "durability_id" in str(exc)
