from phase4.policy_enforcement_layer.policy_enforcement import (
    PolicyEnforcement,
)

from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


def test_enforces_active_policy():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=True,
    )

    assert (
        PolicyEnforcement.enforce(
            policy
        )
        is True
    )


def test_does_not_enforce_inactive_policy():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    assert (
        PolicyEnforcement.enforce(
            policy
        )
        is False
    )


def test_returns_boolean():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=True,
    )

    result = (
        PolicyEnforcement.enforce(
            policy
        )
    )

    assert isinstance(
        result,
        bool,
    )
