from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)

from phase3.trust_policy_engine.trust_evaluation import (
    TrustEvaluation,
)

from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)

from phase3.trust_policy_engine.trust_query import (
    TrustQuery,
)

from phase3.trust_policy_engine.trust_report import (
    TrustReport,
)

from phase3.trust_policy_engine.trust_attestation import (
    TrustAttestation,
)


def test_end_to_end_trust_policy_engine():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    evaluation = (
        TrustEvaluation.evaluate(
            policy=policy,
            certificate_exists=True,
            certificate_published=True,
            certificate_revoked=False,
        )
    )

    assert evaluation is True

    decision = (
        TrustDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "TRUSTED"
    )

    decisions = {
        "decision-001": decision
    }

    query = TrustQuery(
        decisions
    )

    recovered = query.by_id(
        "decision-001"
    )

    assert recovered == decision

    report = TrustReport(
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
        TrustAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "trust_decision"
    )

    assert (
        attestation.evidence_hash
        == "TRUSTED"
    )
