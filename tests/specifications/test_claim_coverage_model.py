from pathlib import Path


MODEL = Path(
    "research/conformance/CLAIM_COVERAGE_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_model_declares_purpose() -> None:
    model = text()

    assert "Purpose" in model
    assert "Claim Coverage" in model


def test_model_declares_covered() -> None:
    model = text()

    assert "Covered" in model
    assert "Capability" in model


def test_model_declares_not_covered() -> None:
    assert "Not Covered" in text()


def test_model_declares_outputs() -> None:
    model = text()

    for item in (
        "Claim Coverage Percentage",
        "Covered Claims",
        "Missing Claims",
    ):
        assert item in model
