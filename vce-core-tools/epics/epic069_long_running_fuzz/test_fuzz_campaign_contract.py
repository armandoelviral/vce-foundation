from pathlib import Path


def test_fuzz_campaign_contract_exists():

    assert Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_contract.md"
    ).exists()


def test_contract_lists_required_targets():

    content = Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_contract.md"
    ).read_text()

    assert "Replay Target" in content
    assert "Hash Chain Target" in content
    assert "WAL Recovery Target" in content
    assert "Success Criteria" in content
