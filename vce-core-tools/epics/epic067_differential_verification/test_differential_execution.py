from pathlib import Path


def test_python_runtime_exists():

    assert Path(
        "epics/epic012_replay_runtime/replay_engine.py"
    ).exists()


def test_rust_runtime_exists():

    assert Path(
        "fuzz-runtime/src/lib.rs"
    ).exists()


def test_shared_corpus_exists():

    assert Path(
        "epics/epic067_differential_verification/corpus/replay_events.txt"
    ).exists()
