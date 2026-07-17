from has.conformance.conformance_pipeline import (
    ConformancePipeline,
)
from has.conformance.decision_evaluator import (
    ConformanceDecisionEvaluator,
)
from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import (
    Decision,
)
from has.conformance.model.decision_record import (
    DecisionRecord,
)
from has.conformance.model.evidence import (
    Evidence,
)


def covered_input() -> ConformanceInput:
    return ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract=(
            "tests/runtime/invariants/"
            "test_invariant_replay_determinism.py"
        ),
        coverage_status="Covered",
    )


def uncovered_input() -> ConformanceInput:
    return ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract=(
            "tests/runtime/invariants/"
            "test_invariant_replay_determinism.py"
        ),
        coverage_status="Not Covered",
    )


def available_evidence() -> Evidence:
    return Evidence(
        source="runtime-invariant-gate",
        status="Available",
    )


def missing_evidence() -> Evidence:
    return Evidence(
        source="runtime-invariant-gate",
        status="Missing",
    )


class RecordingEvaluator(ConformanceDecisionEvaluator):
    def __init__(self) -> None:
        super().__init__()

        self.calls = 0

    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> DecisionRecord:
        self.calls += 1

        return super().evaluate(
            conformance_input,
            evidence,
        )


def test_pipeline_returns_decision_record() -> None:
    result = ConformancePipeline().evaluate(
        covered_input(),
        available_evidence(),
    )

    assert isinstance(
        result,
        DecisionRecord,
    )

    assert result.decision is Decision.CONFORMANT


def test_pipeline_produces_non_conformant_record() -> None:
    result = ConformancePipeline().evaluate(
        uncovered_input(),
        available_evidence(),
    )

    assert result.decision is Decision.NON_CONFORMANT
    assert result.failure_reason == "non_conformant"


def test_pipeline_rejects_missing_evidence_through_evaluator() -> None:
    result = ConformancePipeline().evaluate(
        covered_input(),
        missing_evidence(),
    )

    assert result.decision is Decision.NON_CONFORMANT
    assert result.failure_reason == "non_conformant"


def test_pipeline_preserves_traceability_fields() -> None:
    source = covered_input()

    result = ConformancePipeline().evaluate(
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


def test_pipeline_delegates_to_injected_evaluator() -> None:
    evaluator = RecordingEvaluator()

    pipeline = ConformancePipeline(
        evaluator=evaluator,
    )

    pipeline.evaluate(
        covered_input(),
        available_evidence(),
    )

    assert evaluator.calls == 1


def test_pipeline_is_deterministic() -> None:
    pipeline = ConformancePipeline()

    first = pipeline.evaluate(
        covered_input(),
        available_evidence(),
    )

    second = pipeline.evaluate(
        covered_input(),
        available_evidence(),
    )

    assert first == second


def test_pipeline_does_not_modify_inputs() -> None:
    conformance_input = covered_input()
    evidence = available_evidence()

    before_input = conformance_input
    before_evidence = evidence

    ConformancePipeline().evaluate(
        conformance_input,
        evidence,
    )

    assert conformance_input == before_input
    assert evidence == before_evidence
