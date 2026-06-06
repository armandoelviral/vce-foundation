from pathlib import Path


def test_runtime_agreement_contract_exists():

    assert Path(
        "epics/epic070_veracity_runtime_integration/runtime_agreement_contract.md"
    ).exists()


def test_contract_lists_core_components():

    content = Path(
        "epics/epic070_veracity_runtime_integration/runtime_agreement_contract.md"
    ).read_text()

    assert "Python ReplayEngine" in content
    assert "Rust replay_events" in content
    assert "WASM build artifact" in content
    assert "Wasmtime execution" in content
    assert "WALRecovery" in content
    assert "cargo-fuzz campaign evidence" in content


def test_contract_defines_agreement_properties():

    content = Path(
        "epics/epic070_veracity_runtime_integration/runtime_agreement_contract.md"
    ).read_text()

    assert "same input -> same sequence_number" in content
    assert "same input -> same state_hash" in content
    assert "same input -> deterministic output" in content
