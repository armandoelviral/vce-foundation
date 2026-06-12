from epics.epic084_witness_consensus_layer.consensus_policy import (
    ConsensusPolicy,
)


def build_policy():

    return ConsensusPolicy(
        policy_id="policy-2-of-3",
        required_votes=2,
        total_witnesses=3,
    )


def test_policy_creation():

    policy = build_policy()

    assert policy.policy_id == "policy-2-of-3"
    assert policy.required_votes == 2
    assert policy.total_witnesses == 3


def test_policy_label():

    policy = build_policy()

    assert policy.policy_label() == "2-of-3"


def test_policy_satisfied_when_required_votes_met():

    policy = build_policy()

    assert policy.is_satisfied(
        observed_votes=2,
    ) is True


def test_policy_satisfied_when_votes_exceed_requirement():

    policy = build_policy()

    assert policy.is_satisfied(
        observed_votes=3,
    ) is True


def test_policy_rejects_insufficient_votes():

    policy = build_policy()

    assert policy.is_satisfied(
        observed_votes=1,
    ) is False
