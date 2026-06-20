from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_request_registry import (
    ExecutionRequestRegistry,
)


def test_registry_starts_empty():

    registry = ExecutionRequestRegistry()

    assert registry.count() == 0


def test_registry_accepts_request():

    registry = ExecutionRequestRegistry()

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    registry.add(request)

    assert registry.count() == 1


def test_registry_returns_request():

    registry = ExecutionRequestRegistry()

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    registry.add(request)

    recovered = registry.get(
        "request-001"
    )

    assert recovered == request


def test_missing_request_returns_none():

    registry = ExecutionRequestRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_request_ids():

    registry = ExecutionRequestRegistry()

    registry.add(
        ExecutionRequestRecord(
            request_id="request-001",
            resource_type="REPLAY",
            action="EXECUTE",
            subject="runtime-state-root",
        )
    )

    registry.add(
        ExecutionRequestRecord(
            request_id="request-002",
            resource_type="WITNESS",
            action="SUSPEND",
            subject="did:vcr:gcp:us-central1:fp001",
        )
    )

    assert registry.request_ids() == [
        "request-001",
        "request-002",
    ]
