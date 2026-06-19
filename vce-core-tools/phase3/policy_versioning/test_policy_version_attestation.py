from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)

from phase3.policy_versioning.policy_version_attestation import (
    PolicyVersionAttestation,
)


def test_attestation_subject():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    attestation = (
        PolicyVersionAttestation.attest(
            attestation_id="att-001",
            policy_version=record,
        )
    )

    assert (
        attestation.subject
        == "policy_version"
    )


def test_attestation_uses_version_identifier():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    attestation = (
        PolicyVersionAttestation.attest(
            attestation_id="att-001",
            policy_version=record,
        )
    )

    assert (
        attestation.evidence_hash
        == "trust-policy:v1"
    )


def test_attestation_preserves_id():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    attestation = (
        PolicyVersionAttestation.attest(
            attestation_id="att-001",
            policy_version=record,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
