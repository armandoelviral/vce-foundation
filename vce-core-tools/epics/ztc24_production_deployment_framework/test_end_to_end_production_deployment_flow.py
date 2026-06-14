from epics.ztc24_production_deployment_framework.deployment_manifest import (
    DeploymentManifest,
)

from epics.ztc24_production_deployment_framework.release_gate_policy import (
    ReleaseGatePolicy,
)

from epics.ztc24_production_deployment_framework.deployment_approval_record import (
    DeploymentApprovalRecord,
)

from epics.ztc24_production_deployment_framework.environment_registry import (
    EnvironmentRegistry,
)

from epics.ztc24_production_deployment_framework.promotion_policy import (
    PromotionPolicy,
)

from epics.ztc24_production_deployment_framework.rollback_record import (
    RollbackRecord,
)

from epics.ztc24_production_deployment_framework.disaster_recovery_plan import (
    DisasterRecoveryPlan,
)


def test_end_to_end_production_deployment_flow():

    manifest = DeploymentManifest(
        release_id="release-001",
        artifact_hash="hash-001",
    )

    assert (
        manifest.release_id
        == "release-001"
    )

    gate = ReleaseGatePolicy()

    approved = gate.approve(
        security_validated=True,
        governance_approved=True,
    )

    assert approved

    approval_record = (
        DeploymentApprovalRecord(
            release_id="release-001",
            approved=True,
            reason="all_gates_passed",
        )
    )

    assert (
        approval_record.approved
        is True
    )

    registry = (
        EnvironmentRegistry()
    )

    registry.add(
        "development"
    )

    registry.add(
        "staging"
    )

    registry.add(
        "production"
    )

    assert registry.exists(
        "production"
    )

    promotion = (
        PromotionPolicy()
    )

    assert promotion.allow(
        source="development",
        target="staging",
    )

    assert promotion.allow(
        source="staging",
        target="production",
    )

    rollback = RollbackRecord(
        failed_release_id="release-002",
        restored_release_id="release-001",
        reason="production_failure",
    )

    assert (
        rollback.restored_release_id
        == "release-001"
    )

    disaster_recovery = (
        DisasterRecoveryPlan(
            plan_id="dr-001",
            recovery_target="secondary-region",
        )
    )

    assert (
        disaster_recovery.recovery_target
        == "secondary-region"
    )
