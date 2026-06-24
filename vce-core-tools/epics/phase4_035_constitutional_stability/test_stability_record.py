from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


def test_stability_record_creation():
    record = StabilityRecord(
        stability_id="stability.001",
        source_id="treasury.001",
        stability_amount=100,
        rationale="constitutional continuity",
    )

    assert record.stability_amount == 100


def test_rejects_empty_id():
    try:
        StabilityRecord(
            stability_id="",
            source_id="treasury.001",
            stability_amount=100,
            rationale="test",
        )
        assert False
    except ValueError as exc:
        assert "stability_id" in str(exc)


def test_rejects_non_positive_amount():
    try:
        StabilityRecord(
            stability_id="stability.001",
            source_id="treasury.001",
            stability_amount=0,
            rationale="test",
        )
        assert False
    except ValueError as exc:
        assert "stability_amount" in str(exc)
