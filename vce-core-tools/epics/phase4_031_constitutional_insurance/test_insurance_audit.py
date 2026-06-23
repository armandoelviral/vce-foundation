from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)
from epics.phase4_031_constitutional_insurance.insurance_audit import (
    audit_insurance_system,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


def test_insurance_audit():
    policies = [
        InsurancePolicy(
            policy_id="policy.001",
            holder_id="institution.alpha",
            coverage_amount=100,
            covered_risk="credit_default",
        )
    ]

    claims = [
        ClaimRecord(
            claim_id="claim.001",
            policy_id="policy.001",
            claim_amount=50,
            reason="credit default",
        )
    ]

    audit = audit_insurance_system(
        policies=policies,
        claims=claims,
    )

    assert audit["policy_count"] == 1
    assert audit["claim_count"] == 1
    assert audit["total_coverage"] == 100
    assert audit["total_claims"] == 50


def test_empty_insurance_audit():
    audit = audit_insurance_system(
        policies=[],
        claims=[],
    )

    assert audit["policy_count"] == 0
    assert audit["claim_count"] == 0
