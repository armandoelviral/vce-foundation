from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_report import (
    RuntimePolicyReport,
)


def test_report_contains_policy_count():

    report = RuntimePolicyReport(
        {
            "policy-001":
                RuntimePolicyRecord(
                    policy_id="policy-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    effect="ALLOW",
                )
        }
    )

    assert report.policy_count() == 1


def test_report_lists_policy_ids():

    report = RuntimePolicyReport(
        {
            "policy-001":
                RuntimePolicyRecord(
                    policy_id="policy-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    effect="ALLOW",
                ),

            "policy-002":
                RuntimePolicyRecord(
                    policy_id="policy-002",
                    resource_type="WITNESS",
                    action="PARTICIPATE",
                    effect="DENY",
                ),
        }
    )

    assert report.policy_ids() == [
        "policy-001",
        "policy-002",
    ]


def test_report_serializes():

    report = RuntimePolicyReport(
        {
            "policy-001":
                RuntimePolicyRecord(
                    policy_id="policy-001",
                    resource_type="REPLAY",
                    action="EXECUTE",
                    effect="ALLOW",
                )
        }
    )

    assert report.to_dict() == {
        "policy_count": 1,
        "policy_ids": [
            "policy-001",
        ],
    }
