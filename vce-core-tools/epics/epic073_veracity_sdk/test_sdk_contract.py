from pathlib import Path


CONTRACT = Path(
    "epics/epic073_veracity_sdk/sdk_contract.md"
)


def test_sdk_contract_exists():

    assert CONTRACT.exists()


def test_sdk_contract_mentions_runtime():

    content = CONTRACT.read_text()

    assert "VeracityRuntime" in content


def test_sdk_contract_lists_required_operations():

    content = CONTRACT.read_text()

    assert "create_artifact" in content
    assert "anchor" in content
    assert "verify" in content
