from phase2.policy_persistence.policy_replay_binding import (
    PolicyReplayBinding,
)


def test_binding_contains_policy_id():

    binding = PolicyReplayBinding(
        policy_id="policy-001",
        version=2,
        replay_lsn=100,
    )

    assert binding.policy_id == "policy-001"


def test_binding_contains_version():

    binding = PolicyReplayBinding(
        policy_id="policy-001",
        version=2,
        replay_lsn=100,
    )

    assert binding.version == 2


def test_binding_contains_replay_lsn():

    binding = PolicyReplayBinding(
        policy_id="policy-001",
        version=2,
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100


def test_binding_serializes():

    binding = PolicyReplayBinding(
        policy_id="policy-001",
        version=2,
        replay_lsn=100,
    )

    assert binding.to_dict() == {
        "policy_id": "policy-001",
        "version": 2,
        "replay_lsn": 100,
    }
