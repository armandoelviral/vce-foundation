from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_report import (
    PolicyReport,
)


def test_report_contains_total_policies():

    records = [
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="rule-v1",
        ),
        PolicyRecord(
            policy_id="policy-002",
            version=1,
            rule="rule-v2",
        ),
    ]

    report = PolicyReport(records)

    assert report.total_policies() == 2


def test_report_lists_policy_ids():

    records = [
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="rule-v1",
        ),
        PolicyRecord(
            policy_id="policy-002",
            version=1,
            rule="rule-v2",
        ),
    ]

    report = PolicyReport(records)

    assert report.policy_ids() == [
        "policy-001",
        "policy-002",
    ]


def test_report_serializes():

    records = [
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="rule-v1",
        )
    ]

    report = PolicyReport(records)

    assert report.to_dict() == {
        "total_policies": 1,
        "policy_ids": [
            "policy-001",
        ],
    }
