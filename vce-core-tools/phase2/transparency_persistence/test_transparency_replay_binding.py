from phase2.transparency_persistence.transparency_replay_binding import (
    TransparencyReplayBinding,
)


def test_binding_contains_root_hash():

    binding = TransparencyReplayBinding(
        root_hash="root-001",
        replay_lsn=100,
    )

    assert binding.root_hash == "root-001"


def test_binding_contains_replay_lsn():

    binding = TransparencyReplayBinding(
        root_hash="root-001",
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100


def test_binding_serializes():

    binding = TransparencyReplayBinding(
        root_hash="root-001",
        replay_lsn=100,
    )

    assert binding.to_dict() == {
        "root_hash": "root-001",
        "replay_lsn": 100,
    }
