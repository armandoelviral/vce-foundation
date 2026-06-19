from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)

from phase3.runtime_enforcement_engine.enforcement_report import (
    EnforcementReport,
)


def test_report_contains_decision_count():

    report = EnforcementReport(
        {
            "decision-001": EnforcementDecision(
                status="EXECUTE"
            )
        }
    )

    assert report.decision_count() == 1


def test_report_lists_decision_ids():

    report = EnforcementReport(
        {
            "decision-001": EnforcementDecision(
                status="EXECUTE"
            ),
            "decision-002": EnforcementDecision(
                status="BLOCK"
            ),
        }
    )

    assert report.decision_ids() == [
        "decision-001",
        "decision-002",
    ]


def test_report_serializes():

    report = EnforcementReport(
        {
            "decision-001": EnforcementDecision(
                status="EXECUTE"
            )
        }
    )

    assert report.to_dict() == {
        "decision_count": 1,
        "decision_ids": [
            "decision-001",
        ],
    }
