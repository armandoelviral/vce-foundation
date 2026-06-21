from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)


def test_contains_did():

    entry = TcuRegistryEntry(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
        status="ACTIVE",
    )

    assert entry.did.startswith("did:")


def test_contains_identity_hash():

    entry = TcuRegistryEntry(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
        status="ACTIVE",
    )

    assert entry.identity_hash == (
        "identity-hash-001"
    )


def test_contains_status():

    entry = TcuRegistryEntry(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
        status="ACTIVE",
    )

    assert entry.status == "ACTIVE"


def test_serializes():

    entry = TcuRegistryEntry(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
        status="ACTIVE",
    )

    assert entry.to_dict() == {
        "did":
            "did:tcn:gcp:us-central1:tcu-node-02",
        "identity_hash":
            "identity-hash-001",
        "attestation_root":
            "attestation-root-001",
        "status":
            "ACTIVE",
    }
