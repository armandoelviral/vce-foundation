"""
Executable Specification

CKP-006.3
Commerce Runtime Execution Request Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_EXECUTION_REQUEST_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Execution Request Identity",
    "## Execution Request Version",
    "## Execution Request Lifecycle",
    "## Execution Request Status",
    "## Execution Request Scope",
    "## Execution Request Context",
    "## Execution Request Inputs",
    "## Execution Request Constraints",
    "## Execution Request Preconditions",
    "## Execution Request Admission",
    "## Execution Request Validation",
    "## Execution Request Integrity",
    "## Execution Request Traceability",
    "## Execution Request Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Execution Request Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Validated.",
    "Admitted.",
    "Executing.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

STATUS_VALUES = (
    "CREATED.",
    "VALIDATED.",
    "ADMITTED.",
    "EXECUTING.",
    "COMPLETED.",
    "FAILED.",
    "CANCELLED.",
)

FAILURE_CLASSIFICATIONS = (
    "REQUEST_IDENTITY_VIOLATION.",
    "REQUEST_VERSION_VIOLATION.",
    "REQUEST_CONTEXT_VIOLATION.",
    "REQUEST_INPUT_VIOLATION.",
    "REQUEST_CONSTRAINT_VIOLATION.",
    "REQUEST_PRECONDITION_VIOLATION.",
    "REQUEST_ADMISSION_VIOLATION.",
    "REQUEST_VALIDATION_VIOLATION.",
    "REQUEST_INTEGRITY_VIOLATION.",
    "REQUEST_RELATIONSHIP_VIOLATION.",
    "REQUEST_SERIALIZATION_VIOLATION.",
    "REQUEST_ORDERING_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def headings() -> list[str]:
    return [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_identity() -> None:
    content = normalized_text()

    assert "# CKP-006" in content
    assert "Title Commerce Runtime Execution Request Model" in content
    assert "Abbreviation CRERM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    hs = headings()

    for section in EXPECTED_SECTIONS:
        assert hs.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    hs = headings()

    positions = [
        hs.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_no_duplicate_sections() -> None:
    hs = headings()

    assert len(hs) == len(set(hs))


def test_lifecycle_states() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content


def test_status_values() -> None:
    content = normalized_text()

    for status in STATUS_VALUES:
        assert status in content

    assert "Exactly one status shall exist at any time." in content


def test_dependencies() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary.",
        "CKP-002 Commerce Ontology.",
        "CKP-003 Commerce Knowledge Graph.",
        "CKP-004 Commerce Query Language.",
        "CKP-005 Baseline 1.0.",
        "CKP-005.3 Reasoning Request Model.",
        "CKP-005 Specification Freeze.",
        "CKP-006.1 Commerce Reasoning Runtime Charter.",
        "CKP-006.2 Runtime Structure Model.",
    ):
        assert dependency in content


def test_identity_rules() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution Request shall possess "
        "exactly one immutable Execution Request Identifier."
    ) in content

    assert "CKP-RUNTIME-REQUEST-000001" in content

    assert (
        "Execution Request Identity shall be globally unique."
    ) in content


def test_validation_is_fail_closed() -> None:
    content = normalized_text()

    assert "Validation shall fail closed." in content


def test_integrity() -> None:
    content = normalized_text()

    for field in (
        "Identity.",
        "Version.",
        "Context.",
        "Inputs.",
        "Constraints.",
        "Relationships.",
        "Lifecycle.",
        "Status.",
        "Serialization.",
        "Ordering.",
    ):
        assert field in content

    assert "Mutation shall invalidate Integrity." in content


def test_failure_classifications() -> None:
    content = normalized_text()

    for item in FAILURE_CLASSIFICATIONS:
        assert item in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify the Reasoning Request.",
        "Modify Facts.",
        "Modify Premises.",
        "Modify Rules.",
        "Modify Constraints.",
        "Modify Execution Context.",
        "Modify Runtime Configuration.",
        "Modify Runtime Limits.",
        "Modify CKP-005 Baseline.",
        "Modify admitted inputs.",
        "Repair invalid requests.",
        "Invent missing inputs.",
    ):
        assert prohibition in content


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-006.4" in content
    assert "Runtime Execution Context Model." in content


def test_end_marker() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
