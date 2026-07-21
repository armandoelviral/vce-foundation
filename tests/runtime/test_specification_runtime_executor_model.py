from pathlib import Path

MODEL = Path(
    "research/specification_runtime/"
    "SPECIFICATION_RUNTIME_EXECUTOR.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_definition_exists() -> None:
    content = normalized()

    assert (
        "evaluates one Specification"
        in content
    )

    assert (
        "Execution Results"
        in content
    )


def test_inputs_exist() -> None:
    content = text()

    for item in (
        "Specification.",
        "Execution Units.",
    ):
        assert item in content


def test_outputs_exist() -> None:
    content = text()

    for item in (
        "Execution Result.",
        "Evidence.",
        "Decision.",
    ):
        assert item in content


def test_responsibilities_exist() -> None:
    content = normalized()

    for item in (
        "Evaluate every Execution Unit.",
        "Collect execution Evidence.",
        "Produce deterministic Decisions.",
        "Produce one Execution Result.",
    ):
        assert item in content


def test_execution_flow_exists() -> None:
    content = text()

    for item in (
        "Specification",
        "Execution Units",
        "Evidence",
        "Execution Result",
    ):
        assert item in content


def test_runtime_invariants_exist() -> None:
    content = text()

    for invariant in (
        "Execution Determinism",
        "Evidence Completeness",
        "Verification Closure",
    ):
        assert invariant in content


def test_constraints_exist() -> None:
    content = normalized()

    assert (
        "Every Execution Unit shall be evaluated."
        in content
    )

    assert (
        "Execution order shall be deterministic."
        in content
    )

    assert (
        "Execution shall not modify the Specification."
        in content
    )


def test_release_criteria_exist() -> None:
    content = normalized()

    assert "Release Criteria" in content

    for item in (
        "Executor explicitly defined",
        "Execution flow defined",
        "Responsibilities defined",
        "Runtime invariants declared",
    ):
        assert item in content
