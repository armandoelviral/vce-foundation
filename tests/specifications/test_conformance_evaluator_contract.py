from pathlib import Path


CONTRACT = Path(
    "research/conformance/CONFORMANCE_EVALUATOR_CONTRACT.md"
)


def text() -> str:
    return CONTRACT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        text().split()
    )


def test_contract_exists() -> None:
    assert CONTRACT.is_file()


def test_contract_declares_purpose() -> None:
    content = text()

    assert "Purpose" in content
    assert "Conformance Evaluator" in content


def test_contract_declares_inputs() -> None:
    content = text()

    for item in (
        "Validated Conformance Input",
        "Decision Model",
        "Evidence Model",
    ):
        assert item in content


def test_contract_declares_responsibilities() -> None:
    content = text()

    for item in (
        "Validate Inputs",
        "Evaluate Evidence",
        "Apply Decision Rules",
        "Produce Conformance Decision",
    ):
        assert item in content


def test_contract_declares_outputs() -> None:
    content = text()

    for item in (
        "Conformance Decision",
        "Failure Reason",
        "Evidence Summary",
    ):
        assert item in content


def test_contract_declares_constraints() -> None:
    content = normalized_text()

    assert (
        "The Evaluator shall be deterministic."
        in content
    )

    assert (
        "The Evaluator shall not modify its inputs."
        in content
    )

    assert (
        "The Evaluator shall produce the same "
        "decision for identical inputs."
        in content
    )
