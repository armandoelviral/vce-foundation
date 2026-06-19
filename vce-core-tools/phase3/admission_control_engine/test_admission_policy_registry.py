from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)

from phase3.admission_control_engine.admission_policy_registry import (
    AdmissionPolicyRegistry,
)


def test_registry_starts_empty():

    registry = AdmissionPolicyRegistry()

    assert registry.count() == 0


def test_registry_accepts_policy():

    registry = AdmissionPolicyRegistry()

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    registry.add(policy)

    assert registry.count() == 1


def test_registry_returns_policy():

    registry = AdmissionPolicyRegistry()

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    registry.add(policy)

    recovered = registry.get(
        "policy-001"
    )

    assert recovered == policy


def test_missing_policy_returns_none():

    registry = AdmissionPolicyRegistry()

    assert registry.get(
        "missing"
    ) is None
