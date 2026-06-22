from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


def test_contains_policy_id():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    assert (
        policy.policy_id
        == "policy-001"
    )


def test_contains_policy_name():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    assert (
        policy.policy_name
        == "minimum_reputation_100"
    )


def test_contains_active_flag():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    assert policy.active is False


def test_serializes():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    assert policy.to_dict() == {
        "policy_id":
            "policy-001",
        "policy_name":
            "minimum_reputation_100",
        "active":
            False,
    }
