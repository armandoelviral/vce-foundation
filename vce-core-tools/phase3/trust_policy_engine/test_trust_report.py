from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)

from phase3.trust_policy_engine.trust_report import (
    TrustReport,
)


def test_report_contains_decision_count():

    report = TrustReport(
        {
            "decision-001": TrustDecision(
                status="TRUSTED"
            )
        }
    )

    assert report.decision_count() == 1


def test_report_lists_decisions():

    report = TrustReport(
        {
            "decision-001": TrustDecision(
                status="TRUSTED"
            ),
            "decision-002": TrustDecision(
                status="UNTRUSTED"
            ),
        }
    )

    assert report.decision_ids() == [
        "decision-001",
        "decision-002",
    ]


def test_report_serializes():

    report = TrustReport(
        {
            "decision-001": TrustDecision(
                status="TRUSTED"
            )
        }
    )

    assert report.to_dict() == {
        "decision_count": 1,
        "decision_ids": [
            "decision-001"
        ],
    }
