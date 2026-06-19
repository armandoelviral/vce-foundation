from phase3.governance_merkle_root.root_decision import (
    RootDecision,
)


def test_accept_root():

    decision = RootDecision.from_evaluation(
        True
    )

    assert decision.status == "ACCEPT_ROOT"


def test_reject_root():

    decision = RootDecision.from_evaluation(
        False
    )

    assert decision.status == "REJECT_ROOT"


def test_decision_serializes():

    decision = RootDecision.from_evaluation(
        True
    )

    assert decision.to_dict() == {
        "status": "ACCEPT_ROOT"
    }
