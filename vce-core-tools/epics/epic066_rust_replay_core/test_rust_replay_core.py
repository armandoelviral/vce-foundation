from pathlib import Path


def test_rust_replay_core_exists():

    content = Path("fuzz-runtime/src/lib.rs").read_text()

    assert "pub struct ReplayState" in content
    assert "pub fn replay_events" in content


def test_rust_replay_core_uses_sha256():

    content = Path("fuzz-runtime/src/lib.rs").read_text()

    assert "Sha256" in content
