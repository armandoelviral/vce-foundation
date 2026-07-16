from pathlib import Path

from has.runtime.knowledge_state import (
    KnowledgeState,
)


SPECIFICATION = Path(
    "research/specifications/runtime_specification.md"
)


def specification() -> str:
    return SPECIFICATION.read_text(
        encoding="utf-8",
    )


def test_runtime_states_conform_to_specification() -> None:

    text = specification()

    expected = (
        "Observation",
        "Hypothesis",
        "Candidate Principle",
        "Principle",
    )

    for state in expected:
        assert state in text

    implementation = {
        state.value
        for state in KnowledgeState
    }

    assert implementation == {
        "observation",
        "hypothesis",
        "candidate_principle",
        "principle",
    }
