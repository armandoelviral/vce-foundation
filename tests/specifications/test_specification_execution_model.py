from pathlib import Path

MODEL = Path(
    "research/specification_runtime/"
    "SPECIFICATION_EXECUTION_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_execution_pipeline_exists() -> None:
    content = text()

    for item in (
        "Specification",
        "Section",
        "Claim",
        "Evaluation Unit",
        "Evidence",
        "Decision",
        "Execution Result",
    ):
        assert item in content


def test_execution_unit_definition() -> None:
    content = normalized()

    assert "smallest executable component" in content
    assert "reference exactly one Claim" in content
    assert "produce Evidence" in content
    assert "deterministic Result" in content


def test_evaluation_rules() -> None:
    content = normalized()

    assert "evaluated independently" in content
    assert "Evaluation order shall be deterministic" in content
    assert "shall not modify the Specification" in content


def test_evidence_rules() -> None:
    content = normalized()

    assert "Evidence shall be objective" in content
    assert "Evidence shall be reproducible" in content
    assert "attached to exactly one Execution Unit" in content


def test_decision_boundary() -> None:
    content = normalized()

    assert "Conformance Platform" in content
    assert "shall not perform policy interpretation" in content


def test_invariants_exist() -> None:
    content = text()

    for invariant in (
        "Specification Identity Preservation",
        "Claim Identity Preservation",
        "Execution Determinism",
        "Evidence Completeness",
        "Verification Closure",
    ):
        assert invariant in content


def test_release_criteria_exist() -> None:
    content = text()

    assert "Release Criteria" in content
    assert "Execution Unit" in content
    assert "Decision boundary" in content
