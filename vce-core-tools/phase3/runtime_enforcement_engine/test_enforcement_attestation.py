from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)

from phase3.runtime_enforcement_engine.enforcement_attestation import (
    EnforcementAttestation,
)


def test_attestation_subject():

    decision = EnforcementDecision(
        status="EXECUTE",
    )

    attestation = (
        EnforcementAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "enforcement_decision"
    )


def test_attestation_uses_status():

    decision = EnforcementDecision(
        status="EXECUTE",
    )

    attestation = (
        EnforcementAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.evidence_hash
        == "EXECUTE"
    )


def test_attestation_preserves_id():

    decision = EnforcementDecision(
        status="EXECUTE",
    )

    attestation = (
        EnforcementAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
