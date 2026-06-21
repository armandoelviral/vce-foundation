from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)


def test_starts_empty():

    registry = TcuRegistry()

    assert len(registry.entries) == 0


def test_add_entry():

    registry = TcuRegistry()

    registry.add(
        TcuRegistryEntry(
            did="did:tcn:test:01",
            identity_hash="identity-001",
            attestation_root="attestation-001",
            status="ACTIVE",
        )
    )

    assert len(registry.entries) == 1


def test_contains_entry():

    registry = TcuRegistry()

    entry = TcuRegistryEntry(
        did="did:tcn:test:01",
        identity_hash="identity-001",
        attestation_root="attestation-001",
        status="ACTIVE",
    )

    registry.add(entry)

    assert registry.entries[0] == entry


def test_serializes():

    registry = TcuRegistry()

    registry.add(
        TcuRegistryEntry(
            did="did:tcn:test:01",
            identity_hash="identity-001",
            attestation_root="attestation-001",
            status="ACTIVE",
        )
    )

    data = registry.to_dict()

    assert "entries" in data
    assert len(data["entries"]) == 1
