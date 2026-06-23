from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)
from epics.phase4_031_constitutional_insurance.insurance_registry import (
    InsuranceRegistry,
)
from epics.phase4_031_constitutional_insurance.insurance_state import (
    InsuranceState,
)
from epics.phase4_031_constitutional_insurance.insurance_verifier import (
    verify_insurance_state,
)


def test_end_to_end_insurance_flow():
    registry = InsuranceRegistry()

    registry.add(
        InsurancePolicy(
            policy_id="policy.001",
            holder_id="institution.alpha",
            coverage_amount=100,
            covered_risk="credit_default",
        )
    )

    claim = ClaimRecord(
        claim_id="claim.001",
        policy_id="policy.001",
        claim_amount=40,
        reason="credit default realized",
    )

    state = InsuranceState.from_records(
        policies=registry.policies(),
        claims=[claim],
    )

    assert state.total_coverage == 100
    assert state.total_claims == 40
    assert state.remaining_coverage == 60

    verification = verify_insurance_state(state)

    assert verification["verified"] is True
