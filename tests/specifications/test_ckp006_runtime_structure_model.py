"""
Executable Specification

CKP-006.2
Commerce Reasoning Runtime Structure Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_STRUCTURE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Structure Identity",
    "## Structure Version",
    "## Structural Scope",
    "## Canonical Runtime Structure",
    "## Structural Components",
    "## Runtime Instance",
    "## Runtime Execution",
    "## Runtime Session",
    "## Runtime Configuration",
    "## Runtime Limits",
    "## Execution Request",
    "## Execution Context",
    "## Runtime State",
    "## Runtime Stage",
    "## Runtime Transition",
    "## Runtime Input Set",
    "## Runtime Working Set",
    "## Runtime Artifact Registry",
    "## Runtime Output Set",
    "## Runtime Evidence",
    "## Runtime Failure",
    "## Runtime Result",
    "## Replay Descriptor",
    "## Runtime Validation Reference",
    "## Runtime Certification Reference",
    "## Structural Relationships",
    "## Cardinality Rules",
    "## Lifecycle Rules",
    "## Structural Integrity",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Structural Validation",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Structural Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

STRUCTURAL_COMPONENTS = (
    "Runtime Instance.",
    "Runtime Execution.",
    "Runtime Session.",
    "Runtime Configuration.",
    "Runtime Limits.",
    "Execution Request.",
    "Execution Context.",
    "Runtime State.",
    "Runtime Stage.",
    "Runtime Transition.",
    "Runtime Input Set.",
    "Runtime Working Set.",
    "Runtime Artifact Registry.",
    "Runtime Output Set.",
    "Runtime Evidence.",
    "Runtime Failure.",
    "Runtime Result.",
    "Replay Descriptor.",
    "Runtime Validation Reference.",
    "Runtime Certification Reference.",
)

RUNTIME_STAGES = (
    "CREATED.",
    "ADMISSION.",
    "CONTEXT RESOLUTION.",
    "FACT RESOLUTION.",
    "PREMISE EVALUATION.",
    "RULE APPLICABILITY.",
    "VARIABLE BINDING.",
    "RULE APPLICATION.",
    "CONCLUSION CONSTRUCTION.",
    "PROOF CONSTRUCTION.",
    "EVIDENCE CONSTRUCTION.",
    "EXPLANATION CONSTRUCTION.",
    "VALIDATION.",
    "CERTIFICATION.",
    "COMPLETION.",
    "FAILURE.",
    "CANCELLATION.",
)

RUNTIME_RESULT_STATUSES = (
    "COMPLETED.",
    "FAILED.",
    "CANCELLED.",
)

FAILURE_CLASSIFICATIONS = (
    "RUNTIME_STRUCTURE_IDENTITY_VIOLATION.",
    "RUNTIME_STRUCTURE_VERSION_VIOLATION.",
    "RUNTIME_INSTANCE_VIOLATION.",
    "RUNTIME_EXECUTION_VIOLATION.",
    "RUNTIME_SESSION_VIOLATION.",
    "RUNTIME_CONFIGURATION_VIOLATION.",
    "RUNTIME_LIMITS_VIOLATION.",
    "EXECUTION_REQUEST_VIOLATION.",
    "EXECUTION_CONTEXT_VIOLATION.",
    "RUNTIME_STATE_VIOLATION.",
    "RUNTIME_STAGE_VIOLATION.",
    "RUNTIME_TRANSITION_VIOLATION.",
    "RUNTIME_INPUT_SET_VIOLATION.",
    "RUNTIME_WORKING_SET_VIOLATION.",
    "RUNTIME_ARTIFACT_REGISTRY_VIOLATION.",
    "RUNTIME_OUTPUT_SET_VIOLATION.",
    "RUNTIME_EVIDENCE_VIOLATION.",
    "RUNTIME_FAILURE_VIOLATION.",
    "RUNTIME_RESULT_VIOLATION.",
    "REPLAY_DESCRIPTOR_VIOLATION.",
    "RUNTIME_VALIDATION_REFERENCE_VIOLATION.",
    "RUNTIME_CERTIFICATION_REFERENCE_VIOLATION.",
    "STRUCTURAL_RELATIONSHIP_VIOLATION.",
    "CARDINALITY_VIOLATION.",
    "LIFECYCLE_VIOLATION.",
    "ORDERING_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

STRUCTURAL_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Runtime Structure Identity.",
    "Runtime Structure Version Preservation.",
    "Exactly One Runtime Session Per Execution.",
    "Exactly One Runtime Configuration Per Execution.",
    "Exactly One Runtime Limits Artifact Per Execution.",
    "Exactly One Execution Request Per Execution.",
    "Exactly One Execution Context Per Execution.",
    "Exactly One Runtime State Per Execution.",
    "Exactly One Runtime Input Set After Admission.",
    "Exactly One Isolated Runtime Working Set.",
    "Exactly One Runtime Artifact Registry.",
    "Exactly One Runtime Output Set At Terminal State.",
    "Exactly One Runtime Evidence At Terminal State.",
    "At Most One Runtime Failure.",
    "Exactly One Runtime Result At Terminal State.",
    "Exactly One Replay Descriptor At Terminal State.",
    "Exactly One Runtime Validation Reference At Terminal State.",
    "At Most One Runtime Certification Reference.",
    "Runtime Stage Validity.",
    "Runtime Transition Validity.",
    "Runtime Transition Monotonicity.",
    "Structural Relationship Closure.",
    "Cardinality Integrity.",
    "Lifecycle Compatibility.",
    "Deterministic Ordering.",
    "Canonical Serialization.",
    "Structural Integrity.",
    "Fail-Closed Structural Validation.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def level_two_headings() -> list[str]:
    return [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "# CKP-006" in content
    assert "Title Commerce Reasoning Runtime Structure Model" in content
    assert "Abbreviation CRRSM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    headings = level_two_headings()

    for section in EXPECTED_SECTIONS:
        assert headings.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    headings = level_two_headings()

    positions = [
        headings.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = level_two_headings()

    assert len(headings) == len(set(headings))


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable-boundary, "
        "fail-closed, traceable, replay-compatible, and auditable "
        "structural model of the Commerce Reasoning Runtime.",
        "The Runtime Structure Model specializes the runtime "
        "boundaries established by the Commerce Reasoning "
        "Runtime Charter.",
        "This specification defines the structural components "
        "required to admit, execute, validate, complete, fail, "
        "cancel, and replay one Reasoning Execution.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not implement Runtime classes.",
        "It does not implement execution algorithms.",
        "It does not implement persistence.",
        "It does not implement transport.",
        "It does not implement distributed scheduling.",
        "It does not permit mutation of frozen CKP-005 "
        "knowledge or specifications.",
    ):
        assert boundary in content


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-004 Commerce Query Language 1.0.",
        "CKP-005 Baseline 1.0.",
        "CKP-005 Specification Freeze.",
        "CKP-006.1 Commerce Reasoning Runtime Charter.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert (
        "The Runtime Structure Model shall not reinterpret "
        "or modify any dependency."
    ) in content


def test_structure_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Structure shall possess exactly one "
        "immutable Runtime Structure Identifier.",
        "CKP-RUNTIME-STRUCTURE-000001",
        "Runtime Structure Identity shall remain distinct "
        "from Runtime Structure Version.",
        "Runtime Structure Identity shall be globally unique "
        "within one Runtime implementation baseline.",
        "A Runtime Structure Identifier shall never be reused "
        "for a different normative structure.",
    ):
        assert requirement in content


def test_structure_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Structure shall declare exactly one "
        "Runtime Structure Version.",
        "The initial supported Runtime Structure Version is: 1.0.",
        "Runtime Structure Version identifies the normative "
        "structure schema.",
        "Runtime Structure Version shall not replace Runtime "
        "Structure Identity.",
        "Unsupported Runtime Structure Versions shall cause "
        "structural validation failure.",
    ):
        assert requirement in content


def test_structural_scope_is_declared() -> None:
    content = normalized_text()

    assert (
        "The Runtime Structure Model defines the components "
        "required for exactly one Reasoning Execution."
    ) in content

    for component in STRUCTURAL_COMPONENTS:
        assert component in content

    assert "Cross-execution coordination remains outside Version 1.0." in content


def test_canonical_runtime_structure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Exactly one Runtime Instance.",
        "Zero or more Runtime Executions.",
        "Exactly one Runtime Session.",
        "Exactly one Runtime Configuration Reference.",
        "Exactly one Runtime Limits Reference.",
        "Exactly one Execution Request Reference.",
        "Exactly one Execution Context Reference.",
        "Exactly one Runtime State.",
        "Exactly one Runtime Input Set.",
        "Exactly one Runtime Working Set.",
        "Exactly one Runtime Artifact Registry.",
        "Exactly one Runtime Output Set after terminal completion.",
        "Exactly one Runtime Evidence artifact after terminal completion.",
        "Zero or one Runtime Failure.",
        "Exactly one Runtime Result after terminal completion.",
        "Exactly one Replay Descriptor after terminal completion.",
        "Exactly one Runtime Validation Reference after terminal completion.",
        "Zero or one Runtime Certification Reference.",
    ):
        assert requirement in content


def test_structural_components_are_declared() -> None:
    content = normalized_text()

    for component in STRUCTURAL_COMPONENTS:
        assert component in content

    assert (
        "Every structural component shall possess explicit "
        "identity, lifecycle, integrity, and traceability "
        "boundaries where applicable."
    ) in content


def test_runtime_instance_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Runtime Identifier.",
        "Runtime Version.",
        "Runtime Structure Version.",
        "Runtime Configuration Reference.",
        "Supported CKP-005 Baseline.",
        "Supported Graph Versions.",
        "Supported Rule Registry Versions.",
        "Supported Constraint Registry Versions.",
        "Runtime Instance Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "A Runtime Instance may host zero or more Runtime Executions."
    ) in content
    assert (
        "A Runtime Instance shall not share mutable execution "
        "state between Runtime Executions."
    ) in content


def test_runtime_execution_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Runtime Execution Identifier.",
        "Runtime Identifier.",
        "Runtime Version.",
        "Runtime Session Reference.",
        "Execution Request Reference.",
        "Execution Context Reference.",
        "Runtime Configuration Reference.",
        "Runtime Limits Reference.",
        "Runtime State Reference.",
        "Runtime Input Set Reference.",
        "Runtime Working Set Reference.",
        "Runtime Artifact Registry Reference.",
        "Runtime Execution Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Every Runtime Execution shall remain isolated "
        "from every other Runtime Execution."
    ) in content


def test_runtime_session_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess exactly one "
        "immutable Runtime Session."
    ) in content

    for property_name in (
        "Runtime Session Identifier.",
        "Runtime Execution Identifier.",
        "Runtime Identifier.",
        "Runtime Version.",
        "Session Lifecycle Status.",
        "Session Admission Result.",
        "Session Start Timestamp.",
        "Session Terminal Timestamp when applicable.",
        "Execution Context Reference.",
        "Runtime Configuration Reference.",
        "Runtime Limits Reference.",
        "Session Evidence Reference.",
        "Session Integrity Reference.",
    ):
        assert property_name in content

    assert "A Runtime Session shall not span multiple Runtime Executions." in content
    assert "A terminal Runtime Session shall remain immutable." in content


def test_runtime_configuration_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall reference exactly one "
        "immutable Runtime Configuration."
    ) in content

    for property_name in (
        "Runtime Configuration Identifier.",
        "Runtime Configuration Version.",
        "Runtime Version.",
        "CKP-005 Baseline Reference.",
        "Graph Compatibility Policy.",
        "Rule Registry Compatibility Policy.",
        "Constraint Registry Compatibility Policy.",
        "Deterministic Ordering Policy.",
        "Failure Policy.",
        "Replay Policy.",
        "Validation Policy.",
        "Certification Policy.",
        "Runtime Configuration Evidence Reference.",
        "Runtime Configuration Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Runtime Configuration substitution after admission is prohibited."
    ) in content


def test_runtime_limits_are_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall reference exactly one "
        "immutable Runtime Limits artifact."
    ) in content

    for limit_name in (
        "Maximum Reasoning Depth.",
        "Maximum Rule Applications.",
        "Maximum Derived Conclusions.",
        "Maximum Proof Steps.",
        "Maximum Evidence Artifacts.",
        "Maximum Runtime Transitions.",
        "Maximum Execution Duration.",
        "Maximum Working Set Size.",
    ):
        assert limit_name in content

    assert (
        "A Runtime Limit violation shall produce fail-closed "
        "terminal behavior."
    ) in content


def test_execution_request_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall reference exactly one "
        "admitted Execution Request."
    ) in content

    for property_name in (
        "Reasoning Request Identifier.",
        "Reasoning Request Version.",
        "Reasoning Form.",
        "Goal Assertion Reference.",
        "Graph Identifier.",
        "Graph Version.",
        "Baseline References.",
        "Fact Source References.",
        "Premise References.",
        "Rule References.",
        "Constraint References.",
        "Expected Reasoning Outcome.",
        "Execution Request Integrity Reference.",
    ):
        assert property_name in content

    assert "The Execution Request shall remain immutable after admission." in content


def test_execution_context_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall reference exactly one "
        "immutable Execution Context."
    ) in content

    for property_name in (
        "Execution Context Identifier.",
        "Execution Context Version.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Query Language Baseline Reference.",
        "CKP-005 Baseline Reference.",
        "Fact Registry Reference.",
        "Rule Registry Reference.",
        "Constraint Registry Reference.",
        "Runtime Configuration Reference.",
        "Runtime Limits Reference.",
        "Execution Context Evidence Reference.",
        "Execution Context Integrity Reference.",
    ):
        assert property_name in content

    assert "Execution Context substitution after admission is prohibited." in content


def test_runtime_state_is_exactly_one() -> None:
    content = normalized_text()

    assert "Every Runtime Execution shall possess exactly one Runtime State." in content

    for property_name in (
        "Runtime State Identifier.",
        "Runtime Execution Identifier.",
        "Current Runtime Stage.",
        "Current Lifecycle Status.",
        "Current Transition Number.",
        "Resolved Fact References.",
        "Evaluated Premise References.",
        "Applicable Rule References.",
        "Rejected Rule References.",
        "Rule Application References.",
        "Variable Binding References.",
        "Derived Conclusion References.",
        "Proof References.",
        "Evidence References.",
        "Runtime State Evidence Reference.",
        "Runtime State Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Runtime State may evolve only through valid Runtime Transitions."
    ) in content
    assert (
        "Runtime State shall become immutable at a terminal lifecycle state."
    ) in content


def test_runtime_stages_are_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall occupy exactly one "
        "Runtime Stage at a time."
    ) in content

    for stage in RUNTIME_STAGES:
        assert stage in content

    assert "Unknown or private Runtime Stages shall be invalid." in content


def test_runtime_transition_is_exactly_one_per_state_change() -> None:
    content = normalized_text()

    assert (
        "Every Runtime State change shall occur through "
        "exactly one Runtime Transition."
    ) in content

    for property_name in (
        "Runtime Transition Identifier.",
        "Runtime Execution Identifier.",
        "Source Runtime Stage.",
        "Target Runtime Stage.",
        "Source Lifecycle Status.",
        "Target Lifecycle Status.",
        "Transition Sequence Number.",
        "Transition Preconditions.",
        "Transition Result.",
        "Transition Evidence Reference.",
        "Transition Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Runtime Transition Sequence Numbers shall be unique "
        "and monotonically increasing within one Runtime Execution."
    ) in content
    assert "Invalid Runtime Transitions shall fail closed." in content


def test_runtime_input_set_is_exactly_one_after_admission() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess exactly one "
        "immutable Runtime Input Set after admission."
    ) in content

    for property_name in (
        "Execution Request Reference.",
        "Execution Context Reference.",
        "Runtime Configuration Reference.",
        "Runtime Limits Reference.",
        "Graph Target Reference.",
        "Baseline References.",
        "Fact Registry Reference.",
        "Rule Registry Reference.",
        "Constraint Registry Reference.",
        "Source Evidence References.",
        "Runtime Input Set Evidence Reference.",
        "Runtime Input Set Integrity Reference.",
    ):
        assert property_name in content

    assert "No undocumented Runtime Input shall participate in execution." in content


def test_runtime_working_set_is_isolated() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess exactly one "
        "isolated Runtime Working Set."
    ) in content

    for artifact in (
        "Resolved Facts.",
        "Evaluated Premises.",
        "Applicable Rules.",
        "Rejected Rules.",
        "Variable Bindings.",
        "Rule Applications.",
        "Derived Conclusions.",
        "Partial Proofs.",
        "Partial Evidence.",
        "Partial Explanation.",
        "Detected Violations.",
    ):
        assert artifact in content

    assert "Runtime Working Set content shall remain execution-local." in content
    assert (
        "Runtime Working Set content shall not become "
        "canonical Commerce knowledge."
    ) in content


def test_runtime_artifact_registry_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess exactly one "
        "Runtime Artifact Registry."
    ) in content

    for property_name in (
        "Artifact Identifier.",
        "Artifact Type.",
        "Artifact Lifecycle Status.",
        "Artifact Integrity Reference.",
        "Artifact Evidence Reference.",
        "Artifact Source Reference.",
    ):
        assert property_name in content

    assert (
        "The Runtime Artifact Registry shall not alter "
        "registered artifacts."
    ) in content


def test_runtime_output_set_is_terminal_only() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall possess exactly "
        "one immutable Runtime Output Set."
    ) in content

    for property_name in (
        "Reasoning Outcome.",
        "Final Conclusion References.",
        "Proof References.",
        "Reasoning Evidence Reference.",
        "Explanation Reference.",
        "Validation Result Reference.",
        "Runtime Result Reference.",
        "Replay Descriptor Reference.",
        "Runtime Output Set Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "A non-terminal Runtime Execution shall not claim "
        "a complete Runtime Output Set."
    ) in content


def test_runtime_evidence_is_terminal_and_complete() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall possess exactly "
        "one complete Runtime Evidence artifact."
    ) in content

    for property_name in (
        "Runtime Instance identity.",
        "Runtime Execution identity.",
        "Runtime Session identity.",
        "Runtime Configuration.",
        "Runtime Limits.",
        "Runtime Input Set.",
        "Runtime lifecycle.",
        "Runtime Stages.",
        "Runtime Transitions.",
        "Runtime Working Set terminal snapshot.",
        "Runtime Artifact Registry.",
        "Runtime Output Set.",
        "Runtime Result.",
        "Replay Descriptor.",
        "Validation Result.",
    ):
        assert property_name in content

    assert (
        "Runtime Evidence shall be deterministic, immutable, "
        "complete, and traceable."
    ) in content


def test_runtime_failure_cardinality_is_declared() -> None:
    content = normalized_text()

    assert (
        "A failed Runtime Execution shall possess exactly one "
        "Runtime Failure artifact."
    ) in content
    assert (
        "A non-failed Runtime Execution shall possess no "
        "Runtime Failure artifact."
    ) in content

    for property_name in (
        "Runtime Failure Identifier.",
        "Runtime Execution Identifier.",
        "Failed Runtime Stage.",
        "Failed Runtime Transition Reference.",
        "Failed Artifact Type.",
        "Failed Artifact Identifier.",
        "Failure Classification.",
        "Failure Reason.",
        "Resolved Input References.",
        "Unresolved Input References.",
        "Partial Artifact References.",
        "Failure Evidence Reference.",
        "Failure Integrity Reference.",
    ):
        assert property_name in content


def test_runtime_result_is_exactly_one_at_terminal_state() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall possess exactly "
        "one immutable Runtime Result."
    ) in content

    for status in RUNTIME_RESULT_STATUSES:
        assert status in content

    assert (
        "Runtime Result shall remain compatible with the "
        "terminal Runtime lifecycle state."
    ) in content


def test_replay_descriptor_is_exactly_one_at_terminal_state() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall possess exactly "
        "one Replay Descriptor."
    ) in content

    for property_name in (
        "Replay Descriptor Identifier.",
        "Runtime Execution Identifier.",
        "Runtime Version.",
        "Runtime Structure Version.",
        "Runtime Configuration Reference.",
        "Runtime Limits Reference.",
        "Execution Request Reference.",
        "Execution Context Reference.",
        "Graph Identifier.",
        "Graph Version.",
        "Baseline References.",
        "Registry Version References.",
        "Canonical Input Ordering.",
        "Canonical Transition Ordering.",
        "Canonical Artifact Ordering.",
        "Terminal Runtime Result Reference.",
        "Replay Evidence Reference.",
        "Replay Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Replay Descriptor shall not depend on undocumented "
        "environment state."
    ) in content


def test_runtime_validation_reference_is_required_at_terminal_state() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall possess exactly "
        "one Runtime Validation Reference."
    ) in content
    assert (
        "The Runtime Validation Reference shall resolve to one "
        "Validation Result and one Validation Report."
    ) in content
    assert (
        "A COMPLETED Runtime Result shall require Validation Result PASS."
    ) in content


def test_runtime_certification_reference_is_optional_and_gated() -> None:
    content = normalized_text()

    assert (
        "A Runtime Execution may possess zero or one "
        "Runtime Certification Reference."
    ) in content
    assert (
        "A Runtime Certification Reference shall resolve only "
        "after Validation Result PASS."
    ) in content
    assert (
        "A Runtime Certification Reference shall not exist "
        "for an invalid Runtime Result."
    ) in content


def test_structural_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Runtime Instance hosts Runtime Execution.",
        "Runtime Execution owns Runtime Session.",
        "Runtime Execution references Runtime Configuration.",
        "Runtime Execution references Runtime Limits.",
        "Runtime Execution consumes Execution Request.",
        "Runtime Execution consumes Execution Context.",
        "Runtime Execution owns Runtime State.",
        "Runtime State occupies Runtime Stage.",
        "Runtime State changes through Runtime Transition.",
        "Runtime Execution owns Runtime Input Set.",
        "Runtime Execution owns Runtime Working Set.",
        "Runtime Execution owns Runtime Artifact Registry.",
        "Terminal Runtime Execution owns Runtime Output Set.",
        "Terminal Runtime Execution owns Runtime Evidence.",
        "Failed Runtime Execution owns Runtime Failure.",
        "Terminal Runtime Execution owns Runtime Result.",
        "Terminal Runtime Execution owns Replay Descriptor.",
        "Terminal Runtime Execution references Runtime Validation.",
        "Validated Runtime Execution may reference Runtime Certification.",
    ):
        assert relationship in content

    assert (
        "Every relationship shall be explicit, resolvable, "
        "deterministic, and integrity-bound."
    ) in content


def test_cardinality_rules_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "Exactly one Runtime Instance reference.",
        "Exactly one Runtime Session.",
        "Exactly one Runtime Configuration reference.",
        "Exactly one Runtime Limits reference.",
        "Exactly one Execution Request reference.",
        "Exactly one Execution Context reference.",
        "Exactly one Runtime State.",
        "Exactly one Runtime Input Set after admission.",
        "Exactly one Runtime Working Set.",
        "Exactly one Runtime Artifact Registry.",
        "Zero Runtime Output Sets before terminal completion.",
        "Exactly one Runtime Output Set after terminal completion.",
        "Zero Runtime Results before terminal completion.",
        "Exactly one Runtime Result after terminal completion.",
        "Zero or one Runtime Failure.",
        "Exactly one Replay Descriptor after terminal completion.",
        "Exactly one Runtime Validation Reference after terminal completion.",
        "Zero or one Runtime Certification Reference.",
    ):
        assert rule in content

    assert "Cardinality violations shall fail structural validation." in content


def test_lifecycle_rules_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "Runtime Input Set may be incomplete.",
        "Runtime Working Set shall be empty.",
        "Runtime Output Set shall not exist.",
        "Runtime Result shall not exist.",
        "Runtime Input Set shall be immutable.",
        "Runtime Session shall be active.",
        "Runtime State shall evolve only through valid transitions.",
        "Runtime Output Set shall exist.",
        "Runtime Evidence shall be complete.",
        "Runtime Result shall exist.",
        "Replay Descriptor shall exist.",
        "Runtime Validation Reference shall exist.",
        "Runtime Failure shall exist.",
        "Failure Evidence shall be complete.",
        "Runtime Result Status shall be FAILED.",
        "Cancellation Evidence shall be complete.",
        "Runtime Result Status shall be CANCELLED.",
        "Terminal structural components shall remain immutable.",
    ):
        assert rule in content


def test_structural_integrity_is_declared() -> None:
    content = normalized_text()

    for binding in (
        "Component identity.",
        "Component version.",
        "Runtime Execution identity.",
        "Lifecycle status.",
        "Structural relationships.",
        "Cardinality.",
        "Artifact references.",
        "Evidence references.",
        "Source references.",
    ):
        assert binding in content

    assert (
        "Any unauthorized structural mutation shall invalidate "
        "Structural Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Preserve every normative property.",
        "Preserve component identity.",
        "Preserve lifecycle status.",
        "Preserve structural relationships.",
        "Preserve cardinality.",
        "Preserve Runtime Stage.",
        "Preserve Runtime Transition ordering.",
        "Preserve artifact references.",
        "Preserve evidence references.",
        "Preserve integrity references.",
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for integrity calculation.",
    ):
        assert requirement in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for ordering_rule in (
        "Runtime Executions shall be ordered by: Runtime Execution Identifier.",
        "Transition Sequence Number. Then Runtime Transition Identifier.",
        "Resolved Facts shall be ordered by: Fact Identifier.",
        "Premise Priority. Then Premise Identifier.",
        "Rule Priority. Then Rule Identifier.",
        "Reasoning Depth. Then Rule Priority. Then Rule Identifier. "
        "Then Rule Application Identifier.",
        "Variable Bindings shall be ordered by: Variable Identifier.",
        "Reasoning Depth. Then Conclusion Identifier.",
        "Proofs shall be ordered by: Proof Identifier.",
        "Artifact Type. Then Artifact Identifier.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert ordering_rule in content


def test_structural_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Runtime Structure Identity.",
        "Runtime Structure Version.",
        "Normative dependency compatibility.",
        "Runtime Instance resolution.",
        "Runtime Execution identity.",
        "Runtime Session cardinality.",
        "Runtime Configuration cardinality.",
        "Runtime Limits cardinality.",
        "Execution Request cardinality.",
        "Execution Context cardinality.",
        "Runtime State cardinality.",
        "Runtime Stage validity.",
        "Runtime Transition validity.",
        "Runtime Transition ordering.",
        "Runtime Input Set cardinality.",
        "Runtime Working Set isolation.",
        "Runtime Artifact Registry cardinality.",
        "Runtime Output Set lifecycle compatibility.",
        "Runtime Evidence completeness.",
        "Runtime Failure lifecycle compatibility.",
        "Runtime Result lifecycle compatibility.",
        "Replay Descriptor completeness.",
        "Runtime Validation Reference completeness.",
        "Runtime Certification Reference compatibility.",
        "Structural relationship closure.",
        "Cardinality compliance.",
        "Lifecycle compliance.",
        "Canonical serialization.",
        "Structural Integrity.",
    ):
        assert validation_check in content

    assert "Structural Validation shall fail closed." in content
    assert "An invalid Runtime Structure shall not execute." in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Runtime Structure Identity is invalid.",
        "Runtime Structure Version is unsupported.",
        "A normative dependency is incompatible.",
        "Runtime Instance cannot be resolved.",
        "Runtime Session cardinality is violated.",
        "Runtime Configuration is missing, mutable, or incompatible.",
        "Runtime Limits are missing or invalid.",
        "Execution Request is missing or mutable.",
        "Execution Context is missing or mutable.",
        "Runtime State is missing or invalid.",
        "Runtime Stage is unknown or incompatible.",
        "A Runtime Transition is invalid.",
        "Runtime Transition ordering is inconsistent.",
        "Runtime Working Set is shared across executions.",
        "Runtime Evidence is incomplete.",
        "Runtime Result is missing after terminal completion.",
        "Replay Descriptor is missing or incomplete.",
        "Runtime Validation Reference is missing after terminal completion.",
        "Runtime Certification exists without Validation Result PASS.",
        "A cardinality rule is violated.",
        "A lifecycle rule is violated.",
        "Canonical serialization cannot be produced.",
        "Structural Integrity cannot be established.",
        "The Runtime Structure attempts to mutate source knowledge "
        "or a frozen baseline.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Canonical Commerce Term.",
        "Create an Ontology Assertion.",
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Modify a registered Fact.",
        "Modify a registered Premise.",
        "Modify a registered Rule.",
        "Modify a registered Constraint.",
        "Modify an admitted Reasoning Request.",
        "Modify an admitted Execution Context.",
        "Register a Derived Conclusion as a Graph Fact.",
        "Modify a Proof.",
        "Modify Reasoning Evidence.",
        "Modify an Explanation.",
        "Modify a Validation Result.",
        "Modify a Certification Record.",
        "Modify CKP-005 Baseline 1.0.",
        "Modify CKP-006.1.",
        "Repair an invalid structural component.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_structural_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in STRUCTURAL_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Runtime Structure Identity is valid.",
        "Runtime Structure Version is supported.",
        "Every normative dependency is compatible.",
        "Runtime Instance is resolvable.",
        "Every Runtime Execution is isolated.",
        "Every mandatory component exists with valid cardinality.",
        "Every structural relationship resolves.",
        "Runtime Configuration is immutable.",
        "Runtime Limits are valid.",
        "Execution Request is immutable after admission.",
        "Execution Context is immutable after admission.",
        "Runtime State changes only through valid Runtime Transitions.",
        "Runtime Working Set remains isolated.",
        "Runtime Artifact Registry does not mutate artifacts.",
        "Terminal Runtime Outputs are complete.",
        "Runtime Evidence is complete.",
        "Runtime Result is compatible with lifecycle state.",
        "Replay Descriptor is complete.",
        "Runtime Validation Reference is complete.",
        "Runtime Certification Reference is compatible.",
        "Deterministic ordering succeeds.",
        "Canonical serialization succeeds.",
        "Structural Integrity is valid.",
        "No Failure Condition remains open.",
        "The Runtime Structure does not mutate source knowledge "
        "or a frozen baseline.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the Commerce Reasoning "
        "Runtime Structure Model."
    ) in content

    for excluded_capability in (
        "Concrete Runtime classes.",
        "Runtime execution algorithms.",
        "Persistence implementation.",
        "Transport implementation.",
        "Distributed execution.",
        "Concurrency implementation.",
        "Cryptographic algorithm selection.",
        "Production deployment.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-006 deliverables shall preserve "
        "this Runtime Structure Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006.3" in content
    assert "Runtime Execution Request Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
