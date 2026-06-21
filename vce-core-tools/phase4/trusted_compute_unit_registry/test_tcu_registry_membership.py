from phase4.trusted_compute_unit_registry.tcu_registry import (
    TcuRegistry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_entry import (
    TcuRegistryEntry,
)

from phase4.trusted_compute_unit_registry.tcu_registry_membership import (
    TcuRegistryMembership,
)


def test_active_member_exists():

    registry = build_registry()

    assert (
        TcuRegistryMembership.is_member(
            registry,
            "did:tcn:test:01",
        )
        is True
    )


def test_missing_member_fails():

    registry = build_registry()

    assert (
        TcuRegistryMembership.is_member(
            registry,
            "did:tcn:test:missing",
        )
        is False
    )


def test_inactive_member_fails():

    registry = TcuRegistry()

    registry.add(
        TcuRegistryEntry(
            did="did:tcn:test:02",
            identity_hash="identity-002",
            attestation_root="attestation-002",
            status="SUSPENDED",
        )
    )

    assert (
        TcuRegistryMembership.is_member(
            registry,
            "did:tcn:test:02",
        )
        is False
    )


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
