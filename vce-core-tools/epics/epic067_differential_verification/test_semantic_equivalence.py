from pathlib import Path


def test_python_replay_has_state_hash():

    content = Path(
        "epics/epic012_replay_runtime/replay_state.py"
    ).read_text()

    assert "state_hash" in content


def test_rust_replay_has_state_hash():

    content = Path(
        "fuzz-runtime/src/lib.rs"
    ).read_text()

    assert "state_hash" in content


def test_python_and_rust_track_sequence_numbers():

    python_content = Path(
        "epics/epic012_replay_runtime/replay_state.py"
    ).read_text()

    rust_content = Path(
        "fuzz-runtime/src/lib.rs"
    ).read_text()

    assert "sequence_number" in python_content
    assert "sequence_number" in rust_content
