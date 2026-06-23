from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


def test_policy_creation():
    policy = InsurancePolicy(
        policy_id="policy.001",
        holder_id="institution.alpha",
        coverage_amount=100,
        covered_risk="credit_default",
    )

    assert policy.policy_id == "policy.001"
    assert policy.holder_id == "institution.alpha"
    assert policy.coverage_amount == 100
    assert policy.covered_risk == "credit_default"


def test_rejects_empty_policy_id():
    try:
        InsurancePolicy(
            policy_id="",
            holder_id="institution.alpha",
            coverage_amount=100,
            covered_risk="credit_default",
        )
        assert False
    except ValueError as exc:
        assert "policy_id" in str(exc)


def test_rejects_non_positive_coverage():
    try:
        InsurancePolicy(
            policy_id="policy.001",
            holder_id="institution.alpha",
            coverage_amount=0,
            covered_risk="credit_default",
        )
        assert False
    except ValueError as exc:
        assert "coverage_amount" in str(exc)
