from epics.ztc24_production_deployment_framework.release_gate_policy import (
    ReleaseGatePolicy,
)


def test_accepts_release_when_all_gates_pass():

    policy = ReleaseGatePolicy()

    assert policy.approve(
        security_validated=True,
        governance_approved=True,
    )


def test_rejects_missing_security_validation():

    policy = ReleaseGatePolicy()

    assert not policy.approve(
        security_validated=False,
        governance_approved=True,
    )


def test_rejects_missing_governance_approval():

    policy = ReleaseGatePolicy()

    assert not policy.approve(
        security_validated=True,
        governance_approved=False,
    )


def test_rejects_when_both_gates_fail():

    policy = ReleaseGatePolicy()

    assert not policy.approve(
        security_validated=False,
        governance_approved=False,
    )
