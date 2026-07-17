from has.conformance.conformance_pipeline import (
    ConformancePipeline,
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


def test_end_to_end_conformance_flow() -> None:
    pipeline = ConformancePipeline()

    conformance_input = ConformanceInput(
        claim="GP-001",
        capability="Replay Determinism",
        executable_contract=(
            "tests/runtime/invariants/"
            "test_invariant_replay_determinism.py"
        ),
        coverage_status="Covered",
    )

    evidence = Evidence(
        source="runtime-suite",
        status="Available",
    )

    result = pipeline.evaluate(
        conformance_input,
        evidence,
    )

    assert isinstance(
        result,
        DecisionRecord,
    )

    assert result.decision is Decision.CONFORMANT

    assert result.claim == "GP-001"

    assert (
        result.capability
        == "Replay Determinism"
    )

    assert (
        result.coverage_status
        == "Covered"
    )

    assert result.evidence.available
