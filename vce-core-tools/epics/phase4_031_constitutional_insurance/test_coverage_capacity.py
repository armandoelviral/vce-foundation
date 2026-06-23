from epics.phase4_031_constitutional_insurance.coverage_capacity import (
    calculate_total_coverage,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


def test_total_coverage():
    policies = [
        InsurancePolicy(
            policy_id="policy.001",
            holder_id="institution.alpha",
            coverage_amount=100,
            covered_risk="credit_default",
        ),
        InsurancePolicy(
            policy_id="policy.002",
            holder_id="institution.beta",
            coverage_amount=50,
            covered_risk="credit_default",
        ),
    ]

    assert calculate_total_coverage(policies) == 150


def test_empty_coverage():
    assert calculate_total_coverage([]) == 0


def test_single_policy():
    policies = [
        InsurancePolicy(
            policy_id="policy.001",
            holder_id="institution.alpha",
            coverage_amount=75,
            covered_risk="credit_default",
        )
    ]

    assert calculate_total_coverage(policies) == 75
