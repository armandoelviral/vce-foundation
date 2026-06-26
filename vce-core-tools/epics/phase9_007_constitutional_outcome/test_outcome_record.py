from epics.phase9_007_constitutional_outcome.outcome_record import (
    OutcomeRecord,
)


def test_outcome_record_creation():
    record = OutcomeRecord(
        outcome_id="outcome.001",
        execution_id="execution.001",
        status="successful",
    )

    assert record.outcome_id == "outcome.001"
    assert record.status == "successful"


def test_requires_outcome_id():
    try:
        OutcomeRecord(
            "",
            "execution.001",
            "successful",
        )
        assert False
    except ValueError as exc:
        assert "outcome_id" in str(exc)
