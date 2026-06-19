from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)

from phase3.governance_escalation.escalation_attestation import (
    EscalationAttestation,
)


def test_attestation_subject():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    attestation = (
        EscalationAttestation.attest(
            attestation_id="att-001",
            escalation=record,
        )
    )

    assert (
        attestation.subject
        == "governance_escalation"
    )


def test_attestation_uses_escalation_id():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    attestation = (
        EscalationAttestation.attest(
            attestation_id="att-001",
            escalation=record,
        )
    )

    assert (
        attestation.evidence_hash
        == "esc-001"
    )


def test_attestation_preserves_id():

    record = EscalationRecord(
        escalation_id="esc-001",
        reason="quorum_failure",
        severity="HIGH",
    )

    attestation = (
        EscalationAttestation.attest(
            attestation_id="att-001",
            escalation=record,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
