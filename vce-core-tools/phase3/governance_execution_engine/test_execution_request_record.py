from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)


def test_contains_request_id():

    record = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        record.request_id
        == "request-001"
    )


def test_contains_resource_type():

    record = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        record.resource_type
        == "REPLAY"
    )


def test_contains_action():

    record = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        record.action
        == "EXECUTE"
    )


def test_contains_subject():

    record = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        record.subject
        == "runtime-state-root"
    )


def test_serializes():

    record = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert record.to_dict() == {
        "request_id":
            "request-001",

        "resource_type":
            "REPLAY",

        "action":
            "EXECUTE",

        "subject":
            "runtime-state-root",
    }
