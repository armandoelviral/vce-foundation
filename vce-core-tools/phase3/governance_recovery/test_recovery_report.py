from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_report import (
    RecoveryReport,
)


def test_report_contains_recovery_count():

    report = RecoveryReport(
        {
            "rec-001": RecoveryRecord(
                recovery_id="rec-001",
                incident_id="esc-001",
                recovery_reason="manual_remediation",
            )
        }
    )

    assert report.recovery_count() == 1


def test_report_lists_recovery_ids():

    report = RecoveryReport(
        {
            "rec-001": RecoveryRecord(
                recovery_id="rec-001",
                incident_id="esc-001",
                recovery_reason="manual_remediation",
            ),
            "rec-002": RecoveryRecord(
                recovery_id="rec-002",
                incident_id="esc-002",
                recovery_reason="automatic_recovery",
            ),
        }
    )

    assert report.recovery_ids() == [
        "rec-001",
        "rec-002",
    ]


def test_report_serializes():

    report = RecoveryReport(
        {
            "rec-001": RecoveryRecord(
                recovery_id="rec-001",
                incident_id="esc-001",
                recovery_reason="manual_remediation",
            )
        }
    )

    assert report.to_dict() == {
        "recovery_count": 1,
        "recovery_ids": [
            "rec-001",
        ],
    }
