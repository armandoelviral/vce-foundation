from epics.ztc24_production_deployment_framework.rollback_record import (
    RollbackRecord,
)


def test_record_contains_failed_release():

    record = RollbackRecord(
        failed_release_id="release-002",
        restored_release_id="release-001",
        reason="production_failure",
    )

    assert record.failed_release_id == "release-002"


def test_record_contains_restored_release():

    record = RollbackRecord(
        failed_release_id="release-002",
        restored_release_id="release-001",
        reason="production_failure",
    )

    assert record.restored_release_id == "release-001"


def test_record_contains_reason():

    record = RollbackRecord(
        failed_release_id="release-002",
        restored_release_id="release-001",
        reason="production_failure",
    )

    assert record.reason == "production_failure"


def test_record_serializes():

    record = RollbackRecord(
        failed_release_id="release-002",
        restored_release_id="release-001",
        reason="production_failure",
    )

    assert record.to_dict() == {
        "failed_release_id": "release-002",
        "restored_release_id": "release-001",
        "reason": "production_failure",
    }
