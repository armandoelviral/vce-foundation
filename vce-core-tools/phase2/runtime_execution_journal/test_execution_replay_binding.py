from phase2.runtime_execution_journal.execution_replay_binding import (
    ExecutionReplayBinding,
)


def test_binding_contains_execution_id():

    binding = ExecutionReplayBinding(
        execution_id="exec-001",
        replay_lsn=10,
    )

    assert binding.execution_id == "exec-001"


def test_binding_contains_replay_lsn():

    binding = ExecutionReplayBinding(
        execution_id="exec-001",
        replay_lsn=10,
    )

    assert binding.replay_lsn == 10


def test_binding_serializes():

    binding = ExecutionReplayBinding(
        execution_id="exec-001",
        replay_lsn=10,
    )

    assert binding.to_dict() == {
        "execution_id": "exec-001",
        "replay_lsn": 10,
    }
