from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)

from phase3.governance_execution_engine.execution_request_registry import (
    ExecutionRequestRegistry,
)

from phase3.governance_execution_engine.execution_query import (
    ExecutionQuery,
)

from phase3.governance_execution_engine.execution_authorization import (
    ExecutionAuthorization,
)

from phase3.governance_execution_engine.execution_decision import (
    ExecutionDecision,
)

from phase3.governance_execution_engine.execution_report import (
    ExecutionReport,
)

from phase3.governance_execution_engine.execution_attestation import (
    ExecutionAttestation,
)


def test_end_to_end_governance_execution():

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

    registry = ExecutionRequestRegistry()

    registry.add(request)

    query = ExecutionQuery(registry)

    recovered = query.by_id(
        "request-001"
    )

    assert recovered == request

    authorized = (
        ExecutionAuthorization.authorize(
            request=recovered,
            policy=policy,
        )
    )

    assert authorized is True

    decision = (
        ExecutionDecision.from_authorization(
            authorized
        )
    )

    assert (
        decision.status
        == "EXECUTE_ACTION"
    )

    report = ExecutionReport(
        {
            "request-001":
                recovered
        }
    )

    assert report.request_count() == 1

    assert report.request_ids() == [
        "request-001"
    ]

    attestation = (
        ExecutionAttestation.attest(
            attestation_id="att-001",
            request=request,
        )
    )

    assert (
        attestation.subject
        == "governance_execution"
    )

    assert (
        attestation.evidence_hash
        == "request-001"
    )

