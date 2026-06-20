from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_report import (
    PolicyActivationReport,
)


def test_report_contains_activation_count():

    report = PolicyActivationReport(
        {
            "activation-001":
                PolicyActivationRecord(
                    activation_id="activation-001",
                    policy_id="policy-001",
                    status="ACTIVE",
                )
        }
    )

    assert report.activation_count() == 1


def test_report_lists_activation_ids():

    report = PolicyActivationReport(
        {
            "activation-001":
                PolicyActivationRecord(
                    activation_id="activation-001",
                    policy_id="policy-001",
                    status="ACTIVE",
                ),

            "activation-002":
                PolicyActivationRecord(
                    activation_id="activation-002",
                    policy_id="policy-002",
                    status="INACTIVE",
                ),
        }
    )

    assert report.activation_ids() == [
        "activation-001",
        "activation-002",
    ]


def test_report_serializes():

    report = PolicyActivationReport(
        {
            "activation-001":
                PolicyActivationRecord(
                    activation_id="activation-001",
                    policy_id="policy-001",
                    status="ACTIVE",
                )
        }
    )

    assert report.to_dict() == {
        "activation_count": 1,
        "activation_ids": [
            "activation-001",
        ],
    }
