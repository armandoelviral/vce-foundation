from pathlib import Path


CHARTER = Path(
    "research/specification_runtime/"
    "SR-001_SPECIFICATION_RUNTIME_CHARTER.md"
)

REQUIRED_INPUTS = (
    "Validated Specification",
    "Specification Identifier",
    "Normative Claims",
    "Executable Contract References",
    "Execution Context",
)

REQUIRED_OUTPUTS = (
    "Specification Execution Result",
    "Claim Evaluation Results",
    "Evidence Records",
    "Conformance Decision Records",
    "Failure Reasons",
)

REQUIRED_INVARIANTS = (
    "Specification Identity Preservation",
    "Claim Identity Preservation",
    "Input Immutability",
    "Execution Determinism",
    "Evidence Completeness",
    "Verification Closure",
    "Conformance Delegation",
)

REQUIRED_NON_GOALS = (
    "interpret unrestricted natural language",
    "infer Claims from undocumented intent",
    "generate Specifications",
    "modify HAS Foundation",
    "define domain-specific Retail semantics",
    "replace the Conformance Platform",
)


def charter_text() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        charter_text().split()
    )


def test_sr001_charter_exists() -> None:
    assert CHARTER.is_file()


def test_sr001_declares_purpose_and_mission() -> None:
    content = normalized_text()

    assert "Purpose" in content
    assert "Mission" in content

    assert (
        "executes explicitly represented Specifications "
        "as first-class runtime objects"
    ) in content

    assert (
        "produce verifiable conformance results"
    ) in content


def test_sr001_declares_required_inputs() -> None:
    content = charter_text()

    assert "Inputs" in content

    for item in REQUIRED_INPUTS:
        assert item in content


def test_sr001_declares_required_outputs() -> None:
    content = charter_text()

    assert "Outputs" in content

    for item in REQUIRED_OUTPUTS:
        assert item in content


def test_sr001_declares_runtime_responsibilities() -> None:
    content = normalized_text()

    required = (
        "Preserve Specification identity.",
        "Preserve Claim identity.",
        "Execute only explicitly bound Contracts.",
        "Produce repeatable Results.",
        "Produce Evidence for every evaluated Claim.",
        "Reject unresolved or invalid execution units.",
    )

    for item in required:
        assert item in content


def test_sr001_declares_non_goals() -> None:
    content = normalized_text()

    assert "Non-Goals" in content

    for item in REQUIRED_NON_GOALS:
        assert item in content


def test_sr001_declares_runtime_invariants() -> None:
    content = charter_text()

    assert "Runtime Invariants" in content

    for invariant in REQUIRED_INVARIANTS:
        assert invariant in content


def test_sr001_preserves_foundation_boundary() -> None:
    content = normalized_text()

    assert "HAS Foundation 1.0 LTS" in content

    assert (
        "shall not modify the frozen behavior "
        "or normative contracts of Foundation 1.0"
    ) in content


def test_sr001_preserves_retail_boundary() -> None:
    content = normalized_text()

    assert (
        "The Specification Runtime is domain-neutral."
    ) in content

    assert (
        "Retail-specific vocabulary, ontology, "
        "constraints, and decisions remain outside "
        "the scope of SR-001."
    ) in content


def test_sr001_declares_release_criteria() -> None:
    content = normalized_text()

    assert "Release Criteria" in content
    assert "the complete Foundation suite remains green" in content


def test_sr001_declares_next_deliverable() -> None:
    content = normalized_text()

    assert "SR-002" in content
    assert "Specification Execution Model" in content
