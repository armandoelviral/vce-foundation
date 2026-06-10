from epics.epic078_multi_region_worm_evidence_ledger.s3_worm_bucket import (
    S3WORMBucket,
)


def test_s3_worm_bucket_model_creation():

    bucket = S3WORMBucket(
        bucket_name="vce-immutable-evidence-ledger-primary",
        region="us-east-1",
        object_lock_enabled=True,
        versioning_enabled=True,
        retention_mode="COMPLIANCE",
        retention_days=90,
    )

    assert bucket.bucket_name == "vce-immutable-evidence-ledger-primary"
    assert bucket.region == "us-east-1"


def test_s3_worm_bucket_compliance_ready():

    bucket = S3WORMBucket(
        bucket_name="vce-immutable-evidence-ledger-primary",
        region="us-east-1",
        object_lock_enabled=True,
        versioning_enabled=True,
        retention_mode="COMPLIANCE",
        retention_days=90,
    )

    assert bucket.is_compliance_ready() is True


def test_s3_worm_bucket_rejects_missing_object_lock():

    bucket = S3WORMBucket(
        bucket_name="vce-unsafe-ledger",
        region="us-east-1",
        object_lock_enabled=False,
        versioning_enabled=True,
        retention_mode="COMPLIANCE",
        retention_days=90,
    )

    assert bucket.is_compliance_ready() is False


def test_s3_worm_bucket_rejects_missing_versioning():

    bucket = S3WORMBucket(
        bucket_name="vce-unsafe-ledger",
        region="us-east-1",
        object_lock_enabled=True,
        versioning_enabled=False,
        retention_mode="COMPLIANCE",
        retention_days=90,
    )

    assert bucket.is_compliance_ready() is False


def test_s3_worm_bucket_rejects_non_compliance_mode():

    bucket = S3WORMBucket(
        bucket_name="vce-governance-ledger",
        region="us-east-1",
        object_lock_enabled=True,
        versioning_enabled=True,
        retention_mode="GOVERNANCE",
        retention_days=90,
    )

    assert bucket.is_compliance_ready() is False
