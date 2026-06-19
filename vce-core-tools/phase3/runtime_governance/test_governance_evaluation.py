from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)

from phase3.runtime_governance.governance_evaluation import (
    GovernanceEvaluation,
)

from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)


def test_execute_decision_is_approved():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    decision = EnforcementDecision(
        status="EXECUTE",
    )

    result = GovernanceEvaluation.evaluate(
        policy=policy,
        enforcement_decision=decision,
    )

    assert result is True


def test_block_decision_is_rejected():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    decision = EnforcementDecision(
        status="BLOCK",
    )

    result = GovernanceEvaluation.evaluate(
        policy=policy,
        enforcement_decision=decision,
    )

    assert result is False


def test_unknown_decision_is_rejected():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    decision = EnforcementDecision(
        status="UNKNOWN",
    )

    result = GovernanceEvaluation.evaluate(
        policy=policy,
        enforcement_decision=decision,
    )

    assert result is False
