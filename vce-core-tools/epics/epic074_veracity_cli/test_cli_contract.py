from pathlib import Path


CONTRACT = Path(
    "epics/epic074_veracity_cli/cli_contract.md"
)


def test_cli_contract_exists():

    assert CONTRACT.exists()


def test_cli_contract_lists_commands():

    content = CONTRACT.read_text()

    assert "veracity prove" in content
    assert "veracity verify" in content
    assert "veracity audit" in content


def test_cli_contract_requires_json_output():

    content = CONTRACT.read_text()

    assert "valid JSON" in content
    assert "machine-readable" in content
    assert "CI/CD friendly" in content
