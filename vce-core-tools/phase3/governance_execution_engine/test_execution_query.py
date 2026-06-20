from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_request_registry import (
    ExecutionRequestRegistry,
)

from phase3.governance_execution_engine.execution_query import (
    ExecutionQuery,
)


def test_query_returns_request():

    registry = ExecutionRequestRegistry()

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    registry.add(request)

    query = ExecutionQuery(
        registry
    )

    result = query.by_id(
        "request-001"
    )

    assert result == request


def test_query_returns_none_for_missing():

    registry = ExecutionRequestRegistry()

    query = ExecutionQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_subject():

    registry = ExecutionRequestRegistry()

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    registry.add(request)

    query = ExecutionQuery(
        registry
    )

    result = query.by_id(
        "request-001"
    )

    assert (
        result.subject
        == "runtime-state-root"
    )
