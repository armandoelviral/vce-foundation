from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)

from phase3.hybrid_signature_verification.signature_registry import (
    SignatureRegistry,
)

from phase3.hybrid_signature_verification.signature_evaluation import (
    SignatureEvaluation,
)

from phase3.hybrid_signature_verification.signature_decision import (
    SignatureDecision,
)

from phase3.hybrid_signature_verification.signature_query import (
    SignatureQuery,
)

from phase3.hybrid_signature_verification.signature_report import (
    SignatureReport,
)

from phase3.hybrid_signature_verification.signature_attestation import (
    SignatureAttestation,
)


def test_end_to_end_hybrid_signature():

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

    evaluation = SignatureEvaluation.evaluate(
        signature
    )

    assert evaluation is True

    decision = SignatureDecision.from_evaluation(
        evaluation
    )

    assert (
        decision.status
        == "ACCEPT_SIGNATURE"
    )

    query = SignatureQuery(
        registry
    )

    recovered = query.by_id(
        "sig-001"
    )

    assert recovered == signature

    report = SignatureReport(
        {
            "sig-001": recovered
        }
    )

    assert report.signature_count() == 1

    assert report.signature_ids() == [
        "sig-001"
    ]

    attestation = (
        SignatureAttestation.attest(
            attestation_id="att-001",
            signature=signature,
        )
    )

    assert (
        attestation.subject
        == "hybrid_signature"
    )

    assert (
        attestation.evidence_hash
        == "did:vcr:gcp:us-central1:fp001"
    )
