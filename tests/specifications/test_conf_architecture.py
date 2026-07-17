from pathlib import Path


MODEL = Path("src/has/conformance/model")
POLICIES = Path("src/has/conformance/policies")

PIPELINE = Path(
    "src/has/conformance/conformance_pipeline.py"
)

EVALUATOR = Path(
    "src/has/conformance/decision_evaluator.py"
)


def read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
    )


def test_domain_has_no_pipeline_dependency() -> None:
    for file in MODEL.glob("*.py"):
        assert "conformance_pipeline" not in read(file)


def test_domain_has_no_evaluator_dependency() -> None:
    for file in MODEL.glob("*.py"):
        assert "decision_evaluator" not in read(file)


def test_policies_have_no_pipeline_dependency() -> None:
    for file in POLICIES.glob("*.py"):
        assert "conformance_pipeline" not in read(file)


def test_pipeline_has_no_runtime_dependency() -> None:
    text = read(PIPELINE)

    assert "has.runtime" not in text


def test_pipeline_has_no_specification_dependency() -> None:
    text = read(PIPELINE)

    assert "research." not in text
    assert "specification" not in text.lower()


def test_evaluator_has_no_runtime_dependency() -> None:
    text = read(EVALUATOR)

    assert "has.runtime" not in text


def test_evaluator_has_no_specification_dependency() -> None:
    text = read(EVALUATOR)

    assert "research." not in text
