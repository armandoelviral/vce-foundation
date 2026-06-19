from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)

from phase3.admission_control_engine.admission_report import (
    AdmissionReport,
)


def test_report_contains_decision_count():

    report = AdmissionReport(
        {
            "decision-001": AdmissionDecision(
                status="ALLOW"
            )
        }
    )

    assert report.decision_count() == 1


def test_report_lists_decision_ids():

    report = AdmissionReport(
        {
            "decision-001": AdmissionDecision(
                status="ALLOW"
            ),
            "decision-002": AdmissionDecision(
                status="DENY"
            ),
        }
    )

    assert report.decision_ids() == [
        "decision-001",
        "decision-002",
    ]


def test_report_serializes():

    report = AdmissionReport(
        {
            "decision-001": AdmissionDecision(
                status="ALLOW"
            )
        }
    )

    assert report.to_dict() == {
        "decision_count": 1,
        "decision_ids": [
            "decision-001",
        ],
    }
