from epics.ztc7_quantum_resilient_evidence.hybrid_signature_envelope import (
    HybridSignatureEnvelope,
)


def test_envelope_contains_dual_signatures():

    envelope = HybridSignatureEnvelope(
        evidence_hash="evidence-001",
        classical_signature="ed25519-signature",
        pqc_signature="ml-dsa-signature",
        policy_mode="strict_now",
    )

    assert envelope.evidence_hash == "evidence-001"
    assert envelope.classical_signature == "ed25519-signature"
    assert envelope.pqc_signature == "ml-dsa-signature"
    assert envelope.policy_mode == "strict_now"


def test_envelope_serializes():

    envelope = HybridSignatureEnvelope(
        evidence_hash="evidence-001",
        classical_signature="ed25519-signature",
        pqc_signature="ml-dsa-signature",
        policy_mode="strict_now",
    )

    assert envelope.to_dict() == {
        "evidence_hash": "evidence-001",
        "classical_signature": "ed25519-signature",
        "pqc_signature": "ml-dsa-signature",
        "policy_mode": "strict_now",
    }
