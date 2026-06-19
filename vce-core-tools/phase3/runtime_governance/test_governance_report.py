from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)

from phase3.runtime_governance.governance_report import (
    GovernanceReport,
)


def test_report_contains_decision_count():

    report = GovernanceReport(
        {
            "decision-001": GovernanceDecision(
                status="APPROVED"
            )
        }
    )

    assert report.decision_count() == 1


def test_report_lists_decisions():

    report = GovernanceReport(
        {
            "decision-001": GovernanceDecision(
                status="APPROVED"
            ),
            "decision-002": GovernanceDecision(
                status="REJECTED"
            ),
        }
    )

    assert report.decision_ids() == [
        "decision-001",
        "decision-002",
    ]


def test_report_serializes():

    report = GovernanceReport(
        {
            "decision-001": GovernanceDecision(
                status="APPROVED"
            )
        }
    )

    assert report.to_dict() == {
        "decision_count": 1,
        "decision_ids": [
            "decision-001"
        ],
    }
