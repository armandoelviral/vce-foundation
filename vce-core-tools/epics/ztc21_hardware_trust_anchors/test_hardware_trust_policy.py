from epics.ztc21_hardware_trust_anchors.hardware_trust_policy import (
    HardwareTrustPolicy,
)


def test_accepts_verified_anchor():

    policy = HardwareTrustPolicy()

    assert policy.admit(
        verified=True,
    )


def test_rejects_unverified_anchor():

    policy = HardwareTrustPolicy()

    assert not policy.admit(
        verified=False,
    )


def test_returns_boolean():

    policy = HardwareTrustPolicy()

    result = policy.admit(
        verified=True,
    )

    assert isinstance(
        result,
        bool,
    )
