from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)


def test_contains_activation_id():

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    assert record.activation_id == "activation-001"


def test_contains_policy_id():

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    assert record.policy_id == "policy-001"


def test_contains_status():

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    assert record.status == "ACTIVE"


def test_serializes():

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    assert record.to_dict() == {
        "activation_id": "activation-001",
        "policy_id": "policy-001",
        "status": "ACTIVE",
    }
