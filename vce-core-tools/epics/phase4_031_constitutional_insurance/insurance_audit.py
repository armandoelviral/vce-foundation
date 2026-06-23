from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


def audit_insurance_system(
    policies: list[InsurancePolicy],
    claims: list[ClaimRecord],
):
    return {
        "policy_count": len(policies),
        "claim_count": len(claims),
        "total_coverage": sum(
            policy.coverage_amount
            for policy in policies
        ),
        "total_claims": sum(
            claim.claim_amount
            for claim in claims
        ),
    }
