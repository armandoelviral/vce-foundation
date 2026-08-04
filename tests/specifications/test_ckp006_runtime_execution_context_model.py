"""
Executable Specification

CKP-006.4
Commerce Runtime Execution Context Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_EXECUTION_CONTEXT_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Execution Context Identity",
    "## Execution Context Version",
    "## Execution Context Lifecycle",
    "## Execution Context Scope",
    "## Execution Context Baselines",
    "## Execution Context Registries",
    "## Execution Context Configuration",
    "## Execution Context Limits",
    "## Execution Context Environment",
    "## Execution Context Compatibility",
    "## Execution Context Validation",
    "## Execution Context Integrity",
    "## Execution Context Traceability",
    "## Execution Context Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Execution Context Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Validated.",
    "Admitted.",
    "Active.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

FAILURE_CLASSIFICATIONS = (
    "CONTEXT_IDENTITY_VIOLATION.",
    "CONTEXT_VERSION_VIOLATION.",
    "CONTEXT_BASELINE_VIOLATION.",
    "CONTEXT_REGISTRY_VIOLATION.",
    "CONTEXT_CONFIGURATION_VIOLATION.",
    "CONTEXT_LIMITS_VIOLATION.",
    "CONTEXT_ENVIRONMENT_VIOLATION.",
    "CONTEXT_COMPATIBILITY_VIOLATION.",
    "CONTEXT_VALIDATION_VIOLATION.",
    "CONTEXT_INTEGRITY_VIOLATION.",
    "CONTEXT_RELATIONSHIP_VIOLATION.",
    "CONTEXT_SERIALIZATION_VIOLATION.",
    "CONTEXT_ORDERING_VIOLATION.",
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


def test_document_identity() -> None:
    content = normalized_text()

    assert "# CKP-006" in content
    assert "Title Commerce Runtime Execution Context Model" in content
    assert "Abbreviation CRECM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    hs = headings()

    for section in EXPECTED_SECTIONS:
        assert hs.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    hs = headings()

    indexes = [
        hs.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert indexes == sorted(indexes)


def test_no_duplicate_sections() -> None:
    hs = headings()

    assert len(hs) == len(set(hs))


def test_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content


def test_normative_dependencies() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary.",
        "CKP-002 Commerce Ontology.",
        "CKP-003 Commerce Knowledge Graph.",
        "CKP-004 Commerce Query Language.",
        "CKP-005 Baseline 1.0.",
        "CKP-005 Specification Freeze.",
        "CKP-006.1 Commerce Reasoning Runtime Charter.",
        "CKP-006.2 Runtime Structure Model.",
        "CKP-006.3 Runtime Execution Request Model.",
    ):
        assert dependency in content


def test_context_identity() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution Context shall possess "
        "exactly one immutable Execution Context Identifier."
    ) in content

    assert "CKP-RUNTIME-CONTEXT-000001" in content

    assert (
        "Execution Context Identity shall be globally unique."
    ) in content


def test_context_validation_is_fail_closed() -> None:
    content = normalized_text()

    assert "Validation shall fail closed." in content


def test_context_integrity() -> None:
    content = normalized_text()

    for item in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Baselines.",
        "Registries.",
        "Configuration.",
        "Limits.",
        "Environment.",
        "Relationships.",
        "Serialization.",
        "Ordering.",
    ):
        assert item in content

    assert "Mutation shall invalidate Integrity." in content


def test_failure_classifications() -> None:
    content = normalized_text()

    for item in FAILURE_CLASSIFICATIONS:
        assert item in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify baselines.",
        "Modify registries.",
        "Modify Runtime Configuration.",
        "Modify Runtime Limits.",
        "Modify Execution Request.",
        "Modify Runtime Execution.",
        "Modify Validation Results.",
        "Modify Replay artifacts.",
        "Modify Certification artifacts.",
        "Modify CKP-005 Baseline.",
        "Repair invalid context.",
        "Invent missing runtime state.",
    ):
        assert prohibition in content


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-006.5" in content
    assert "Runtime State Model." in content


def test_end_marker() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
