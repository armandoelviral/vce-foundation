from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)

from phase3.governance_merkle_root.root_attestation import (
    RootAttestation,
)


def test_attestation_subject():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    attestation = (
        RootAttestation.attest(
            attestation_id="att-001",
            root=root,
        )
    )

    assert (
        attestation.subject
        == "governance_merkle_root"
    )


def test_attestation_uses_root_id():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    attestation = (
        RootAttestation.attest(
            attestation_id="att-001",
            root=root,
        )
    )

    assert (
        attestation.evidence_hash
        == "root-001"
    )


def test_attestation_preserves_id():

    root = GovernanceMerkleRootRecord(
        root_id="root-001",
        root_hash="root-hash-001",
        leaf_count=3,
    )

    attestation = (
        RootAttestation.attest(
            attestation_id="att-001",
            root=root,
        )
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
