from pathlib import Path


CONTRACT = Path(
    "research/conformance/CONFORMANCE_INPUT_CONTRACT.md"
)


def text() -> str:
    return CONTRACT.read_text(
        encoding="utf-8",
    )


def test_contract_exists() -> None:
    assert CONTRACT.is_file()


def test_contract_declares_purpose() -> None:
    content = text()

    assert "Purpose" in content
    assert "Conformance Engine" in content


def test_contract_declares_required_inputs() -> None:
    content = text()

    required = (
        "Normative Claim",
        "Capability",
        "Executable Contract",
        "Coverage Status",
    )

    for item in required:
        assert item in content


def test_contract_declares_validation_rules() -> None:
    content = text()

    assert "Validation Rules" in content
    assert "Covered" in content
    assert "Not Covered" in content


def test_contract_declares_failure_conditions() -> None:
    content = text()

    required = (
        "Missing Claim",
        "Missing Capability",
        "Missing Contract",
        "Undefined Coverage Status",
    )

    for item in required:
        assert item in content


def test_contract_declares_outputs() -> None:
    content = text()

    assert "Conformance Decision" in content
    assert "Failure Reason" in content
