from epics.ztc7_quantum_resilient_evidence.pqc_signature_layer import (
    PQCSignatureLayer,
)


def test_pqc_signature_is_deterministic():

    sig_1 = PQCSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="pqc-key",
    )

    sig_2 = PQCSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="pqc-key",
    )

    assert sig_1 == sig_2


def test_pqc_signature_changes_when_evidence_changes():

    sig_1 = PQCSignatureLayer.sign(
        evidence_hash="evidence-001",
        key="pqc-key",
    )

    sig_2 = PQCSignatureLayer.sign(
        evidence_hash="evidence-002",
        key="pqc-key",
    )

    assert sig_1 != sig_2
