from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_registry import (
    RecoveryRegistry,
)

from phase3.governance_recovery.recovery_evaluation import (
    RecoveryEvaluation,
)

from phase3.governance_recovery.reinstatement_decision import (
    ReinstatementDecision,
)

from phase3.governance_recovery.recovery_query import (
    RecoveryQuery,
)

from phase3.governance_recovery.recovery_report import (
    RecoveryReport,
)

from phase3.governance_recovery.recovery_attestation import (
    RecoveryAttestation,
)


def test_end_to_end_recovery_flow():

    registry = RecoveryRegistry()

    recovery = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    registry.add(
        recovery
    )

    evaluation = (
        RecoveryEvaluation.evaluate(
            recovery
        )
    )

    assert evaluation is True

    decision = (
        ReinstatementDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "REINSTATE"
    )

    query = RecoveryQuery(
        registry
    )

    recovered = query.by_id(
        "rec-001"
    )

    assert recovered == recovery

    report = RecoveryReport(
        {
            "rec-001": recovered
        }
    )

    assert (
        report.recovery_count()
        == 1
    )

    assert (
        report.recovery_ids()
        == ["rec-001"]
    )

    attestation = (
        RecoveryAttestation.attest(
            attestation_id="att-001",
            recovery=recovery,
        )
    )

    assert (
        attestation.subject
        == "governance_recovery"
    )

    assert (
        attestation.evidence_hash
        == "rec-001"
    )

