from epics.epic078_multi_region_worm_evidence_ledger.crr_replication_policy import (
    CRRReplicationPolicy,
)


def build_policy():

    return CRRReplicationPolicy(
        source_bucket="vce-primary",
        destination_bucket="vce-secondary",
        source_region="us-east-1",
        destination_region="us-west-2",
        object_lock_replication=True,
        versioning_required=True,
        enabled=True,
    )


def test_crr_policy_creation():

    policy = build_policy()

    assert policy.source_bucket == "vce-primary"
    assert policy.destination_bucket == "vce-secondary"


def test_crr_policy_is_valid():

    policy = build_policy()

    assert policy.is_valid() is True


def test_crr_policy_requires_distinct_regions():

    policy = CRRReplicationPolicy(
        source_bucket="vce-primary",
        destination_bucket="vce-secondary",
        source_region="us-east-1",
        destination_region="us-east-1",
        object_lock_replication=True,
        versioning_required=True,
        enabled=True,
    )

    assert policy.is_valid() is False


def test_crr_policy_requires_object_lock_replication():

    policy = CRRReplicationPolicy(
        source_bucket="vce-primary",
        destination_bucket="vce-secondary",
        source_region="us-east-1",
        destination_region="us-west-2",
        object_lock_replication=False,
        versioning_required=True,
        enabled=True,
    )

    assert policy.is_valid() is False


def test_crr_policy_requires_versioning():

    policy = CRRReplicationPolicy(
        source_bucket="vce-primary",
        destination_bucket="vce-secondary",
        source_region="us-east-1",
        destination_region="us-west-2",
        object_lock_replication=True,
        versioning_required=False,
        enabled=True,
    )

    assert policy.is_valid() is False
