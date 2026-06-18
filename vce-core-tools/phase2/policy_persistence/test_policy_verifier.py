from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_verifier import (
    PolicyVerifier,
)


def test_verifier_accepts_matching_version():

    policy = PolicyRecord(
        policy_id="policy-001",
        version=2,
        rule="rule-v2",
    )

    assert (
        PolicyVerifier.verify(
            policy,
            expected_version=2,
        )
        is True
    )


def test_verifier_rejects_wrong_version():

    policy = PolicyRecord(
        policy_id="policy-001",
        version=2,
        rule="rule-v2",
    )

    assert (
        PolicyVerifier.verify(
            policy,
            expected_version=1,
        )
        is False
    )


def test_verifier_rejects_none_policy():

    assert (
        PolicyVerifier.verify(
            None,
            expected_version=1,
        )
        is False
    )
