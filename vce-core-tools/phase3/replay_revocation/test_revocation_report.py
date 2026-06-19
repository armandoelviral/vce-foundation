from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)

from phase3.replay_revocation.revocation_report import (
    RevocationReport,
)


def test_report_contains_revocation_count():

    registry = RevocationRegistry()

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-001",
            certificate_id="cert-001",
            reason="key_compromise",
        )
    )

    report = RevocationReport(
        registry
    )

    assert report.revocation_count() == 1


def test_report_lists_revocation_ids():

    registry = RevocationRegistry()

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-001",
            certificate_id="cert-001",
            reason="key_compromise",
        )
    )

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-002",
            certificate_id="cert-002",
            reason="policy_violation",
        )
    )

    report = RevocationReport(
        registry
    )

    assert report.revocation_ids() == [
        "rev-001",
        "rev-002",
    ]


def test_report_serializes():

    registry = RevocationRegistry()

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-001",
            certificate_id="cert-001",
            reason="key_compromise",
        )
    )

    report = RevocationReport(
        registry
    )

    assert report.to_dict() == {
        "revocation_count": 1,
        "revocation_ids": [
            "rev-001",
        ],
    }
