from pathlib import Path

MODEL = Path(
    "research/specification_runtime/"
    "EXECUTION_UNIT_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_definition_exists() -> None:
    content = normalized()

    assert (
        "An Execution Unit represents one executable Claim."
        in content
    )

    assert (
        "one Executable Contract"
        in content
    )


def test_properties_exist() -> None:
    content = text()

    for item in (
        "Claim.",
        "Executable Contract.",
    ):
        assert item in content


def test_responsibilities_exist() -> None:
    content = normalized()

    for item in (
        "Execute one Claim.",
        "Produce deterministic Evidence.",
        "Produce one deterministic Decision.",
        "Remain immutable during execution.",
    ):
        assert item in content


def test_relationship_exists() -> None:
    content = text()

    for item in (
        "Specification",
        "Claim",
        "Execution Unit",
        "Execution Result",
    ):
        assert item in content


def test_runtime_invariants_exist() -> None:
    content = text()

    for invariant in (
        "Claim Identity Preservation",
        "Execution Determinism",
        "Evidence Completeness",
        "Verification Closure",
    ):
        assert invariant in content


def test_constraints_exist() -> None:
    content = normalized()

    assert (
        "Every Execution Unit shall reference exactly one Claim."
        in content
    )

    assert (
        "Every Execution Unit shall reference exactly one Executable Contract."
        in content
    )

    assert (
        "Execution Units shall execute independently."
        in content
    )

    assert (
        "Execution Units shall not modify the Specification."
        in content
    )


def test_release_criteria_exist() -> None:
    content = normalized()

    assert "Release Criteria" in content

    for item in (
        "Execution Unit is explicitly defined",
        "Responsibilities are explicitly defined",
        "Relationships are explicitly defined",
        "Runtime invariants are declared",
    ):
        assert item in content

