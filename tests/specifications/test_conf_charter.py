from pathlib import Path


CHARTER = Path(
    "research/conformance/CONF_CHARTER.md"
)


def charter() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def test_charter_exists() -> None:
    assert CHARTER.is_file()


def test_charter_defines_mission() -> None:
    text = charter()

    assert "Mission" in text
    assert "Normative Claim" in text
    assert "HAS Runtime" in text


def test_charter_defines_scope() -> None:
    text = charter()

    assert "Scope" in text
    assert "does not define specifications" in text
    assert "does not implement runtime behavior" in text


def test_charter_defines_inputs() -> None:
    text = charter()

    required = (
        "Specification Platform",
        "Traceability Registry",
        "Executable Contracts",
        "Runtime Test Suite",
    )

    for item in required:
        assert item in text


def test_charter_defines_outputs() -> None:
    text = charter()

    required = (
        "Conformance Report",
        "Coverage Metrics",
        "Evidence Registry",
    )

    for item in required:
        assert item in text


def test_charter_defines_success_criteria() -> None:
    text = charter()

    assert "Success Criteria" in text
    assert "Executable Evidence" in text
    assert "overall Conformance" in text
