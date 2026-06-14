from epics.ztc24_production_deployment_framework.disaster_recovery_plan import (
    DisasterRecoveryPlan,
)


def test_plan_contains_plan_id():

    plan = DisasterRecoveryPlan(
        plan_id="dr-001",
        recovery_target="secondary-region",
    )

    assert plan.plan_id == "dr-001"


def test_plan_contains_recovery_target():

    plan = DisasterRecoveryPlan(
        plan_id="dr-001",
        recovery_target="secondary-region",
    )

    assert (
        plan.recovery_target
        == "secondary-region"
    )


def test_plan_serializes():

    plan = DisasterRecoveryPlan(
        plan_id="dr-001",
        recovery_target="secondary-region",
    )

    assert plan.to_dict() == {
        "plan_id": "dr-001",
        "recovery_target": "secondary-region",
    }


def test_plan_is_immutable():

    plan = DisasterRecoveryPlan(
        plan_id="dr-001",
        recovery_target="secondary-region",
    )

    assert (
        plan.plan_id
        == "dr-001"
    )
