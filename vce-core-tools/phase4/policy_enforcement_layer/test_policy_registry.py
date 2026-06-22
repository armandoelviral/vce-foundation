from phase4.policy_enforcement_layer.policy_registry import (
    PolicyRegistry,
)

from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


def test_contains_policies():

    registry = PolicyRegistry(
        policies=[
            PolicyRecord(
                policy_id="policy-001",
                policy_name="minimum_reputation_100",
                active=False,
            ),
        ]
    )

    assert len(registry.policies) == 1


def test_serializes():

    registry = PolicyRegistry(
        policies=[
            PolicyRecord(
                policy_id="policy-001",
                policy_name="minimum_reputation_100",
                active=False,
            ),
        ]
    )

    data = registry.to_dict()

    assert len(data["policies"]) == 1


def test_contains_policy_id():

    registry = PolicyRegistry(
        policies=[
            PolicyRecord(
                policy_id="policy-001",
                policy_name="minimum_reputation_100",
                active=False,
            ),
        ]
    )

    assert (
        registry.policies[0].policy_id
        == "policy-001"
    )
