from epics.epic078_multi_region_worm_evidence_ledger.replication_monitor import (
    ReplicationHealth,
)


def build_health():

    return ReplicationHealth(
        source_region="us-east-1",
        destination_region="us-west-2",
        replication_enabled=True,
        last_replication_status="COMPLETED",
        replication_lag_seconds=120,
        failure_count=0,
    )


def test_replication_health_is_healthy():

    health = build_health()

    assert health.is_healthy() is True


def test_replication_health_rejects_disabled_replication():

    health = ReplicationHealth(
        source_region="us-east-1",
        destination_region="us-west-2",
        replication_enabled=False,
        last_replication_status="COMPLETED",
        replication_lag_seconds=120,
        failure_count=0,
    )

    assert health.is_healthy() is False


def test_replication_health_rejects_failed_status():

    health = ReplicationHealth(
        source_region="us-east-1",
        destination_region="us-west-2",
        replication_enabled=True,
        last_replication_status="FAILED",
        replication_lag_seconds=120,
        failure_count=1,
    )

    assert health.is_healthy() is False


def test_replication_health_rejects_excessive_lag():

    health = ReplicationHealth(
        source_region="us-east-1",
        destination_region="us-west-2",
        replication_enabled=True,
        last_replication_status="COMPLETED",
        replication_lag_seconds=1800,
        failure_count=0,
    )

    assert health.is_healthy() is False
