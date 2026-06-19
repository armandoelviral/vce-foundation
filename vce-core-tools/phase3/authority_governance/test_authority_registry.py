from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.authority_registry import (
    AuthorityRegistry,
)


def test_registry_starts_empty():

    registry = AuthorityRegistry()

    assert registry.count() == 0


def test_registry_accepts_authority():

    registry = AuthorityRegistry()

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    registry.add(
        authority
    )

    assert registry.count() == 1


def test_registry_returns_authority():

    registry = AuthorityRegistry()

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    registry.add(
        authority
    )

    recovered = registry.get(
        "auth-001"
    )

    assert recovered == authority


def test_missing_authority_returns_none():

    registry = AuthorityRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_authorities():

    registry = AuthorityRegistry()

    registry.add(
        AuthorityRecord(
            authority_id="auth-001",
            principal_id="principal-001",
            role="GOVERNOR",
        )
    )

    registry.add(
        AuthorityRecord(
            authority_id="auth-002",
            principal_id="principal-002",
            role="AUDITOR",
        )
    )

    assert registry.authority_ids() == [
        "auth-001",
        "auth-002",
    ]
