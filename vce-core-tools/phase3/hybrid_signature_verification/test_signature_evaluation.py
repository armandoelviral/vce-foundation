from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_evaluation import (
    SignatureEvaluation,
)


def test_valid_signature_passes():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert (
        SignatureEvaluation.evaluate(
            signature
        )
        is True
    )


def test_missing_witness_did_fails():

    signature = HybridSignatureRecord(
        witness_did="",
        classical_signature="ed25519-sig",
        pqc_signature="mldsa-sig",
    )

    assert (
        SignatureEvaluation.evaluate(
            signature
        )
        is False
    )


def test_missing_classical_signature_fails():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="",
        pqc_signature="mldsa-sig",
    )

    assert (
        SignatureEvaluation.evaluate(
            signature
        )
        is False
    )


def test_missing_pqc_signature_fails():

    signature = HybridSignatureRecord(
        witness_did="did:vcr:gcp:us-central1:fp001",
        classical_signature="ed25519-sig",
        pqc_signature="",
    )

    assert (
        SignatureEvaluation.evaluate(
            signature
        )
        is False
    )
