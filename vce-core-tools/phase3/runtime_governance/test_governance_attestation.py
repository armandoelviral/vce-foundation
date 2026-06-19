from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)

from phase3.runtime_governance.governance_attestation import (
    GovernanceAttestation,
)


def test_attestation_subject():

    decision = GovernanceDecision(
        status="APPROVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.subject
        == "governance_decision"
    )


def test_attestation_uses_status():

    decision = GovernanceDecision(
        status="APPROVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.evidence_hash
        == "APPROVED"
    )


def test_attestation_preserves_id():

    decision = GovernanceDecision(
        status="APPROVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            decision=decision,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
