"""
Executable Specification

CKP-006.1
Commerce Reasoning Runtime Charter
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_COMMERCE_REASONING_RUNTIME_CHARTER.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Runtime Identity",
    "## Runtime Mission",
    "## Normative Baseline",
    "## Runtime Scope",
    "## Runtime Responsibilities",
    "## Runtime Non-Responsibilities",
    "## Execution Boundary",
    "## Determinism",
    "## Fail-Closed Behavior",
    "## Read-Only Knowledge Boundary",
    "## Runtime State Boundary",
    "## Execution Lifecycle",
    "## Runtime Inputs",
    "## Runtime Outputs",
    "## Runtime Evidence",
    "## Runtime Integrity",
    "## Replay Compatibility",
    "## Failure Semantics",
    "## Security Boundary",
    "## Conformance Requirements",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

RUNTIME_SCOPE_ITEMS = (
    "Reasoning Request admission.",
    "Execution Context resolution.",
    "Fact resolution.",
    "Premise evaluation.",
    "Rule registration verification.",
    "Rule applicability evaluation.",
    "Variable binding.",
    "Rule Application.",
    "Derived Conclusion construction.",
    "Proof construction.",
    "Reasoning Evidence construction.",
    "Explanation construction.",
    "Reasoning Validation invocation.",
    "Reasoning Certification invocation when requested and permitted.",
    "Execution Result construction.",
    "Failure Result construction.",
    "Runtime state transition.",
    "Replay-compatible artifact production.",
)

EXECUTION_LIFECYCLE = (
    "Created.",
    "Admitted.",
    "Running.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

RUNTIME_INPUTS = (
    "Runtime Identifier.",
    "Runtime Version.",
    "Reasoning Request Reference.",
    "Reasoning Execution Context Reference.",
    "Graph Identifier.",
    "Graph Version.",
    "Vocabulary Baseline Reference.",
    "Ontology Baseline Reference.",
    "Graph Baseline Reference.",
    "Query Language Baseline Reference.",
    "CKP-005 Baseline Reference.",
    "Fact Registry Reference.",
    "Rule Registry Reference.",
    "Constraint Registry Reference.",
    "Runtime Configuration Reference.",
    "Runtime Limits.",
    "Source Evidence References.",
)

RUNTIME_OUTPUTS = (
    "Runtime Execution Identifier.",
    "Runtime Status.",
    "Reasoning Status.",
    "Reasoning Outcome.",
    "Resolved Fact References.",
    "Evaluated Premise References.",
    "Considered Rule References.",
    "Rule Application References.",
    "Variable Binding References.",
    "Derived Conclusion References.",
    "Proof References.",
    "Reasoning Evidence Reference.",
    "Explanation Reference.",
    "Validation Result Reference.",
    "Certification Reference when applicable.",
    "Failure Evidence Reference when applicable.",
    "Runtime Result Integrity Reference.",
    "Replay Reference.",
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
    assert "Title Commerce Reasoning Runtime Charter" in content
    assert "Abbreviation CRRC" in content
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
        "Define the canonical, deterministic, fail-closed, "
        "auditable, replay-compatible, integrity-preserving, "
        "and normatively conformant charter for the "
        "Commerce Reasoning Runtime.",
        "The Commerce Reasoning Runtime shall materialize "
        "the frozen CKP-005 Commerce Reasoning Specification "
        "without redefining, weakening, extending, or repairing "
        "its normative semantics.",
        "The Runtime shall execute validated Reasoning Requests "
        "against immutable Commerce Knowledge Platform baselines.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "This Charter does not define implementation classes.",
        "It does not define storage technology.",
        "It does not define transport protocols.",
        "It does not define a concrete cryptographic algorithm.",
        "It does not permit mutation of frozen knowledge baselines.",
    ):
        assert boundary in content


def test_runtime_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every conforming Commerce Reasoning Runtime shall "
        "possess exactly one immutable Runtime Identifier.",
        "CKP-RUNTIME-000001",
        "Runtime Identity shall remain distinct from Runtime Version.",
        "A Runtime Identifier shall not be reused for a different "
        "normative Runtime instance.",
        "Missing, malformed, duplicated, or reused Runtime Identity "
        "shall cause Runtime admission failure.",
    ):
        assert requirement in content


def test_runtime_mission_is_declared() -> None:
    content = normalized_text()

    assert (
        "The Runtime mission is to execute one validated "
        "Reasoning Request deterministically against one "
        "immutable Reasoning Execution Context."
    ) in content

    for preserved_identity in (
        "CKP-005 semantics.",
        "Request identity.",
        "Goal identity.",
        "Graph identity.",
        "Baseline identity.",
        "Fact identity.",
        "Premise identity.",
        "Rule identity.",
        "Rule Application identity.",
        "Proof identity.",
        "Evidence identity.",
        "Explanation identity.",
        "Validation identity.",
        "Certification identity when applicable.",
    ):
        assert preserved_identity in content


def test_normative_baseline_is_declared() -> None:
    content = normalized_text()

    for dependency in (
        "CKP-005 Baseline 1.0.",
        "CKP-005.1 Commerce Reasoning Charter.",
        "CKP-005.2 Reasoning Structure Model.",
        "CKP-005.3 Reasoning Request Model.",
        "CKP-005.4 Inference Rule Model.",
        "CKP-005.5 Fact and Premise Model.",
        "CKP-005.6 Proof Model.",
        "CKP-005.7 Reasoning Evidence Model.",
        "CKP-005.8 Explanation Model.",
        "CKP-005.9 Reasoning Validation Model.",
        "CKP-005.10 Reasoning Certification Model.",
        "CKP-005 Specification Freeze.",
    ):
        assert dependency in content

    assert "The Runtime shall not reinterpret the frozen baseline." in content


def test_runtime_scope_is_declared() -> None:
    content = normalized_text()

    for item in RUNTIME_SCOPE_ITEMS:
        assert item in content

    assert (
        "Runtime scope shall remain limited to one Reasoning "
        "Execution at a time unless a future normative version "
        "explicitly defines multi-execution coordination."
    ) in content


def test_runtime_responsibilities_are_declared() -> None:
    content = normalized_text()

    for responsibility in (
        "Validate every mandatory input before use.",
        "Preserve immutable baseline references.",
        "Apply deterministic ordering.",
        "Enforce Reasoning Limits.",
        "Enforce lifecycle requirements.",
        "Construct Proofs from explicit dependencies.",
        "Construct Evidence for successful, failed, "
        "non-applicable, and cancelled paths.",
        "Invoke Validation before terminal completion.",
        "Invoke Certification only after successful Validation "
        "and explicit authorization.",
        "Fail closed when any mandatory condition cannot be established.",
    ):
        assert responsibility in content


def test_runtime_non_responsibilities_are_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Define new Commerce semantics.",
        "Create Canonical Commerce Terms.",
        "Modify the Commerce Ontology.",
        "Modify the Commerce Knowledge Graph.",
        "Repair malformed Facts.",
        "Repair unsatisfied Premises.",
        "Repair invalid Rules.",
        "Repair broken Proofs.",
        "Repair incomplete Evidence.",
        "Invent missing Variable Bindings.",
        "Infer undocumented Rule behavior.",
        "Select private runtime Rules.",
        "Override CKP-005 invariants.",
        "Perform probabilistic reasoning.",
        "Perform machine learning.",
        "Modify a completed Reasoning Result.",
    ):
        assert prohibition in content


def test_execution_boundary_is_exact() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Execution shall process exactly one "
        "Reasoning Request.",
        "Every Runtime Execution shall use exactly one "
        "Reasoning Execution Context.",
        "Every Runtime Execution shall target exactly one "
        "Graph Identifier and one Graph Version.",
        "Execution boundaries shall remain immutable after admission.",
        "Cross-request state leakage is prohibited.",
    ):
        assert requirement in content


def test_determinism_is_declared() -> None:
    content = normalized_text()

    for deterministic_element in (
        "Input ordering.",
        "Fact resolution ordering.",
        "Premise evaluation ordering.",
        "Rule applicability ordering.",
        "Variable binding ordering.",
        "Rule Application ordering.",
        "Conclusion ordering.",
        "Proof ordering.",
        "Evidence ordering.",
        "Explanation ordering.",
        "Validation ordering.",
        "Failure ordering.",
    ):
        assert deterministic_element in content

    assert "Runtime scheduling shall not alter normative results." in content
    assert "Implementation-defined ordering is prohibited." in content


def test_fail_closed_behavior_is_declared() -> None:
    content = normalized_text()

    assert "The Runtime shall fail closed." in content

    for failure_condition in (
        "Runtime Identity is invalid.",
        "Runtime Version is unsupported.",
        "The CKP-005 baseline cannot be resolved.",
        "A mandatory input is missing.",
        "The Reasoning Request is invalid.",
        "The Execution Context is invalid.",
        "The Graph target is incompatible.",
        "A mandatory Fact cannot be resolved.",
        "A mandatory Premise is unsatisfied.",
        "A required Rule is unregistered.",
        "A required Variable cannot be bound.",
        "A mandatory Constraint is violated.",
        "Reasoning Limits are exceeded.",
        "A Proof cannot be completed.",
        "Evidence cannot be completed.",
        "Validation does not return PASS.",
        "Runtime Integrity cannot be established.",
    ):
        assert failure_condition in content


def test_read_only_knowledge_boundary_is_declared() -> None:
    content = normalized_text()

    for read_only_target in (
        "Canonical Commerce Vocabulary.",
        "Commerce Ontology.",
        "Commerce Knowledge Graph.",
        "Registered Facts.",
        "Registered Premises.",
        "Registered Rules.",
        "Registered Constraints.",
        "Reasoning Requests after admission.",
        "Execution Contexts after admission.",
        "Proof inputs.",
        "Evidence inputs.",
        "Frozen CKP-005 specifications.",
    ):
        assert read_only_target in content

    assert "The Runtime shall not mutate source knowledge." in content


def test_runtime_state_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "The Runtime may maintain transient execution state only "
        "within one admitted Reasoning Execution.",
        "Runtime State shall remain isolated from other executions.",
        "Runtime State shall not become canonical Commerce knowledge.",
        "Runtime State shall be immutable after the execution "
        "reaches a terminal state.",
    ):
        assert requirement in content


def test_execution_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in EXECUTION_LIFECYCLE:
        assert state in content

    assert "A terminal lifecycle state shall not regress." in content

    assert (
        "Completed, Failed, and Cancelled shall each produce "
        "a terminal Runtime Result."
    ) in content


def test_runtime_inputs_are_declared() -> None:
    content = normalized_text()

    for runtime_input in RUNTIME_INPUTS:
        assert runtime_input in content

    assert "Every mandatory Runtime Input shall be explicit." in content

    assert (
        "No mandatory Runtime Input shall be inferred "
        "from environment defaults."
    ) in content


def test_runtime_outputs_are_declared() -> None:
    content = normalized_text()

    for runtime_output in RUNTIME_OUTPUTS:
        assert runtime_output in content

    assert (
        "Outputs shall be deterministic, immutable, "
        "traceable, and canonically serializable."
    ) in content


def test_runtime_evidence_is_complete() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall produce deterministic "
        "Runtime Evidence."
    ) in content

    for property_name in (
        "Runtime Identity.",
        "Runtime Version.",
        "Runtime Configuration Reference.",
        "Lifecycle transitions.",
        "Resolved inputs.",
        "Rejected inputs.",
        "Applied Rules.",
        "Rejected Rules.",
        "Rule Applications.",
        "Variable Bindings.",
        "Derived Conclusions.",
        "Proofs.",
        "Reasoning Evidence.",
        "Explanation.",
        "Validation Result.",
        "Certification Result when applicable.",
        "Failure Classification.",
        "Failure Reason.",
        "Terminal Runtime Status.",
        "Runtime Evidence Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "No successful, failed, or cancelled Runtime "
        "Execution shall omit Evidence."
    ) in content


def test_runtime_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess one "
        "deterministic Runtime Integrity Reference."
    ) in content

    assert (
        "Any normative Runtime mutation shall invalidate "
        "Runtime Integrity."
    ) in content


def test_replay_compatibility_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall produce "
        "sufficient immutable artifacts for deterministic replay."
    ) in content

    for preserved_item in (
        "Reasoning Request.",
        "Execution Context.",
        "Graph target.",
        "Baseline versions.",
        "Runtime Version.",
        "Runtime Configuration.",
        "Runtime Limits.",
        "Fact resolution results.",
        "Premise evaluation results.",
        "Rule ordering.",
        "Rule Applications.",
        "Variable Bindings.",
        "Derived Conclusions.",
        "Proofs.",
        "Evidence.",
        "Explanation.",
        "Validation Result.",
        "Terminal Runtime Result.",
    ):
        assert preserved_item in content

    assert (
        "A replay shall not depend on undocumented environment state."
    ) in content


def test_failure_semantics_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Failure Identifier.",
        "Runtime Execution Identifier.",
        "Failed Runtime Stage.",
        "Failed Artifact Type.",
        "Failed Artifact Identifier.",
        "Failure Classification.",
        "Failure Reason.",
        "Resolved Inputs.",
        "Unresolved Inputs.",
        "Partial Rule Applications.",
        "Partial Conclusions.",
        "Partial Proof References.",
        "Source Evidence References.",
        "Failure Evidence Reference.",
        "Failure Integrity Reference.",
    ):
        assert property_name in content

    assert "Failures shall be deterministic." in content
    assert "Failures shall be traceable." in content
    assert "Failures shall not repair the failed execution." in content


def test_security_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "The Runtime shall treat all external inputs as "
        "untrusted until validated."
    ) in content

    for untrusted_item in (
        "Caller assertions.",
        "Environment defaults.",
        "Unverified baseline references.",
        "Unregistered Rules.",
        "Unregistered Constraints.",
        "Unverified Evidence.",
        "Unverified Proofs.",
        "Unverified Execution Contexts.",
    ):
        assert untrusted_item in content

    assert (
        "The Runtime shall verify every normative reference before use."
    ) in content


def test_conformance_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Implement the frozen CKP-005 Baseline 1.0 "
        "without semantic reinterpretation.",
        "Preserve deterministic execution.",
        "Preserve read-only knowledge boundaries.",
        "Preserve fail-closed behavior.",
        "Preserve complete traceability.",
        "Produce complete Runtime Evidence.",
        "Produce replay-compatible artifacts.",
        "Validate terminal results.",
        "Prevent Certification without Validation Result PASS.",
        "Preserve canonical serialization.",
        "Preserve Runtime Integrity.",
    ):
        assert requirement in content

    assert (
        "A Runtime that violates any mandatory requirement "
        "shall not claim CKP-006 conformance."
    ) in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Runtime Identity is valid.",
        "The CKP-005 baseline is resolvable and compatible.",
        "Runtime scope is explicit.",
        "Runtime responsibilities are enforced.",
        "Runtime non-responsibilities are preserved.",
        "Execution boundaries are immutable.",
        "Determinism is preserved.",
        "Fail-closed behavior is preserved.",
        "Knowledge remains read-only.",
        "Runtime State remains isolated.",
        "The canonical lifecycle is enforced.",
        "Inputs are explicit and valid.",
        "Outputs are complete and immutable.",
        "Runtime Evidence is complete.",
        "Runtime Integrity is valid.",
        "Replay compatibility is established.",
        "Failure semantics are deterministic.",
        "Security boundaries are enforced.",
        "All conformance requirements are satisfied.",
        "No mandatory condition remains unresolved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the Commerce Reasoning Runtime Charter."
    ) in content

    for excluded_capability in (
        "Concrete Runtime classes.",
        "Persistence implementation.",
        "Transport implementation.",
        "Distributed scheduling.",
        "Cryptographic algorithm selection.",
        "Production observability.",
        "Production deployment.",
        "Machine learning.",
        "Probabilistic reasoning.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-006 deliverables shall preserve "
        "this Runtime Charter."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006.2" in content
    assert "Runtime Structure Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
