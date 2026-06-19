from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)

from phase3.trust_policy_engine.trust_query import (
    TrustQuery,
)


def test_query_returns_decision():

    decision = TrustDecision(
        status="TRUSTED",
    )

    query = TrustQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result == decision


def test_query_returns_none_for_missing():

    query = TrustQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    decision = TrustDecision(
        status="TRUSTED",
    )

    query = TrustQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result.status == "TRUSTED"
