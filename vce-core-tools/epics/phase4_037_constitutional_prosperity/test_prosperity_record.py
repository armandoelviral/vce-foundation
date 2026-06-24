from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


def test_prosperity_record_creation():
    record = ProsperityRecord(
        prosperity_id="prosperity.001",
        source_id="sustainability.001",
        prosperity_amount=100,
        rationale="sustainable capacity expansion",
    )

    assert record.prosperity_id == "prosperity.001"
    assert record.source_id == "sustainability.001"
    assert record.prosperity_amount == 100
    assert record.rationale == "sustainable capacity expansion"


def test_rejects_empty_prosperity_id():
    try:
        ProsperityRecord(
            prosperity_id="",
            source_id="sustainability.001",
            prosperity_amount=100,
            rationale="invalid",
        )
        assert False
    except ValueError as exc:
        assert "prosperity_id" in str(exc)


def test_rejects_non_positive_prosperity_amount():
    try:
        ProsperityRecord(
            prosperity_id="prosperity.001",
            source_id="sustainability.001",
            prosperity_amount=0,
            rationale="invalid",
        )
        assert False
    except ValueError as exc:
        assert "prosperity_amount" in str(exc)

