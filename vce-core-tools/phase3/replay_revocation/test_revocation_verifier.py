from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)

from phase3.replay_revocation.revocation_verifier import (
    RevocationVerifier,
)


def test_revoked_certificate_returns_true():

    registry = RevocationRegistry()

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-001",
            certificate_id="cert-001",
            reason="key_compromise",
        )
    )

    assert (
        RevocationVerifier.is_revoked(
            registry,
            "cert-001",
        )
        is True
    )


def test_non_revoked_certificate_returns_false():

    registry = RevocationRegistry()

    assert (
        RevocationVerifier.is_revoked(
            registry,
            "cert-001",
        )
        is False
    )


def test_multiple_revocations_supported():

    registry = RevocationRegistry()

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-001",
            certificate_id="cert-001",
            reason="key_compromise",
        )
    )

    registry.add(
        ReplayRevocationRecord(
            revocation_id="rev-002",
            certificate_id="cert-002",
            reason="policy_violation",
        )
    )

    assert (
        RevocationVerifier.is_revoked(
            registry,
            "cert-002",
        )
        is True
    )
