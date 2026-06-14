from epics.ztc7_quantum_resilient_evidence.hybrid_signature_envelope import (
    HybridSignatureEnvelope,
)

from epics.ztc7_quantum_resilient_evidence.dual_verification_policy import (
    DualVerificationPolicy,
)


def test_quantum_resilient_attestation_strict_mode():

    envelope = HybridSignatureEnvelope(
        evidence_hash="evidence-001",
        classical_signature="ed25519-signature",
        pqc_signature="ml-dsa-signature",
        policy_mode="strict_now",
    )

    trusted = DualVerificationPolicy.verify(
        classical_valid=bool(envelope.classical_signature),
        pqc_valid=bool(envelope.pqc_signature),
        mode=envelope.policy_mode,
    )

    assert trusted is True
