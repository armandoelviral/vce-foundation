from pathlib import Path


def test_fuzz_campaign_plan_exists():

    assert Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_plan.md"
    ).exists()


def test_plan_defines_replay_campaign():

    content = Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_plan.md"
    ).read_text()

    assert "Campaign 1 — Replay" in content
    assert "fuzz_target_1" in content
    assert "100000" in content


def test_plan_defines_hash_chain_campaign():

    content = Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_plan.md"
    ).read_text()

    assert "Campaign 2 — Hash Chain" in content
    assert "hash_chain_fuzz_target" in content


def test_plan_defines_wal_recovery_campaign():

    content = Path(
        "epics/epic069_long_running_fuzz/fuzz_campaign_plan.md"
    ).read_text()

    assert "Campaign 3 — WAL Recovery" in content
    assert "wal_recovery_fuzz_target" in content
