from phase4.reputation_constitution_layer.reputation_state import (
    ReputationState,
)


def test_contains_score():

    state = ReputationState(
        score=100,
    )

    assert state.score == 100


def test_serializes():

    state = ReputationState(
        score=100,
    )

    assert state.to_dict() == {
        "score": 100,
    }


def test_supports_updates():

    state = ReputationState(
        score=75,
    )

    assert state.score == 75
