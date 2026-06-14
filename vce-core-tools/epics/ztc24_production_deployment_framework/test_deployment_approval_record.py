from epics.ztc24_production_deployment_framework.deployment_approval_record import (
    DeploymentApprovalRecord,
)


def test_record_contains_release_id():

    record = DeploymentApprovalRecord(
        release_id="release-001",
        approved=True,
        reason="all_gates_passed",
    )

    assert record.release_id == "release-001"


def test_record_contains_approval_status():

    record = DeploymentApprovalRecord(
        release_id="release-001",
        approved=True,
        reason="all_gates_passed",
    )

    assert record.approved is True


def test_record_contains_reason():

    record = DeploymentApprovalRecord(
        release_id="release-001",
        approved=False,
        reason="security_validation_failed",
    )

    assert (
        record.reason
        == "security_validation_failed"
    )


def test_record_serializes():

    record = DeploymentApprovalRecord(
        release_id="release-001",
        approved=True,
        reason="all_gates_passed",
    )

    assert record.to_dict() == {
        "release_id": "release-001",
        "approved": True,
        "reason": "all_gates_passed",
    }
