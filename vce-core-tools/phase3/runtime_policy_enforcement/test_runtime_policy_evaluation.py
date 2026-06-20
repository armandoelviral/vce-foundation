from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_evaluation import (
    RuntimePolicyEvaluation,
)


def test_matching_allow_policy():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert (
        RuntimePolicyEvaluation.evaluate(
            policy=policy,
            resource_type="REPLAY",
            action="EXECUTE",
        )
        is True
    )


def test_matching_deny_policy():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="DENY",
    )

    assert (
        RuntimePolicyEvaluation.evaluate(
            policy=policy,
            resource_type="REPLAY",
            action="EXECUTE",
        )
        is False
    )


def test_resource_mismatch_fails():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert (
        RuntimePolicyEvaluation.evaluate(
            policy=policy,
            resource_type="ARTIFACT",
            action="EXECUTE",
        )
        is False
    )


def test_action_mismatch_fails():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    assert (
        RuntimePolicyEvaluation.evaluate(
            policy=policy,
            resource_type="REPLAY",
            action="DELETE",
        )
        is False
    )


def test_full_match_required():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="WITNESS",
        action="PARTICIPATE",
        effect="ALLOW",
    )

    assert (
        RuntimePolicyEvaluation.evaluate(
            policy=policy,
            resource_type="WITNESS",
            action="PARTICIPATE",
        )
        is True
    )
