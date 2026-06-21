from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_revocation import (
    TcuRegistryRevocation,
)


def test_revokes_member():

    registry = build_registry()

    result = TcuRegistryRevocation.revoke(
        registry,
        "did:tcn:test:01",
    )

    assert result is True

    assert (
        registry.entries[0].status
        == "REVOKED"
    )


def test_missing_member_returns_false():

    registry = build_registry()

    result = TcuRegistryRevocation.revoke(
        registry,
        "did:tcn:test:missing",
    )

    assert result is False


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
