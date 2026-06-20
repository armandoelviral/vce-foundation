from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_report import (
    ExecutionReport,
)


def test_report_contains_request_count():

    report = ExecutionReport(
        {
            "request-001":
                ExecutionRequestRecord(
                    request_id="request-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    subject="runtime-state-root",
                )
        }
    )

    assert report.request_count() == 1


def test_report_lists_request_ids():

    report = ExecutionReport(
        {
            "request-001":
                ExecutionRequestRecord(
                    request_id="request-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    subject="runtime-state-root",
                ),

            "request-002":
                ExecutionRequestRecord(
                    request_id="request-002",
                    resource_type="WITNESS",
                    action="SUSPEND",
                    subject="did:vcr:gcp:us-central1:fp001",
                ),
        }
    )

    assert report.request_ids() == [
        "request-001",
        "request-002",
    ]


def test_report_serializes():

    report = ExecutionReport(
        {
            "request-001":
                ExecutionRequestRecord(
                    request_id="request-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    subject="runtime-state-root",
                )
        }
    )

    assert report.to_dict() == {
        "request_count": 1,
        "request_ids": [
            "request-001",
        ],
    }
