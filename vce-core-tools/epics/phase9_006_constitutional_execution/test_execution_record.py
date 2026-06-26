from epics.phase9_006_constitutional_execution.execution_record import (
    ExecutionRecord,
)


def test_execution_record_creation():
    record = ExecutionRecord(
        execution_id="execution.001",
        delegation_id="delegation.001",
        status="completed",
    )

    assert record.execution_id == "execution.001"
    assert record.status == "completed"


def test_requires_execution_id():
    try:
        ExecutionRecord(
            "",
            "delegation.001",
            "completed",
        )
        assert False
    except ValueError as exc:
        assert "execution_id" in str(exc)
