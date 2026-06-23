from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)
from epics.phase4_031_constitutional_insurance.insurance_state import (
    InsuranceState,
)


def test_builds_insurance_state():
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
            claim_amount=40,
            reason="credit default",
        )
    ]

    state = InsuranceState.from_records(
        policies=policies,
        claims=claims,
    )

    assert state.total_coverage == 100
    assert state.total_claims == 40
    assert state.remaining_coverage == 60


def test_empty_insurance_state():
    state = InsuranceState.from_records(
        policies=[],
        claims=[],
    )

    assert state.remaining_coverage == 0
