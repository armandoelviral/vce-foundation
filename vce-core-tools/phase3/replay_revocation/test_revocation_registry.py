from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)


def test_registry_starts_empty():

    registry = RevocationRegistry()

    assert registry.count() == 0


def test_registry_accepts_revocation():

    registry = RevocationRegistry()

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    registry.add(
        revocation
    )

    assert registry.count() == 1


def test_registry_returns_revocation():

    registry = RevocationRegistry()

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    registry.add(
        revocation
    )

    recovered = registry.get(
        "rev-001"
    )

    assert recovered == revocation


def test_missing_revocation_returns_none():

    registry = RevocationRegistry()

    assert registry.get(
        "missing"
    ) is None
