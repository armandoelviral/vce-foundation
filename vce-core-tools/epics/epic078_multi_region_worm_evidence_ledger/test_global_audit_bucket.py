from epics.epic078_multi_region_worm_evidence_ledger.global_audit_bucket import (
    GlobalAuditBucket,
)


def build_bucket():

    return GlobalAuditBucket(
        bucket_name="vce-global-audit-ledger",
        primary_region="us-east-1",
        replica_regions=[
            "us-west-2",
        ],
        read_only=True,
        worm_enabled=True,
    )


def test_global_audit_bucket_creation():

    bucket = build_bucket()

    assert bucket.bucket_name == "vce-global-audit-ledger"
    assert bucket.primary_region == "us-east-1"


def test_global_audit_bucket_is_audit_ready():

    bucket = build_bucket()

    assert bucket.is_audit_ready() is True


def test_global_audit_bucket_requires_read_only():

    bucket = GlobalAuditBucket(
        bucket_name="vce-global-audit-ledger",
        primary_region="us-east-1",
        replica_regions=["us-west-2"],
        read_only=False,
        worm_enabled=True,
    )

    assert bucket.is_audit_ready() is False


def test_global_audit_bucket_requires_worm():

    bucket = GlobalAuditBucket(
        bucket_name="vce-global-audit-ledger",
        primary_region="us-east-1",
        replica_regions=["us-west-2"],
        read_only=True,
        worm_enabled=False,
    )

    assert bucket.is_audit_ready() is False


def test_global_audit_bucket_requires_replica_regions():

    bucket = GlobalAuditBucket(
        bucket_name="vce-global-audit-ledger",
        primary_region="us-east-1",
        replica_regions=[],
        read_only=True,
        worm_enabled=True,
    )

    assert bucket.is_audit_ready() is False
