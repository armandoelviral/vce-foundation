from pathlib import Path


CHARTER = Path(
    "research/commerce/query_language/"
    "CKP004_COMMERCE_QUERY_LANGUAGE_CHARTER.md"
)

INITIAL_QUERY_CAPABILITIES = (
    "Node Selection.",
    "Edge Selection.",
    "Path Selection.",
    "Relationship-Type Filtering.",
    "Node-Type Filtering.",
    "Canonical Identifier Filtering.",
    "Preferred Name Filtering.",
    "Domain Membership Filtering.",
    "Lifecycle Status Filtering.",
    "Source Node Filtering.",
    "Target Node Filtering.",
    "Direction Filtering.",
    "Exact Match Filtering.",
    "Deterministic Ordering.",
    "Result Limiting.",
    "Result Offset.",
    "Projection.",
    "Existence Validation.",
    "Reachability Validation.",
    "Direct Relationship Validation.",
    "Registered Path Validation.",
)

INITIAL_QUERY_FORMS = (
    "SELECT NODE.",
    "SELECT EDGE.",
    "SELECT PATH.",
    "VALIDATE EXISTS.",
    "VALIDATE REACHABLE.",
    "VALIDATE RELATIONSHIP.",
    "VALIDATE PATH.",
)

LANGUAGE_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Registered Node Closure.",
    "Registered Edge Closure.",
    "Registered Path Closure.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Selection Target Validity.",
    "Filter Canonicality.",
    "Projection Canonicality.",
    "Deterministic Ordering.",
    "Deterministic Pagination.",
    "Deterministic Query Result.",
    "Query Evidence Completeness.",
    "Result Integrity.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Fail-Closed Evaluation.",
)


def charter_text() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        charter_text().split()
    )


def test_charter_exists() -> None:
    assert CHARTER.is_file()


def test_document_identity() -> None:
    content = normalized_text()

    assert "Commerce Query Language" in content
    assert "Abbreviation CQL" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_vision_is_declared() -> None:
    content = normalized_text()

    assert (
        "Establish a canonical, declarative, "
        "deterministic, traceable, and auditable "
        "language for querying immutable Commerce "
        "Knowledge Graphs."
    ) in content

    assert (
        "Commerce Query Language shall allow consumers "
        "to request registered Commerce knowledge "
        "without modifying, extending, or redefining "
        "the queried Graph."
    ) in content


def test_mission_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define a technology-independent query language "
        "over the frozen Commerce Knowledge Graph.",
        "CQL shall transform explicit Query Requests "
        "into deterministic Query Results and Query "
        "Evidence.",
        "CQL shall preserve canonical identity, "
        "relationship direction, graph boundaries, "
        "baseline compatibility, and semantic closure.",
    ):
        assert requirement in content


def test_inputs_reference_frozen_baselines() -> None:
    content = normalized_text()

    for baseline in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
    ):
        assert baseline in content


def test_language_boundary_is_read_only() -> None:
    content = normalized_text()

    assert (
        "CQL is a read-only declarative query language."
    ) in content

    assert (
        "CQL shall not mutate the queried Graph."
    ) in content


def test_initial_query_capabilities_are_declared() -> None:
    content = normalized_text()

    for capability in INITIAL_QUERY_CAPABILITIES:
        assert capability in content


def test_initial_query_forms_are_declared() -> None:
    content = normalized_text()

    for form in INITIAL_QUERY_FORMS:
        assert form in content

    assert (
        "Every Query Request shall select exactly one "
        "canonical Query Form."
    ) in content


def test_query_identity_is_declared() -> None:
    content = normalized_text()

    assert "CKP-QUERY-000001" in content

    assert (
        "Query Identifiers shall be unique within one "
        "execution context."
    ) in content

    assert (
        "Query identity shall remain distinct from "
        "Query Version."
    ) in content


def test_read_only_semantics_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "CQL shall be read-only.",
        "A Query shall not:",
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Modify a Graph Component.",
        "Modify a frozen baseline.",
        "Create undocumented semantic meaning.",
    ):
        assert rule in content


def test_language_principles_are_declared() -> None:
    content = normalized_text()

    for principle in (
        "Read-only before extensible.",
        "Canonical identity before aliases.",
        "Explicit selection before inference.",
        "Validation before execution.",
        "Evidence for success and failure.",
    ):
        assert principle in content


def test_language_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in LANGUAGE_INVARIANTS:
        assert invariant in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Query Request is incomplete.",
        "The Graph Manifest cannot be resolved.",
        "The Graph Version is incompatible.",
        "The Query Form is unknown.",
        "A Query attempts to mutate the Graph.",
        "A Query attempts to redefine frozen Commerce semantics.",
    ):
        assert condition in content


def test_frozen_baseline_boundary_is_declared() -> None:
    content = normalized_text()

    for baseline in (
        "HAS Foundation 1.0 LTS remains frozen.",
        "Specification Runtime 1.0 remains frozen.",
        "CKP-001 Canonical Commerce Vocabulary 1.0 remains frozen.",
        "CKP-002 Commerce Ontology 1.0 remains frozen.",
        "CKP-003 Commerce Knowledge Graph 1.0 remains frozen.",
    ):
        assert baseline in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Every Query Request references one immutable Graph Version.",
        "Every Query Form is canonical.",
        "Every Selection Target is registered.",
        "No Query mutates the Graph.",
        "Query consistency is executable and auditable.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "CKP-004 shall remain specification-first."
    ) in content

    assert (
        "No parser, interpreter, compiler, storage "
        "adapter, network interface, or query runtime "
        "shall be implemented before the normative "
        "query models and executable specification "
        "contracts are complete."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.2" in content
    assert "Query Structure Model." in content
