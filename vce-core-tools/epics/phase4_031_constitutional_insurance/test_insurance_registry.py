from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)
from epics.phase4_031_constitutional_insurance.insurance_registry import (
    InsuranceRegistry,
)


def test_registry_stores_policy():
    registry = InsuranceRegistry()

    policy = InsurancePolicy(
        policy_id="policy.001",
        holder_id="institution.alpha",
        coverage_amount=100,
        covered_risk="credit_default",
    )

    registry.add(policy)

    assert registry.policies() == [policy]


def test_registry_rejects_duplicate_policy():
    registry = InsuranceRegistry()

    policy = InsurancePolicy(
        policy_id="policy.001",
        holder_id="institution.alpha",
        coverage_amount=100,
        covered_risk="credit_default",
    )

    registry.add(policy)

    try:
        registry.add(policy)
        assert False
    except ValueError as exc:
        assert "duplicate policy" in str(exc)


def test_registry_returns_copy():
    registry = InsuranceRegistry()

    policy = InsurancePolicy(
        policy_id="policy.001",
        holder_id="institution.alpha",
        coverage_amount=100,
        covered_risk="credit_default",
    )

    registry.add(policy)

    policies = registry.policies()
    policies.clear()

    assert len(registry.policies()) == 1
