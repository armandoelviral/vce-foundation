from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)

from phase3.multi_party_governance.governance_report import (
    GovernanceReport,
)


def test_report_contains_resolution_count():

    report = GovernanceReport(
        {
            "resolution-001": GovernanceResolution(
                status="RESOLVED"
            )
        }
    )

    assert report.resolution_count() == 1


def test_report_lists_resolution_ids():

    report = GovernanceReport(
        {
            "resolution-001": GovernanceResolution(
                status="RESOLVED"
            ),
            "resolution-002": GovernanceResolution(
                status="UNRESOLVED"
            ),
        }
    )

    assert report.resolution_ids() == [
        "resolution-001",
        "resolution-002",
    ]


def test_report_serializes():

    report = GovernanceReport(
        {
            "resolution-001": GovernanceResolution(
                status="RESOLVED"
            )
        }
    )

    assert report.to_dict() == {
        "resolution_count": 1,
        "resolution_ids": [
            "resolution-001",
        ],
    }
