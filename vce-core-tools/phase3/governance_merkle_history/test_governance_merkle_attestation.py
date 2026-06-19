from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.governance_merkle_attestation import (
    GovernanceMerkleAttestation,
)


def test_attestation_subject():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    attestation = (
        GovernanceMerkleAttestation.attest(
            attestation_id="att-001",
            leaf=leaf,
        )
    )

    assert (
        attestation.subject
        == "governance_merkle_leaf"
    )


def test_attestation_uses_leaf_id():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    attestation = (
        GovernanceMerkleAttestation.attest(
            attestation_id="att-001",
            leaf=leaf,
        )
    )

    assert (
        attestation.evidence_hash
        == "leaf-001"
    )


def test_attestation_preserves_id():

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    attestation = (
        GovernanceMerkleAttestation.attest(
            attestation_id="att-001",
            leaf=leaf,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
