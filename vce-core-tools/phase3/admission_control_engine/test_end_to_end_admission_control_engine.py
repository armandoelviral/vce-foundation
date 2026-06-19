from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)

from phase3.admission_control_engine.admission_evaluation import (
    AdmissionEvaluation,
)

from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)

from phase3.admission_control_engine.admission_query import (
    AdmissionQuery,
)

from phase3.admission_control_engine.admission_report import (
    AdmissionReport,
)

from phase3.admission_control_engine.admission_attestation import (
    AdmissionAttestation,
)

from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)


def test_end_to_end_admission_control_engine():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    trust_decision = TrustDecision(
        status="TRUSTED",
    )

    evaluation = (
        AdmissionEvaluation.evaluate(
            policy=policy,
            trust_decision=trust_decision,
        )
    )

    assert evaluation is True

    decision = (
        AdmissionDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "ALLOW"
    )

    decisions = {
        "decision-001": decision
    }

    query = AdmissionQuery(
        decisions
    )

    recovered = query.by_id(
        "decision-001"
    )

    assert recovered == decision

    report = AdmissionReport(
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
        AdmissionAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "admission_decision"
    )

    assert (
        attestation.evidence_hash
        == "ALLOW"
    )
