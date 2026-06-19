from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)

from phase3.policy_versioning.policy_version_report import (
    PolicyVersionReport,
)


def test_report_contains_version_count():

    report = PolicyVersionReport(
        {
            "trust-policy:v1":
                PolicyVersionRecord(
                    policy_id="trust-policy",
                    version="v1",
                    approved_by="auth-001",
                )
        }
    )

    assert report.version_count() == 1


def test_report_lists_version_ids():

    report = PolicyVersionReport(
        {
            "trust-policy:v1":
                PolicyVersionRecord(
                    policy_id="trust-policy",
                    version="v1",
                    approved_by="auth-001",
                ),

            "trust-policy:v2":
                PolicyVersionRecord(
                    policy_id="trust-policy",
                    version="v2",
                    approved_by="auth-001",
                ),
        }
    )

    assert report.version_ids() == [
        "trust-policy:v1",
        "trust-policy:v2",
    ]


def test_report_serializes():

    report = PolicyVersionReport(
        {
            "trust-policy:v1":
                PolicyVersionRecord(
                    policy_id="trust-policy",
                    version="v1",
                    approved_by="auth-001",
                )
        }
    )

    assert report.to_dict() == {
        "version_count": 1,
        "version_ids": [
            "trust-policy:v1",
        ],
    }
