from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)

from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)

from phase3.runtime_enforcement_engine.enforcement_evaluation import (
    EnforcementEvaluation,
)

from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)

from phase3.runtime_enforcement_engine.enforcement_query import (
    EnforcementQuery,
)

from phase3.runtime_enforcement_engine.enforcement_report import (
    EnforcementReport,
)

from phase3.runtime_enforcement_engine.enforcement_attestation import (
    EnforcementAttestation,
)


def test_end_to_end_runtime_enforcement_engine():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    admission_decision = AdmissionDecision(
        status="ALLOW",
    )

    evaluation = EnforcementEvaluation.evaluate(
        policy=policy,
        admission_decision=admission_decision,
    )

    assert evaluation == "EXECUTE"

    decision = EnforcementDecision.from_evaluation(
        evaluation
    )

    assert decision.status == "EXECUTE"

    decisions = {
        "decision-001": decision
    }

    query = EnforcementQuery(
        decisions
    )

    recovered = query.by_id(
        "decision-001"
    )

    assert recovered == decision

    report = EnforcementReport(
        decisions
    )

    assert report.decision_count() == 1
    assert report.decision_ids() == [
        "decision-001",
    ]

    attestation = EnforcementAttestation.attest(
        attestation_id="att-001",
        decision=decision,
    )

    assert attestation.subject == "enforcement_decision"
    assert attestation.evidence_hash == "EXECUTE"
