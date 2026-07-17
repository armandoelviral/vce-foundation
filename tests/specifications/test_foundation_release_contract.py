from pathlib import Path


CONTRACT = Path(
    "research/releases/"
    "HAS_FOUNDATION_1_0_RELEASE_CONTRACT.md"
)

REQUIRED_PLATFORMS = (
    "Runtime",
    "Executable Knowledge Infrastructure",
    "Specification Platform",
    "Conformance Platform",
)

REQUIRED_PROPERTIES = (
    "Stable API.",
    "Stable Domain Model.",
    "Executable Specifications.",
    "Executable Contracts.",
    "Deterministic Runtime.",
    "Deterministic Conformance.",
)

RELEASE_CRITERIA = (
    "All mandatory executable contracts pass.",
    "All architectural invariants pass.",
    "No open foundational milestones remain.",
)


def contract_text() -> str:
    return CONTRACT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        contract_text().split()
    )


def test_release_contract_exists() -> None:
    assert CONTRACT.is_file()


def test_release_contract_status_is_frozen() -> None:
    content = normalized_text()

    assert "Status Frozen" in content


def test_release_contract_declares_required_platforms() -> None:
    content = contract_text()

    assert "Required Platforms" in content

    for platform in REQUIRED_PLATFORMS:
        assert platform in content


def test_release_contract_declares_required_properties() -> None:
    content = contract_text()

    assert "Required Properties" in content

    for property_name in REQUIRED_PROPERTIES:
        assert property_name in content


def test_release_contract_declares_release_criteria() -> None:
    content = normalized_text()

    assert "Release Criteria" in content

    for criterion in RELEASE_CRITERIA:
        assert criterion in content


def test_release_contract_declares_release_output() -> None:
    content = normalized_text()

    assert "HAS Foundation 1.0" in content
    assert "Eligible for Release." in content
