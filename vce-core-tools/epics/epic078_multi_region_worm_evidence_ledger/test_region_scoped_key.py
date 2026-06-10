from epics.epic078_multi_region_worm_evidence_ledger.region_scoped_key import (
    RegionScopedLedgerKey,
)


def test_region_scoped_key_contains_region():

    key = RegionScopedLedgerKey(
        region="us-east-1",
        artifact_hash="abc123",
        ledger_sequence=1,
    )

    assert key.build_key().startswith(
        "region=us-east-1/"
    )


def test_region_scoped_key_contains_sequence():

    key = RegionScopedLedgerKey(
        region="us-east-1",
        artifact_hash="abc123",
        ledger_sequence=42,
    )

    assert "sequence=42" in key.build_key()


def test_region_scoped_key_contains_artifact_hash():

    key = RegionScopedLedgerKey(
        region="us-west-2",
        artifact_hash="hash-001",
        ledger_sequence=7,
    )

    assert key.build_key().endswith(
        "artifact=hash-001.json"
    )


def test_distinct_regions_generate_distinct_keys():

    artifact_hash = "same-hash"

    east_key = RegionScopedLedgerKey(
        region="us-east-1",
        artifact_hash=artifact_hash,
        ledger_sequence=1,
    ).build_key()

    west_key = RegionScopedLedgerKey(
        region="us-west-2",
        artifact_hash=artifact_hash,
        ledger_sequence=1,
    ).build_key()

    assert east_key != west_key
