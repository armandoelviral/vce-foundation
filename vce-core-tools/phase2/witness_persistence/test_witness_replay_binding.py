from phase2.witness_persistence.witness_replay_binding import (
    WitnessReplayBinding,
)


def test_binding_contains_decision_id():

    binding = WitnessReplayBinding(
        decision_id="decision-001",
        replay_lsn=100,
    )

    assert binding.decision_id == "decision-001"


def test_binding_contains_replay_lsn():

    binding = WitnessReplayBinding(
        decision_id="decision-001",
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100


def test_binding_serializes():

    binding = WitnessReplayBinding(
        decision_id="decision-001",
        replay_lsn=100,
    )

    assert binding.to_dict() == {
        "decision_id": "decision-001",
        "replay_lsn": 100,
    }
