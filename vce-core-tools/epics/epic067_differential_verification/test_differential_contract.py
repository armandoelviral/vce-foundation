from pathlib import Path


def test_differential_verification_contract_exists():

    path = Path(
        "epics/epic067_differential_verification/differential_contract.md"
    )

    assert path.exists()


def test_contract_names_python_and_rust_replay():

    content = Path(
        "epics/epic067_differential_verification/differential_contract.md"
    ).read_text()

    assert "Python ReplayEngine" in content
    assert "Rust replay_events" in content
    assert "state_hash" in content
    assert "sequence_number" in content
