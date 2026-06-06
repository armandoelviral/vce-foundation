from epics.epic012_replay_runtime.replay_engine import ReplayEngine


def test_replay_is_deterministic():

    events = [
        "AppendEvidence",
        "SealSnapshot",
        "RegisterArtifact",
    ]

    engine = ReplayEngine()

    run_a = engine.replay(events)
    run_b = engine.replay(events)

    assert run_a.state_hash == run_b.state_hash
    assert run_a.sequence_number == run_b.sequence_number


def test_replay_tracks_sequence_number():

    events = [
        "AppendEvidence",
        "SealSnapshot",
        "RegisterArtifact",
    ]

    engine = ReplayEngine()

    state = engine.replay(events)

    assert state.sequence_number == 3
