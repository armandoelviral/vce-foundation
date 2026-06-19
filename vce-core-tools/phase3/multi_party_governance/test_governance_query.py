from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)

from phase3.multi_party_governance.governance_query import (
    GovernanceQuery,
)


def test_query_returns_resolution():

    resolution = GovernanceResolution(
        status="RESOLVED",
    )

    query = GovernanceQuery(
        {
            "resolution-001": resolution,
        }
    )

    result = query.by_id(
        "resolution-001"
    )

    assert result == resolution


def test_query_returns_none_for_missing():

    query = GovernanceQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    resolution = GovernanceResolution(
        status="RESOLVED",
    )

    query = GovernanceQuery(
        {
            "resolution-001": resolution,
        }
    )

    result = query.by_id(
        "resolution-001"
    )

    assert result.status == "RESOLVED"
