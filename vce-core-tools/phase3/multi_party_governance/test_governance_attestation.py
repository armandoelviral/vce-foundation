from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)

from phase3.multi_party_governance.governance_attestation import (
    GovernanceAttestation,
)


def test_attestation_subject():

    resolution = GovernanceResolution(
        status="RESOLVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            resolution=resolution,
        )
    )

    assert (
        attestation.subject
        == "governance_resolution"
    )


def test_attestation_uses_resolution_status():

    resolution = GovernanceResolution(
        status="RESOLVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            resolution=resolution,
        )
    )

    assert (
        attestation.evidence_hash
        == "RESOLVED"
    )


def test_attestation_preserves_id():

    resolution = GovernanceResolution(
        status="RESOLVED",
    )

    attestation = (
        GovernanceAttestation.attest(
            attestation_id="att-001",
            resolution=resolution,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
