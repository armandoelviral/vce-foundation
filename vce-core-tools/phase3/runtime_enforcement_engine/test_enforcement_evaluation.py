from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)

from phase3.runtime_enforcement_engine.enforcement_evaluation import (
    EnforcementEvaluation,
)

from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)


def test_allow_admission_executes():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    decision = AdmissionDecision(
        status="ALLOW",
    )

    result = EnforcementEvaluation.evaluate(
        policy=policy,
        admission_decision=decision,
    )

    assert result == "EXECUTE"


def test_deny_admission_blocks():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    decision = AdmissionDecision(
        status="DENY",
    )

    result = EnforcementEvaluation.evaluate(
        policy=policy,
        admission_decision=decision,
    )

    assert result == "BLOCK"


def test_unknown_status_defaults_to_block():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    decision = AdmissionDecision(
        status="UNKNOWN",
    )

    result = EnforcementEvaluation.evaluate(
        policy=policy,
        admission_decision=decision,
    )

    assert result == "BLOCK"
