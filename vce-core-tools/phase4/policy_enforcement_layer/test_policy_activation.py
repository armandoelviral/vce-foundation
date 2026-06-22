from phase4.policy_enforcement_layer.policy_activation import (
    PolicyActivation,
)

from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


def test_activates_policy():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    activated = PolicyActivation.activate(policy)

    assert activated.active is True


def test_preserves_policy_id():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    activated = PolicyActivation.activate(policy)

    assert activated.policy_id == "policy-001"


def test_preserves_policy_name():

    policy = PolicyRecord(
        policy_id="policy-001",
        policy_name="minimum_reputation_100",
        active=False,
    )

    activated = PolicyActivation.activate(policy)

    assert activated.policy_name == "minimum_reputation_100"
