from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)

from phase3.admission_control_engine.admission_evaluation import (
    AdmissionEvaluation,
)

from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)


def test_trusted_decision_allows_admission():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    decision = TrustDecision(
        status="TRUSTED",
    )

    result = AdmissionEvaluation.evaluate(
        policy=policy,
        trust_decision=decision,
    )

    assert result is True


def test_untrusted_decision_denies_admission():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    decision = TrustDecision(
        status="UNTRUSTED",
    )

    result = AdmissionEvaluation.evaluate(
        policy=policy,
        trust_decision=decision,
    )

    assert result is False


def test_unknown_decision_denies_admission():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    decision = TrustDecision(
        status="UNKNOWN",
    )

    result = AdmissionEvaluation.evaluate(
        policy=policy,
        trust_decision=decision,
    )

    assert result is False
