from pathlib import Path


MODEL = Path(
    "research/conformance/CONFORMANCE_EVIDENCE_MODEL.md"
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
    assert "objective result" in content


def test_model_declares_sources() -> None:
    content = text()

    for item in (
        "Executable Contract",
        "Runtime Test Suite",
        "Specification Test Suite",
    ):
        assert item in content


def test_model_declares_requirements() -> None:
    content = text()

    for item in (
        "Objective",
        "Executable",
        "Repeatable",
        "Deterministic",
    ):
        assert item in content


def test_model_declares_states() -> None:
    content = text()

    for item in (
        "Available",
        "Missing",
        "Invalid",
    ):
        assert item in content


def test_model_declares_outputs() -> None:
    content = text()

    assert "Evidence Status" in content
    assert "Evidence Source" in content
