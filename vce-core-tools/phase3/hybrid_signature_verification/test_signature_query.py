from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_registry import (
    SignatureRegistry,
)

from phase3.hybrid_signature_verification.signature_query import (
    SignatureQuery,
)


def test_query_returns_signature():

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

    query = SignatureQuery(
        registry
    )

    result = query.by_id(
        "sig-001"
    )

    assert result == signature


def test_query_returns_none_for_missing():

    registry = SignatureRegistry()

    query = SignatureQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_witness_did():

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

    query = SignatureQuery(
        registry
    )

    result = query.by_id(
        "sig-001"
    )

    assert (
        result.witness_did
        == "did:vcr:gcp:us-central1:fp001"
    )
