from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)

from phase3.runtime_enforcement_engine.enforcement_query import (
    EnforcementQuery,
)


def test_query_returns_decision():

    decision = EnforcementDecision(
        status="EXECUTE",
    )

    query = EnforcementQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result == decision


def test_query_returns_none_for_missing():

    query = EnforcementQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    decision = EnforcementDecision(
        status="BLOCK",
    )

    query = EnforcementQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result.status == "BLOCK"
