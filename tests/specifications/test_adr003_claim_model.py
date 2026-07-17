from pathlib import Path


ADR = Path(
    "research/adr/ADR-003_CLAIMS_BASED_SPECIFICATION_MODEL.md"
)


def adr_text() -> str:
    return ADR.read_text(
        encoding="utf-8",
    )


def test_adr_exists() -> None:
    assert ADR.is_file()


def test_defines_claim_as_primary_unit() -> None:
    text = adr_text()

    assert "Claim" in text
    assert "Executable Contract" in text
    assert "Conformance" in text


def test_defines_traceability() -> None:
    text = adr_text()

    assert "Traceability" in text
    assert "Implementation" in text
