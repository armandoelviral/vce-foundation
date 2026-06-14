from epics.ztc7_quantum_resilient_evidence.classical_signature_layer import (
    ClassicalSignatureLayer,
)


def test_classical_signature_is_deterministic():

    sig_1 = ClassicalSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="classical-key",
    )

    sig_2 = ClassicalSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="classical-key",
    )

    assert sig_1 == sig_2


def test_classical_signature_changes_when_evidence_changes():

    sig_1 = ClassicalSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="classical-key",
    )

    sig_2 = ClassicalSignatureLayer.sign(
        evidence_hash="evidence-002",
        key="classical-key",
    )

    assert sig_1 != sig_2
