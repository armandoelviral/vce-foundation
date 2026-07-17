from pathlib import Path


ADR = Path(
    "research/adr/"
    "ADR-005_NORMATIVE_DRIVEN_PLATFORM_ARCHITECTURE.md"
)


LAYERS = (
    "Normative Documents",
    "Executable Contracts",
    "Domain Model",
    "Policies",
    "Evaluator",
    "Pipeline",
    "End-to-End Flow",
)


def text() -> str:
    return ADR.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_adr_exists() -> None:
    assert ADR.is_file()


def test_adr_is_accepted() -> None:
    assert "Status Accepted" in normalized()


def test_adr_declares_layered_architecture() -> None:
    content = text()

    for layer in LAYERS:
        assert layer in content


def test_adr_declares_rationale() -> None:
    assert "Rationale" in text()


def test_adr_declares_consequences() -> None:
    content = text()

    assert "Consequences" in content

    assert (
        "Future HAS platforms shall adopt"
        in content
    )
