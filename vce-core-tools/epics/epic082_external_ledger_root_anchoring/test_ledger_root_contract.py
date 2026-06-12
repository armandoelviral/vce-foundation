from pathlib import Path


CONTRACT = Path(
    "epics/epic082_external_ledger_root_anchoring/ledger_root_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_root_fields():

    content = CONTRACT.read_text()

    assert "root_hash" in content
    assert "sequence_start" in content
    assert "sequence_end" in content
    assert "evidence_count" in content
    assert "region" in content


def test_contract_defines_properties():

    content = CONTRACT.read_text()

    assert "deterministic" in content
    assert "reproducible" in content
    assert "independently verifiable" in content


def test_contract_excludes_raw_data():

    content = CONTRACT.read_text()

    assert "raw evidence" in content
    assert "PII" in content
    assert "PHI" in content
