from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)

from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)

from phase3.runtime_governance.governance_evaluation import (
    GovernanceEvaluation,
)

from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)

from phase3.runtime_governance.governance_query import (
    GovernanceQuery,
)

from phase3.runtime_governance.governance_report import (
    GovernanceReport,
)

from phase3.runtime_governance.governance_attestation import (
    GovernanceAttestation,
)


def test_end_to_end_runtime_governance():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    enforcement_decision = (
        EnforcementDecision(
            status="EXECUTE"
        )
    )

    evaluation = (
        GovernanceEvaluation.evaluate(
            policy=policy,
            enforcement_decision=enforcement_decision,
        )
    )

    assert evaluation is True

    decision = (
        GovernanceDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "APPROVED"
    )

    decisions = {
        "decision-001": decision
    }

    query = GovernanceQuery(
        decisions
    )

    recovered = query.by_id(
        "decision-001"
    )

    assert recovered == decision

    report = GovernanceReport(
        decisions
    )

    assert (
        report.decision_count()
        == 1
    )

    assert (
        report.decision_ids()
        == ["decision-001"]
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "governance_decision"
    )

    assert (
        attestation.evidence_hash
        == "APPROVED"
    )
