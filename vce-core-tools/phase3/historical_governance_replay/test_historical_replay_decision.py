from phase3.historical_governance_replay.historical_replay_decision import (
    HistoricalReplayDecision,
)


def test_replay_decision():

    decision = (
        HistoricalReplayDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "REPLAY"
    )


def test_reject_replay_decision():

    decision = (
        HistoricalReplayDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_REPLAY"
    )


def test_decision_serializes():

    decision = (
        HistoricalReplayDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "REPLAY"
    }
