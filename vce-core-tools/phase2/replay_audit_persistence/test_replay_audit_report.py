from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)

from phase2.replay_audit_persistence.replay_audit_report import (
    ReplayAuditReport,
)


def test_report_contains_total_audits():

    records = [
        ReplayAuditRecord(
            replay_id="replay-001",
            audit_result=True,
        ),
        ReplayAuditRecord(
            replay_id="replay-002",
            audit_result=False,
        ),
    ]

    report = ReplayAuditReport(records)

    assert report.total_audits() == 2


def test_report_lists_replay_ids():

    records = [
        ReplayAuditRecord(
            replay_id="replay-001",
            audit_result=True,
        ),
        ReplayAuditRecord(
            replay_id="replay-002",
            audit_result=False,
        ),
    ]

    report = ReplayAuditReport(records)

    assert report.replay_ids() == [
        "replay-001",
        "replay-002",
    ]


def test_report_serializes():

    records = [
        ReplayAuditRecord(
            replay_id="replay-001",
            audit_result=True,
        )
    ]

    report = ReplayAuditReport(records)

    assert report.to_dict() == {
        "total_audits": 1,
        "replay_ids": [
            "replay-001",
        ],
    }
