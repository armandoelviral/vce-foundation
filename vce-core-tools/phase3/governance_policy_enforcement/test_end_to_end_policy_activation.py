from phase3.governance_policy_enforcement.policy_activation_evaluation import (
    PolicyActivationEvaluation,
)

from phase3.governance_policy_enforcement.policy_activation_decision import (
    PolicyActivationDecision,
)

from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_registry import (
    PolicyActivationRegistry,
)

from phase3.governance_policy_enforcement.policy_activation_query import (
    PolicyActivationQuery,
)

from phase3.governance_policy_enforcement.policy_activation_report import (
    PolicyActivationReport,
)

from phase3.governance_policy_enforcement.policy_activation_attestation import (
    PolicyActivationAttestation,
)


def test_end_to_end_policy_activation():

    evaluation = (
        PolicyActivationEvaluation.evaluate(
            "APPROVED"
        )
    )

    assert evaluation is True

    decision = (
        PolicyActivationDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "ACTIVATE_POLICY"
    )

    activation = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    registry = PolicyActivationRegistry()

    registry.add(
        activation
    )

    query = PolicyActivationQuery(
        registry
    )

    recovered = query.by_id(
        "activation-001"
    )

    assert recovered == activation

    report = PolicyActivationReport(
        {
            "activation-001":
                recovered
        }
    )

    assert report.activation_count() == 1

    assert report.activation_ids() == [
        "activation-001"
    ]

    attestation = (
        PolicyActivationAttestation.attest(
            attestation_id="att-001",
            activation=activation,
        )
    )

    assert (
        attestation.subject
        == "policy_activation"
    )

    assert (
        attestation.evidence_hash
        == "activation-001"
    )
