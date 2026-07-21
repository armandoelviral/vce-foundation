from pathlib import Path

MODEL = Path(
    "research/specification_runtime/"
    "SPECIFICATION_RUNTIME_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_runtime_model_exists() -> None:
    assert MODEL.is_file()


def test_runtime_objects_exist() -> None:
    content = text()

    for item in (
        "Specification",
        "Claim",
        "Execution Result",
    ):
        assert item in content


def test_specification_definition() -> None:
    content = normalized()

    assert "Represents one executable Specification." in content

    for item in (
        "Identifier.",
        "Claims.",
        "Preserve Specification Identity.",
        "Contain executable Claims.",
        "Remain immutable during execution.",
    ):
        assert item in content


def test_claim_definition() -> None:
    content = normalized()

    assert "Represents one normative Claim." in content

    for item in (
        "Identifier.",
        "Statement.",
        "Executable Contract.",
        "Represent one normative requirement.",
        "Reference exactly one executable Contract.",
        "Remain immutable during execution.",
    ):
        assert item in content


def test_execution_result_definition() -> None:
    content = normalized()

    assert "Represents the execution outcome of one Specification." in content

    for item in (
        "Specification Identifier.",
        "Passed.",
        "Evidence.",
        "Decision.",
        "Collect execution evidence.",
        "Preserve execution result.",
        "Represent deterministic execution outcome.",
    ):
        assert item in content


def test_relationship_exists() -> None:
    content = text()

    for item in (
        "Specification",
        "Claim",
        "Execution Result",
    ):
        assert item in content


def test_runtime_invariants_exist() -> None:
    content = text()

    for invariant in (
        "Specification Identity Preservation",
        "Claim Identity Preservation",
        "Input Immutability",
        "Execution Determinism",
        "Verification Closure",
    ):
        assert invariant in content


def test_constraints_exist() -> None:
    content = normalized()

    assert (
        "A Specification shall contain one or more Claims."
        in content
    )

    assert (
        "Every Claim shall reference exactly one Executable Contract."
        in content
    )

    assert (
        "Execution Results shall reference exactly one Specification."
        in content
    )

    assert (
        "Execution Results shall be deterministic."
        in content
    )


def test_release_criteria_exist() -> None:
    content = normalized()

    assert "Release Criteria" in content

    for item in (
        "Runtime Model is completely defined",
        "Runtime Objects are explicitly specified",
        "Relationships are explicitly defined",
        "Runtime invariants are declared",
    ):
        assert item in content
