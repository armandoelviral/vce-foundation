from epics.ztc15_witness_suspension_recovery.witness_readmission_policy import (
    WitnessReadmissionPolicy,
)


def test_recovered_witness_is_eligible():

    policy = WitnessReadmissionPolicy()

    assert policy.is_eligible(
        suspended=True,
        recovered=True,
    )


def test_non_recovered_witness_not_eligible():

    policy = WitnessReadmissionPolicy()

    assert not policy.is_eligible(
        suspended=True,
        recovered=False,
    )


def test_never_suspended_witness_not_eligible():

    policy = WitnessReadmissionPolicy()

    assert not policy.is_eligible(
        suspended=False,
        recovered=True,
    )
