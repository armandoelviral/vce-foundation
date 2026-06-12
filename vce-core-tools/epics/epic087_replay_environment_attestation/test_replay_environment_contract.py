from pathlib import Path


CONTRACT = Path(
    "epics/epic087_replay_environment_attestation/replay_environment_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_principle():

    content = CONTRACT.read_text()

    assert (
        "History must be replayed in a verifiably equivalent environment."
        in content
    )


def test_contract_defines_required_inputs():

    content = CONTRACT.read_text()

    assert "original_environment_fingerprint" in content
    assert "replay_environment_fingerprint" in content
    assert "container_digest" in content
    assert "runtime_version" in content
    assert "dependency_manifest_hash" in content
    assert "model_fingerprint" in content
    assert "policy_version" in content
    assert "execution_profile" in content


def test_contract_defines_outputs():

    content = CONTRACT.read_text()

    assert "ENVIRONMENT_EQUIVALENT" in content
    assert "ENVIRONMENT_MISMATCH" in content


def test_contract_preserves_scope_boundary():

    content = CONTRACT.read_text()

    assert "does not prove decision correctness" in content
    assert "proves replay environment compatibility" in content
