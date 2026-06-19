from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_attestation import (
    RecoveryAttestation,
)


def test_attestation_subject():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    attestation = (
        RecoveryAttestation.attest(
            attestation_id="att-001",
            recovery=record,
        )
    )

    assert (
        attestation.subject
        == "governance_recovery"
    )


def test_attestation_uses_recovery_id():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    attestation = (
        RecoveryAttestation.attest(
            attestation_id="att-001",
            recovery=record,
        )
    )

    assert (
        attestation.evidence_hash
        == "rec-001"
    )


def test_attestation_preserves_id():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    attestation = (
        RecoveryAttestation.attest(
            attestation_id="att-001",
            recovery=record,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
