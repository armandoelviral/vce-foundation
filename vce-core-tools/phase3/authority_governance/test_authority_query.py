from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)

from phase3.authority_governance.authority_registry import (
    AuthorityRegistry,
)

from phase3.authority_governance.authority_query import (
    AuthorityQuery,
)


def test_query_returns_authority():

    registry = AuthorityRegistry()

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    registry.add(authority)

    query = AuthorityQuery(registry)

    result = query.by_id("auth-001")

    assert result == authority


def test_query_returns_none_for_missing():

    registry = AuthorityRegistry()

    query = AuthorityQuery(registry)

    assert query.by_id("missing") is None


def test_query_returns_role():

    registry = AuthorityRegistry()

    authority = AuthorityRecord(
        authority_id="auth-001",
        principal_id="principal-001",
        role="GOVERNOR",
    )

    registry.add(authority)

    query = AuthorityQuery(registry)

    result = query.by_id("auth-001")

    assert result.role == "GOVERNOR"
