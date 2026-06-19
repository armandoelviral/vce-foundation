from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.authority_report import (
    AuthorityReport,
)


def test_report_contains_authority_count():

    report = AuthorityReport(
        {
            "auth-001": AuthorityRecord(
                authority_id="auth-001",
                principal_id="principal-001",
                role="GOVERNOR",
            )
        }
    )

    assert report.authority_count() == 1


def test_report_lists_authority_ids():

    report = AuthorityReport(
        {
            "auth-001": AuthorityRecord(
                authority_id="auth-001",
                principal_id="principal-001",
                role="GOVERNOR",
            ),
            "auth-002": AuthorityRecord(
                authority_id="auth-002",
                principal_id="principal-002",
                role="AUDITOR",
            ),
        }
    )

    assert report.authority_ids() == [
        "auth-001",
        "auth-002",
    ]


def test_report_serializes():

    report = AuthorityReport(
        {
            "auth-001": AuthorityRecord(
                authority_id="auth-001",
                principal_id="principal-001",
                role="GOVERNOR",
            )
        }
    )

    assert report.to_dict() == {
        "authority_count": 1,
        "authority_ids": [
            "auth-001",
        ],
    }
