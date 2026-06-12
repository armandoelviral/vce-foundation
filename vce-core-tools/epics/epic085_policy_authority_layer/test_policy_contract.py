from pathlib import Path


CONTRACT = Path(
    "epics/epic085_policy_authority_layer/policy_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_policy_properties():

    content = CONTRACT.read_text()

    assert "versioned" in content
    assert "approved" in content
    assert "attestable" in content
    assert "revocable" in content
    assert "replayable" in content


def test_contract_defines_policy_outputs():

    content = CONTRACT.read_text()

    assert "policy_id" in content
    assert "policy_version" in content
    assert "policy_hash" in content


def test_contract_preserves_scope_boundary():

    content = CONTRACT.read_text()

    assert "Policies govern evidence admission" in content
