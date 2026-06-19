from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)

from phase3.runtime_governance.governance_query import (
    GovernanceQuery,
)


def test_query_returns_decision():

    decision = GovernanceDecision(
        status="APPROVED",
    )

    query = GovernanceQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result == decision


def test_query_returns_none_for_missing():

    query = GovernanceQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    decision = GovernanceDecision(
        status="APPROVED",
    )

    query = GovernanceQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result.status == "APPROVED"
