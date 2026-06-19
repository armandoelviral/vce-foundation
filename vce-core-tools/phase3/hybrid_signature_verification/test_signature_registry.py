from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_registry import (
    SignatureRegistry,
)


def test_registry_starts_empty():

    registry = SignatureRegistry()

    assert registry.count() == 0


def test_registry_accepts_signature():

    registry = SignatureRegistry()

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    registry.add(
        signature_id="sig-001",
        signature=signature,
    )

    assert registry.count() == 1


def test_registry_returns_signature():

    registry = SignatureRegistry()

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    registry.add(
        signature_id="sig-001",
        signature=signature,
    )

    recovered = registry.get(
        "sig-001"
    )

    assert recovered == signature


def test_missing_signature_returns_none():

    registry = SignatureRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_signature_ids():

    registry = SignatureRegistry()

    registry.add(
        signature_id="sig-001",
        signature=HybridSignatureRecord(
            witness_did="did:vcr:gcp:us-central1:fp001",
            classical_signature="ed25519-sig",
            pqc_signature="mldsa-sig",
        ),
    )

    registry.add(
        signature_id="sig-002",
        signature=HybridSignatureRecord(
            witness_did="did:vcr:aws:us-east-1:fp002",
            classical_signature="ed25519-sig-2",
            pqc_signature="mldsa-sig-2",
        ),
    )

    assert registry.signature_ids() == [
        "sig-001",
        "sig-002",
    ]

