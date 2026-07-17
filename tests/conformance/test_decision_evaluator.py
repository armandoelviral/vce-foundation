from has.conformance.decision_evaluator import (
    ConformanceDecisionEvaluator,
)
from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import Decision
from has.conformance.model.evidence import Evidence
from has.conformance.policies.decision_policy import (
    DecisionPolicy,
)


def covered_input() -> ConformanceInput:
    return ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract="contract.py",
        coverage_status="Covered",
    )


def uncovered_input() -> ConformanceInput:
    return ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract="contract.py",
        coverage_status="Not Covered",
    )


def available_evidence() -> Evidence:
    return Evidence(
        source="runtime",
        status="Available",
    )


def missing_evidence() -> Evidence:
    return Evidence(
        source="runtime",
        status="Missing",
    )


class AlwaysNonConformantPolicy(DecisionPolicy):
    def __init__(self) -> None:
        self.calls = 0

    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> Decision:
        self.calls += 1

        return Decision.NON_CONFORMANT


def test_default_policy_produces_conformant_decision() -> None:
    result = ConformanceDecisionEvaluator().evaluate(
        covered_input(),
        available_evidence(),
    )

    assert result.decision is Decision.CONFORMANT
    assert result.conformant
    assert result.failure_reason is None


def test_default_policy_rejects_missing_evidence() -> None:
    result = ConformanceDecisionEvaluator().evaluate(
        covered_input(),
        missing_evidence(),
    )

    assert result.decision is Decision.NON_CONFORMANT
    assert not result.conformant
    assert result.failure_reason == "non_conformant"


def test_default_policy_rejects_uncovered_input() -> None:
    result = ConformanceDecisionEvaluator().evaluate(
        uncovered_input(),
        available_evidence(),
    )

    assert result.decision is Decision.NON_CONFORMANT
    assert result.failure_reason == "non_conformant"


def test_evaluator_delegates_to_injected_policy() -> None:
    policy = AlwaysNonConformantPolicy()

    result = ConformanceDecisionEvaluator(
        policy=policy,
    ).evaluate(
        covered_input(),
        available_evidence(),
    )

    assert policy.calls == 1
    assert result.decision is Decision.NON_CONFORMANT


def test_evaluator_preserves_traceability_fields() -> None:
    source = covered_input()

    result = ConformanceDecisionEvaluator().evaluate(
        source,
        available_evidence(),
    )

    assert result.claim == source.claim
    assert result.capability == source.capability

    assert (
        result.executable_contract
        == source.executable_contract
    )

    assert (
        result.coverage_status
        == source.coverage_status
    )


def test_evaluator_is_deterministic() -> None:
    evaluator = ConformanceDecisionEvaluator()

    first = evaluator.evaluate(
        covered_input(),
        available_evidence(),
    )

    second = evaluator.evaluate(
        covered_input(),
        available_evidence(),
    )

    assert first == second


def test_evaluator_does_not_modify_inputs() -> None:
    conformance_input = covered_input()
    evidence = available_evidence()

    before_input = conformance_input
    before_evidence = evidence

    ConformanceDecisionEvaluator().evaluate(
        conformance_input,
        evidence,
    )

    assert conformance_input == before_input
    assert evidence == before_evidence
