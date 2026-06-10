from pathlib import Path


CONTRACT = Path(
    "epics/epic077_veracity_transparency_sidecar/sidecar_architecture_contract.md"
)


def test_sidecar_architecture_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_async_sidecar_role():

    content = CONTRACT.read_text()

    assert "asynchronous transparency anchoring" in content
    assert "outside the critical runtime hot path" in content
    assert "Fast Response" in content


def test_contract_defines_sidecar_responsibilities():

    content = CONTRACT.read_text()

    assert "retry handling" in content
    assert "backoff handling" in content
    assert "SET receipt handling" in content
    assert "Prometheus metrics emission" in content


def test_contract_defines_status_model():

    content = CONTRACT.read_text()

    assert "LOCAL_COMMITTED" in content
    assert "PENDING_TRANSPARENCY" in content
    assert "ANCHORING" in content
    assert "TRANSPARENCY_ANCHORED" in content
    assert "RETRYING" in content
    assert "FAILED" in content


def test_contract_protects_hot_path():

    content = CONTRACT.read_text()

    assert "must not" in content
    assert "block application responses" in content
    assert "become required for local proof creation" in content
