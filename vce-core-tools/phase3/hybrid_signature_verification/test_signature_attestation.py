from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_attestation import (
    SignatureAttestation,
)


def test_attestation_subject():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    attestation = SignatureAttestation.attest(
        attestation_id="att-001",
        signature=signature,
    )

    assert (
        attestation.subject
        == "hybrid_signature"
    )


def test_attestation_uses_witness_did():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    attestation = SignatureAttestation.attest(
        attestation_id="att-001",
        signature=signature,
    )

    assert (
        attestation.evidence_hash
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_attestation_preserves_id():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    attestation = SignatureAttestation.attest(
        attestation_id="att-001",
        signature=signature,
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
