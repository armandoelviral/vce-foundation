from pathlib import Path


MODEL = Path(
    "research/conformance/COVERAGE_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_model_declares_purpose() -> None:
    assert "Purpose" in text()
    assert "Coverage" in text()


def test_model_declares_covered() -> None:
    assert "Covered" in text()
    assert "Executable Contract" in text()


def test_model_declares_not_covered() -> None:
    assert "Not Covered" in text()


def test_model_declares_output() -> None:
    model = text()

    for item in (
        "Coverage Percentage",
        "Covered Capabilities",
        "Missing Claims",
        "Missing Contracts",
    ):
        assert item in model
