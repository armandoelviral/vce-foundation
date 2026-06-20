from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_registry import (
    RuntimePolicyRegistry,
)

from phase3.runtime_policy_enforcement.runtime_policy_query import (
    RuntimePolicyQuery,
)

from phase3.runtime_policy_enforcement.runtime_policy_evaluation import (
    RuntimePolicyEvaluation,
)

from phase3.runtime_policy_enforcement.runtime_policy_decision import (
    RuntimePolicyDecision,
)

from phase3.runtime_policy_enforcement.runtime_policy_report import (
    RuntimePolicyReport,
)

from phase3.runtime_policy_enforcement.runtime_policy_attestation import (
    RuntimePolicyAttestation,
)


def test_end_to_end_runtime_policy_enforcement():

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    registry = RuntimePolicyRegistry()

    registry.add(
        policy
    )

    query = RuntimePolicyQuery(
        registry
    )

    recovered = query.by_id(
        "policy-001"
    )

    assert recovered == policy

    evaluation = (
        RuntimePolicyEvaluation.evaluate(
            policy=recovered,
            resource_type="REPLAY",
            action="EXECUTE",
        )
    )

    assert evaluation is True

    decision = (
        RuntimePolicyDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "ALLOW_REQUEST"
    )

    report = RuntimePolicyReport(
        {
            "policy-001":
                recovered
        }
    )

    assert report.policy_count() == 1

    assert report.policy_ids() == [
        "policy-001"
    ]

    attestation = (
        RuntimePolicyAttestation.attest(
            attestation_id="att-001",
            policy=policy,
        )
    )

    assert (
        attestation.subject
        == "runtime_policy"
    )

    assert (
        attestation.evidence_hash
        == "policy-001"
    )
