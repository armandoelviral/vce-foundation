from phase2.runtime_state_recovery.recovery_report import (
    RecoveryReport,
)

from phase2.attestation_persistence.recovery_attestation import (
    RecoveryAttestation,
)


def test_attests_recovery_report():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    record = RecoveryAttestation.attest(
        attestation_id="att-001",
        report=report,
    )

    assert record.subject == "recovery"


def test_recovery_attestation_uses_recovery_id():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    record = RecoveryAttestation.attest(
        attestation_id="att-001",
        report=report,
    )

    assert record.evidence_hash == "recovery-001"


def test_recovery_attestation_preserves_id():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    record = RecoveryAttestation.attest(
        attestation_id="att-001",
        report=report,
    )

    assert record.attestation_id == "att-001"
