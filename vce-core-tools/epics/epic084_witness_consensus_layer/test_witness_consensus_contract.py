from pathlib import Path


CONTRACT = Path(
    "epics/epic084_witness_consensus_layer/witness_consensus_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_core_principle():

    content = CONTRACT.read_text()

    assert "single witness provides observation" in content.lower()
    assert "multiple independent witnesses provide consensus" in content.lower()


def test_contract_defines_outputs():

    content = CONTRACT.read_text()

    assert "CONSENSUS_ACHIEVED" in content
    assert "CONSENSUS_NOT_ACHIEVED" in content


def test_contract_supports_thresholds():

    content = CONTRACT.read_text()

    assert "2 of 3" in content
    assert "3 of 5" in content
    assert "5 of 7" in content


def test_contract_preserves_scope_boundary():

    content = CONTRACT.read_text()

    assert "does not prove correctness of evidence" in content
