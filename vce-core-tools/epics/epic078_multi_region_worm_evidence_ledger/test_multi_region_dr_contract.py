from pathlib import Path


CONTRACT = Path(
    "epics/epic078_multi_region_worm_evidence_ledger/multi_region_dr_contract.md"
)


def test_contract_exists():

    assert CONTRACT.exists()


def test_contract_defines_disaster_recovery_events():

    content = CONTRACT.read_text()

    assert "region outage" in content
    assert "availability zone outage" in content
    assert "bucket compromise" in content
    assert "cluster compromise" in content
    assert "credential compromise" in content


def test_contract_requires_worm_controls():

    content = CONTRACT.read_text()

    assert "object lock" in content
    assert "versioning" in content
    assert "immutable retention" in content


def test_contract_requires_cross_region_durability():

    content = CONTRACT.read_text()

    assert "cross-region durability" in content
    assert "Global Audit Replica" in content
