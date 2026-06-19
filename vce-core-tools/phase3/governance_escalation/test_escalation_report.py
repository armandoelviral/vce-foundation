from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.escalation_report import (
    EscalationReport,
)


def test_report_contains_escalation_count():

    report = EscalationReport(
        {
            "esc-001": EscalationRecord(
                escalation_id="esc-001",
                reason="quorum_failure",
                severity="HIGH",
            )
        }
    )

    assert report.escalation_count() == 1


def test_report_lists_escalation_ids():

    report = EscalationReport(
        {
            "esc-001": EscalationRecord(
                escalation_id="esc-001",
                reason="quorum_failure",
                severity="HIGH",
            ),
            "esc-002": EscalationRecord(
                escalation_id="esc-002",
                reason="witness_divergence",
                severity="MEDIUM",
            ),
        }
    )

    assert report.escalation_ids() == [
        "esc-001",
        "esc-002",
    ]


def test_report_serializes():

    report = EscalationReport(
        {
            "esc-001": EscalationRecord(
                escalation_id="esc-001",
                reason="quorum_failure",
                severity="HIGH",
            )
        }
    )

    assert report.to_dict() == {
        "escalation_count": 1,
        "escalation_ids": [
            "esc-001",
        ],
    }
