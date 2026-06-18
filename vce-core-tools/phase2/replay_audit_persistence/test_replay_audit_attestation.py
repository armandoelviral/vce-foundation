from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)

from phase2.replay_audit_persistence.replay_audit_attestation import (
    ReplayAuditAttestation,
)


def test_attestation_subject():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    attestation = ReplayAuditAttestation.attest(
        attestation_id="att-001",
        replay_audit=record,
    )

    assert attestation.subject == "replay_audit"


def test_attestation_uses_replay_id():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    attestation = ReplayAuditAttestation.attest(
        attestation_id="att-001",
        replay_audit=record,
    )

    assert (
        attestation.evidence_hash
        == "replay-001"
    )


def test_attestation_preserves_id():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    attestation = ReplayAuditAttestation.attest(
        attestation_id="att-001",
        replay_audit=record,
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
