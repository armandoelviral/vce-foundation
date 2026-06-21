from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_hasher import (
    TcuRegistryHasher,
)


def test_generates_registry_hash():

    registry = build_registry()

    result = TcuRegistryHasher.hash_registry(
        registry
    )

    assert isinstance(result, str)
    assert len(result) == 64


def test_same_registry_same_hash():

    registry = build_registry()

    h1 = TcuRegistryHasher.hash_registry(registry)
    h2 = TcuRegistryHasher.hash_registry(registry)

    assert h1 == h2


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
