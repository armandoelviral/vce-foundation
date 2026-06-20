from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)


def test_contains_policy_id():

    record = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert record.policy_id == "policy-001"


def test_contains_resource_type():

    record = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert record.resource_type == "REPLAY"


def test_contains_action():

    record = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert record.action == "EXECUTE"


def test_contains_effect():

    record = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert record.effect == "ALLOW"


def test_serializes():

    record = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert record.to_dict() == {
        "policy_id": "policy-001",
        "resource_type": "REPLAY",
        "action": "EXECUTE",
        "effect": "ALLOW",
    }
