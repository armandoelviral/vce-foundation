from pathlib import Path


MODEL = Path(
    "research/conformance/CONFORMANCE_DECISION_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_model_declares_purpose() -> None:
    content = text()

    assert "Purpose" in content
    assert "Conformance Decisions" in content


def test_model_declares_inputs() -> None:
    content = text()

    for item in (
        "Normative Claim",
        "Capability",
        "Executable Contract",
        "Coverage Status",
    ):
        assert item in content


def test_model_declares_decision_rules() -> None:
    content = text()

    assert "Conformant" in content
    assert "Non-Conformant" in content


def test_model_declares_failure_reasons() -> None:
    content = text()

    for item in (
        "Missing Claim",
        "Missing Capability",
        "Missing Contract",
        "Not Covered",
        "Undefined Input",
    ):
        assert item in content


def test_model_declares_outputs() -> None:
    content = text()

    assert "Conformance Decision" in content
    assert "Failure Reason" in content
