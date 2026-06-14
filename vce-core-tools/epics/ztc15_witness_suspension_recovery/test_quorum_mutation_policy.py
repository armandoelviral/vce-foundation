from epics.ztc15_witness_suspension_recovery.quorum_mutation_policy import (
    QuorumMutationPolicy,
)


def test_standard_quorum_without_suspensions():

    policy = QuorumMutationPolicy()

    assert policy.required_votes(
        total_witnesses=3,
        suspended_witnesses=0,
    ) == 2


def test_emergency_quorum_with_one_suspension():

    policy = QuorumMutationPolicy()

    assert policy.required_votes(
        total_witnesses=3,
        suspended_witnesses=1,
    ) == 2


def test_single_remaining_witness_not_allowed():

    policy = QuorumMutationPolicy()

    assert policy.required_votes(
        total_witnesses=3,
        suspended_witnesses=2,
    ) == 0
