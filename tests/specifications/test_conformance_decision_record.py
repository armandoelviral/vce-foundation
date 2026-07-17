from pathlib import Path


RECORD = Path(
    "research/conformance/CONFORMANCE_DECISION_RECORD.md"
)


def text() -> str:
    return RECORD.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_record_exists() -> None:
    assert RECORD.is_file()


def test_record_declares_purpose() -> None:
    content = normalized()

    assert "Conformance Evaluator" in content
    assert "Decision Record" in content


def test_record_declares_required_fields() -> None:
    content = normalized()

    for item in (
        "Normative Claim",
        "Capability",
        "Executable Contract",
        "Coverage Status",
        "Decision",
        "Failure Reason",
    ):
        assert item in content


def test_record_declares_decision_values() -> None:
    content = normalized()

    assert "Conformant." in content
    assert "Non-Conformant." in content


def test_record_declares_constraints() -> None:
    content = normalized()

    assert "exactly one Normative Claim." in content
    assert "exactly one Capability." in content
    assert "exactly one Decision." in content


def test_record_declares_output() -> None:
    assert "Decision Record." in normalized()
