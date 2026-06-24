from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)


def test_sustainability_depletion_creation():
    record = SustainabilityDepletionRecord(
        depletion_id="depletion.001",
        sustainability_id="sus.001",
        depletion_amount=40,
        reason="resource exhaustion",
    )

    assert record.depletion_id == "depletion.001"
    assert record.sustainability_id == "sus.001"
    assert record.depletion_amount == 40
    assert record.reason == "resource exhaustion"


def test_rejects_empty_depletion_id():
    try:
        SustainabilityDepletionRecord(
            depletion_id="",
            sustainability_id="sus.001",
            depletion_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "depletion_id" in str(exc)


def test_rejects_non_positive_depletion_amount():
    try:
        SustainabilityDepletionRecord(
            depletion_id="depletion.001",
            sustainability_id="sus.001",
            depletion_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "depletion_amount" in str(exc)
