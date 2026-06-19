from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.escalation_registry import (
    EscalationRegistry,
)

from phase3.governance_escalation.suspension_evaluation import (
    SuspensionEvaluation,
)

from phase3.governance_escalation.suspension_decision import (
    SuspensionDecision,
)

from phase3.governance_escalation.escalation_query import (
    EscalationQuery,
)

from phase3.governance_escalation.escalation_report import (
    EscalationReport,
)

from phase3.governance_escalation.escalation_attestation import (
    EscalationAttestation,
)


def test_end_to_end_escalation_flow():

    registry = EscalationRegistry()

    escalation = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    registry.add(escalation)

    evaluation = SuspensionEvaluation.evaluate(
        escalation
    )

    assert evaluation is True

    decision = SuspensionDecision.from_evaluation(
        evaluation
    )

    assert decision.status == "SUSPEND"

    query = EscalationQuery(
        registry
    )

    recovered = query.by_id(
        "esc-001"
    )

    assert recovered == escalation

    report = EscalationReport(
        {
            "esc-001": recovered
        }
    )

    assert report.escalation_count() == 1
    assert report.escalation_ids() == [
        "esc-001",
    ]

    attestation = EscalationAttestation.attest(
        attestation_id="att-001",
        escalation=escalation,
    )

    assert attestation.subject == "governance_escalation"
    assert attestation.evidence_hash == "esc-001"
