from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)

from phase3.admission_control_engine.admission_attestation import (
    AdmissionAttestation,
)


def test_attestation_subject():

    decision = AdmissionDecision(
        status="ALLOW",
    )

    attestation = (
        AdmissionAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "admission_decision"
    )


def test_attestation_uses_status():

    decision = AdmissionDecision(
        status="ALLOW",
    )

    attestation = (
        AdmissionAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.evidence_hash
        == "ALLOW"
    )


def test_attestation_preserves_id():

    decision = AdmissionDecision(
        status="ALLOW",
    )

    attestation = (
        AdmissionAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
