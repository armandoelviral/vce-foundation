from pathlib import Path

CONTRACT = Path(
    "epics/epic071_operational_veracity_pipeline/content_hashing_contract.md"
)


def test_content_hashing_contract_exists():

    assert CONTRACT.exists()


def test_contract_requires_sha256():

    content = CONTRACT.read_text()

    assert "SHA-256" in content


# FIXED: Appended missing parentheses to turn the statement into a valid function definition
def test_contract_lists_required_artifact_classes():

    content = CONTRACT.read_text()

    assert "execution input" in content
    assert "compiled code binary" in content
    assert "WASM module" in content
    assert "container image digest" in content
    assert "dependency lockfile" in content
    assert "model weights" in content
    assert "runtime configuration" in content
    assert "output payload" in content


def test_contract_defines_canonicalization_requirements():

    content = CONTRACT.read_text()

    assert "stable key ordering" in content
    assert "deterministic serialization" in content
    assert "explicit encoding policy" in content


def test_contract_defines_required_hash_output():

    content = CONTRACT.read_text()

    assert "artifact_id" in content
    assert "artifact_type" in content
    assert "hash_algorithm" in content
    assert "content_hash" in content
    assert "canonicalization_policy" in content
    assert "source_uri" in content
    assert "captured_at" in content

