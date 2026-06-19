from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)

from phase3.admission_control_engine.admission_query import (
    AdmissionQuery,
)


def test_query_returns_decision():

    decision = AdmissionDecision(
        status="ALLOW",
    )

    query = AdmissionQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result == decision


def test_query_returns_none_for_missing():

    query = AdmissionQuery(
        {}
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    decision = AdmissionDecision(
        status="ALLOW",
    )

    query = AdmissionQuery(
        {
            "decision-001": decision,
        }
    )

    result = query.by_id(
        "decision-001"
    )

    assert result.status == "ALLOW"
