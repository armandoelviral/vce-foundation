from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)


def test_contains_witness_did():

    record = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert (
        record.witness_did
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_contains_classical_signature():

    record = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert (
        record.classical_signature
        == "ed25519-sig"
    )


def test_contains_pqc_signature():

    record = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert (
        record.pqc_signature
        == "mldsa-sig"
    )


def test_serializes():

    record = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert record.to_dict() == {
        "witness_did":
            "did:vcr:gcp:us-central1:fp001",

        "classical_signature":
            "ed25519-sig",

        "pqc_signature":
            "mldsa-sig",
    }
