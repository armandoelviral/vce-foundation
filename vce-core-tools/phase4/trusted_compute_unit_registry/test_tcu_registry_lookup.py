from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_lookup import (
    TcuRegistryLookup,
)


def test_lookup_returns_entry():

    registry = build_registry()

    entry = TcuRegistryLookup.by_did(
        registry,
        "did:tcn:test:01",
    )

    assert entry.did == "did:tcn:test:01"


def test_lookup_missing_returns_none():

    registry = build_registry()

    entry = TcuRegistryLookup.by_did(
        registry,
        "did:tcn:test:missing",
    )

    assert entry is None


def test_lookup_returns_identity_hash():

    registry = build_registry()

    entry = TcuRegistryLookup.by_did(
        registry,
        "did:tcn:test:01",
    )

    assert entry.identity_hash == "identity-001"


def build_registry():

    registry = TcuRegistry()

    registry.add(
        TcuRegistryEntry(
            did="did:tcn:test:01",
            identity_hash="identity-001",
            attestation_root="attestation-001",
            status="ACTIVE",
        )
    )

    return registry
