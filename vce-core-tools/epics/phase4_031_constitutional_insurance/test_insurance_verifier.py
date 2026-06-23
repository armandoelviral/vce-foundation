from epics.phase4_031_constitutional_insurance.insurance_state import (
    InsuranceState,
)
from epics.phase4_031_constitutional_insurance.insurance_verifier import (
    verify_insurance_state,
)


def test_insurance_verification_succeeds():
    state = InsuranceState(
        total_coverage=100,
        total_claims=40,
        remaining_coverage=60,
    )

    result = verify_insurance_state(state)

    assert result["verified"] is True
    assert result["remaining_coverage"] == 60


def test_insurance_verification_fails_when_claims_exceed_coverage():
    state = InsuranceState(
        total_coverage=100,
        total_claims=120,
        remaining_coverage=-20,
    )

    result = verify_insurance_state(state)

    assert result["verified"] is False
    assert result["remaining_coverage"] == -20


def test_reports_coverage_and_claims():
    state = InsuranceState(
        total_coverage=80,
        total_claims=30,
        remaining_coverage=50,
    )

    result = verify_insurance_state(state)

    assert result["total_coverage"] == 80
    assert result["total_claims"] == 30
