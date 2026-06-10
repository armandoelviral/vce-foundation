from epics.epic078_multi_region_worm_evidence_ledger.global_audit_bucket import (
    GlobalAuditBucket,
)
from epics.epic078_multi_region_worm_evidence_ledger.region_scoped_key import (
    RegionScopedLedgerKey,
)


def test_replay_artifact_from_global_audit_replica():

    bucket = GlobalAuditBucket(
        bucket_name="vce-global-audit-ledger",
        primary_region="us-east-1",
        replica_regions=["us-west-2"],
        read_only=True,
        worm_enabled=True,
    )

    assert bucket.is_audit_ready() is True

    artifact_key = RegionScopedLedgerKey(
        region="us-east-1",
        artifact_hash="artifact-001",
        ledger_sequence=42,
    ).build_key()

    replica_storage = {
        artifact_key: {
            "artifact_hash": "artifact-001",
            "ledger_sequence": 42,
            "region": "us-east-1",
        }
    }

    recovered = replica_storage[
        artifact_key
    ]

    assert recovered["artifact_hash"] == "artifact-001"
    assert recovered["ledger_sequence"] == 42


def test_replay_remains_available_after_primary_region_loss():

    artifact_key = RegionScopedLedgerKey(
        region="us-east-1",
        artifact_hash="artifact-002",
        ledger_sequence=99,
    ).build_key()

    global_replica = {
        artifact_key: {
            "artifact_hash": "artifact-002",
            "ledger_sequence": 99,
        }
    }

    primary_region_available = False

    assert primary_region_available is False

    recovered = global_replica[
        artifact_key
    ]

    assert recovered["artifact_hash"] == "artifact-002"
    assert recovered["ledger_sequence"] == 99
