from epics.ztc20_confidential_compute_attestation.witness_attestation_policy import (
    WitnessAttestationPolicy,
)


def test_accepts_verified_attestation():

    policy = WitnessAttestationPolicy()

    assert policy.admit(
        verified=True,
    )


def test_rejects_unverified_attestation():

    policy = WitnessAttestationPolicy()

    assert not policy.admit(
        verified=False,
    )


def test_policy_returns_boolean():

    policy = WitnessAttestationPolicy()

    result = policy.admit(
        verified=True,
    )

    assert isinstance(
        result,
        bool,
    )
