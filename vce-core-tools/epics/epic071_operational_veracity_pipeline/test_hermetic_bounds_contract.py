from pathlib import Path


CONTRACT = Path(
    "epics/epic071_operational_veracity_pipeline/hermetic_bounds_contract.md"
)


def test_hermetic_bounds_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_hermetic_requirements():

    content = CONTRACT.read_text()

    assert "deterministic runtime behavior" in content
    assert "isolated process boundary" in content
    assert "restricted host filesystem access" in content
    assert "disabled or isolated network access" in content


def test_contract_defines_ai_runtime_requirements():

    content = CONTRACT.read_text()

    assert "model weights hash" in content
    assert "inference runtime hash" in content
    assert "deterministic execution configuration" in content
    assert "WASM or equivalent sandbox boundary" in content


def test_contract_defines_supply_chain_requirements():

    content = CONTRACT.read_text()

    assert "container image digest" in content
    assert "build runner identity" in content
    assert "compiled artifact hash" in content
    assert "dependency lockfile hash" in content


def test_contract_defines_required_evidence_fields():

    content = CONTRACT.read_text()

    assert "runtime_id" in content
    assert "execution_id" in content
    assert "input_hash" in content
    assert "code_hash" in content
    assert "environment_hash" in content
    assert "deterministic_policy" in content
