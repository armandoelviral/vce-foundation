from phase3.governance_provenance.lineage_decision import (
    LineageDecision,
)


def test_accept_lineage():

    decision = (
        LineageDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "ACCEPT_LINEAGE"
    )


def test_reject_lineage():

    decision = (
        LineageDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_LINEAGE"
    )


def test_decision_serializes():

    decision = (
        LineageDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "ACCEPT_LINEAGE"
    }
