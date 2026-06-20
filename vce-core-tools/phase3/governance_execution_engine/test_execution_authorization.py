from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_authorization import (
    ExecutionAuthorization,
)


def test_execution_authorized():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        ExecutionAuthorization.authorize(
            request=request,
            policy=policy,
        )
        is True
    )


def test_execution_denied_by_effect():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="DENY",
    )

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        ExecutionAuthorization.authorize(
            request=request,
            policy=policy,
        )
        is False
    )


def test_execution_denied_by_resource():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="ARTIFACT",
        action="EXECUTE",
        effect="ALLOW",
    )

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        ExecutionAuthorization.authorize(
            request=request,
            policy=policy,
        )
        is False
    )


def test_execution_denied_by_action():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="DELETE",
        effect="ALLOW",
    )

    request = ExecutionRequestRecord(
        request_id="request-001",
        resource_type="REPLAY",
        action="EXECUTE",
        subject="runtime-state-root",
    )

    assert (
        ExecutionAuthorization.authorize(
            request=request,
            policy=policy,
        )
        is False
    )
