from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)

from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)

from phase3.replay_revocation.revocation_query import (
    RevocationQuery,
)


def test_query_returns_revocation():

    registry = RevocationRegistry()

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    registry.add(
        revocation
    )

    query = RevocationQuery(
        registry
    )

    result = query.by_id(
        "rev-001"
    )

    assert result == revocation


def test_query_returns_none_for_missing():

    registry = RevocationRegistry()

    query = RevocationQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_reason():

    registry = RevocationRegistry()

    revocation = ReplayRevocationRecord(
        revocation_id="rev-001",
        certificate_id="cert-001",
        reason="key_compromise",
    )

    registry.add(
        revocation
    )

    query = RevocationQuery(
        registry
    )

    result = query.by_id(
        "rev-001"
    )

    assert result.reason == "key_compromise"
