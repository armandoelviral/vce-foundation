from pathlib import Path


def test_shared_corpus_exists():

    path = Path(
        "epics/epic067_differential_verification/corpus/replay_events.txt"
    )

    assert path.exists()


def test_shared_corpus_contains_events():

    content = Path(
        "epics/epic067_differential_verification/corpus/replay_events.txt"
    ).read_text()

    assert "APPEND_EVIDENCE" in content
    assert "REGISTER_ARTIFACT" in content
    assert "SEAL_SNAPSHOT" in content
