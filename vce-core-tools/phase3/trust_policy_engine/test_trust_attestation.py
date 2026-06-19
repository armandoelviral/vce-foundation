from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)

from phase3.trust_policy_engine.trust_attestation import (
    TrustAttestation,
)


def test_attestation_subject():

    decision = TrustDecision(
        status="TRUSTED",
    )

    attestation = (
        TrustAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "trust_decision"
    )


def test_attestation_uses_status():

    decision = TrustDecision(
        status="TRUSTED",
    )

    attestation = (
        TrustAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.evidence_hash
        == "TRUSTED"
    )


def test_attestation_preserves_id():

    decision = TrustDecision(
        status="TRUSTED",
    )

    attestation = (
        TrustAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
