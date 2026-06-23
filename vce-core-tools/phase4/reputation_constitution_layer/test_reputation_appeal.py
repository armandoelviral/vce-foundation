from phase4.reputation_constitution_layer.reputation_appeal import (
    ReputationAppeal,
)


def test_contains_appeal_id():

    appeal = ReputationAppeal(
        appeal_id="appeal-001",
        reputation_event="loss-001",
    )

    assert appeal.appeal_id == "appeal-001"


def test_contains_event():

    appeal = ReputationAppeal(
        appeal_id="appeal-001",
        reputation_event="loss-001",
    )

    assert appeal.reputation_event == "loss-001"


def test_serializes():

    appeal = ReputationAppeal(
        appeal_id="appeal-001",
        reputation_event="loss-001",
    )

    assert appeal.to_dict() == {
        "appeal_id": "appeal-001",
        "reputation_event": "loss-001",
    }
