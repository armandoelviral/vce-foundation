from pathlib import Path


SPECIFICATION = Path(
    "research/specifications/runtime_specification.md"
)


def specification_text() -> str:
    return SPECIFICATION.read_text(
        encoding="utf-8",
    )


def test_runtime_specification_exists() -> None:
    assert SPECIFICATION.exists()


def test_contains_knowledge_states() -> None:
    text = specification_text()

    assert "Knowledge States" in text

    assert "Observation" in text
    assert "Hypothesis" in text
    assert "Candidate Principle" in text
    assert "Principle" in text


def test_contains_allowed_transitions() -> None:
    text = specification_text()

    assert "Allowed Transitions" in text

    assert "Observation" in text
    assert "Hypothesis" in text
    assert "Candidate Principle" in text
    assert "Principle" in text


def test_contains_guaranteed_properties() -> None:
    text = specification_text()

    assert "Guaranteed Properties" in text

    assert "Replay Determinism" in text
    assert "History Integrity" in text
    assert "Verification Closure" in text
    assert "Pipeline Closure" in text
    assert "State Monotonicity" in text
