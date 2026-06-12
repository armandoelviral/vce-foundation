from pathlib import Path


CONTRACT = Path(
    "epics/epic086_historical_policy_replay_audit/historical_replay_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_principle():

    content = CONTRACT.read_text()

    assert (
        "History must be replayed using the policy"
        in content
    )


def test_contract_defines_required_inputs():

    content = CONTRACT.read_text()

    assert "evidence_hash" in content
    assert "policy_id" in content
    assert "policy_version" in content
    assert "execution_attributes" in content


def test_contract_defines_outputs():

    content = CONTRACT.read_text()

    assert "REPLAY_MATCH" in content
    assert "REPLAY_MISMATCH" in content


def test_contract_requires_version_pinning():

    content = CONTRACT.read_text()

    assert "version-pinned" in content


def test_contract_preserves_scope_boundary():

    content = CONTRACT.read_text()

    assert "Replay reconstructs history" in content
