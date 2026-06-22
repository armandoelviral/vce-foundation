from phase4.policy_enforcement_layer.policy_state import (
    PolicyState,
)


def test_contains_policy_id():

    state = PolicyState(
        policy_id="policy-001",
        policy_state="ACTIVE",
    )

    assert state.policy_id == (
        "policy-001"
    )


def test_contains_state():

    state = PolicyState(
        policy_id="policy-001",
        policy_state="ACTIVE",
    )

    assert state.policy_state == (
        "ACTIVE"
    )


def test_serializes():

    state = PolicyState(
        policy_id="policy-001",
        policy_state="ACTIVE",
    )

    assert state.to_dict() == {
        "policy_id":
            "policy-001",
        "policy_state":
            "ACTIVE",
    }
