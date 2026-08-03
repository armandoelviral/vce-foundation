"""
Executable Specification

CKP-005.7
Commerce Reasoning Evidence Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_REASONING_EVIDENCE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Evidence Identity",
    "## Evidence Version",
    "## Evidence Lifecycle",
    "## Evidence Type",
    "## Evidence Properties",
    "## Evidence Scope",
    "## Request Evidence",
    "## Fact Evidence",
    "## Premise Evidence",
    "## Rule Evidence",
    "## Rule Application Evidence",
    "## Proof Evidence",
    "## Proof Step Evidence",
    "## Contradiction Evidence",
    "## Failure Evidence",
    "## Terminal Reasoning Evidence",
    "## Reasoning Status Compatibility",
    "## Reasoning Outcome Compatibility",
    "## Evidence Construction",
    "## Evidence Completeness",
    "## Evidence Closure",
    "## Evidence Chain",
    "## Evidence Ordering",
    "## Evidence Validation",
    "## Evidence Validation Result",
    "## Evidence Integrity",
    "## Evidence Chain Integrity",
    "## Canonical Serialization",
    "## Determinism",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Evidence Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

EVIDENCE_TYPES = (
    "REQUEST EVIDENCE.",
    "FACT EVIDENCE.",
    "PREMISE EVIDENCE.",
    "RULE EVIDENCE.",
    "RULE APPLICATION EVIDENCE.",
    "PROOF EVIDENCE.",
    "PROOF STEP EVIDENCE.",
    "CONTRADICTION EVIDENCE.",
    "FAILURE EVIDENCE.",
    "TERMINAL REASONING EVIDENCE.",
)

EVIDENCE_LIFECYCLE_VALUES = (
    "Draft.",
    "Constructed.",
    "Validated.",
    "Invalid.",
    "Superseded.",
    "Archived.",
)

FAILURE_CLASSIFICATIONS = (
    "EVIDENCE_IDENTITY_VIOLATION.",
    "EVIDENCE_VERSION_VIOLATION.",
    "EVIDENCE_LIFECYCLE_VIOLATION.",
    "EVIDENCE_TYPE_VIOLATION.",
    "EVIDENCE_SCOPE_VIOLATION.",
    "REQUEST_EVIDENCE_VIOLATION.",
    "FACT_EVIDENCE_VIOLATION.",
    "PREMISE_EVIDENCE_VIOLATION.",
    "RULE_EVIDENCE_VIOLATION.",
    "RULE_APPLICATION_EVIDENCE_VIOLATION.",
    "PROOF_EVIDENCE_VIOLATION.",
    "PROOF_STEP_EVIDENCE_VIOLATION.",
    "CONTRADICTION_EVIDENCE_VIOLATION.",
    "FAILURE_EVIDENCE_VIOLATION.",
    "TERMINAL_EVIDENCE_VIOLATION.",
    "STATUS_COMPATIBILITY_VIOLATION.",
    "OUTCOME_COMPATIBILITY_VIOLATION.",
    "EVIDENCE_COMPLETENESS_VIOLATION.",
    "EVIDENCE_REFERENCE_CLOSURE_VIOLATION.",
    "EVIDENCE_CHAIN_VIOLATION.",
    "EVIDENCE_CHAIN_CYCLE_VIOLATION.",
    "ORDERING_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "DETERMINISM_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

EVIDENCE_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Evidence Identity.",
    "Evidence Version Preservation.",
    "Lifecycle Validity.",
    "Canonical Evidence Type.",
    "Exactly One Reasoning Request Scope.",
    "Immutable Execution Context.",
    "Immutable Graph Target.",
    "Baseline Compatibility.",
    "Request Evidence Completeness.",
    "Fact Evidence Completeness.",
    "Premise Evidence Completeness.",
    "Rule Evidence Completeness.",
    "Rule Application Evidence Completeness.",
    "Proof Evidence Completeness.",
    "Proof Step Evidence Completeness.",
    "Contradiction Branch Preservation.",
    "Failure Evidence Completeness.",
    "Exactly One Terminal Evidence Artifact.",
    "Reasoning Status Compatibility.",
    "Reasoning Outcome Compatibility.",
    "Expected Outcome Independence.",
    "Evidence Reference Closure.",
    "No Dangling Evidence References.",
    "Evidence Chain Completeness.",
    "Evidence Chain Acyclicity.",
    "Deterministic Evidence Ordering.",
    "Deterministic Evidence Construction.",
    "Canonical Serialization.",
    "Evidence Integrity.",
    "Evidence Chain Integrity.",
    "Fail-Closed Validation.",
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

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Evidence Model" in content
    assert "Abbreviation CREM" in content
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


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-004 Commerce Query Language 1.0.",
        "CKP-005.1 Commerce Reasoning Charter.",
        "CKP-005.2 Commerce Reasoning Structure Model.",
        "CKP-005.3 Commerce Reasoning Request Model.",
        "CKP-005.4 Inference Rule Model.",
        "CKP-005.5 Fact and Premise Model.",
        "CKP-005.6 Proof Model.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert (
        "Reasoning Evidence shall not redefine or "
        "modify any dependency."
    ) in content


def test_evidence_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Evidence artifact shall possess "
        "exactly one immutable Evidence Identifier.",
        "CKP-REASONING-EVIDENCE-000001",
        "Every Evidence Identifier shall be globally "
        "unique within one Reasoning Execution registry.",
        "An Evidence Identifier shall never be reused "
        "for a different normative Evidence artifact.",
    ):
        assert requirement in content


def test_evidence_version_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Reasoning Evidence artifact shall declare "
        "one Evidence Version."
    ) in content
    assert "The initial supported Evidence Version is: 1.0." in content
    assert "Evidence Version shall not replace Evidence Identity." in content
    assert (
        "Evidence Version compatibility shall be verified "
        "before Evidence construction or validation."
    ) in content


def test_evidence_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in EVIDENCE_LIFECYCLE_VALUES:
        assert lifecycle in content

    for rule in (
        "Draft Evidence shall not support a terminal "
        "Reasoning Result.",
        "Only Validated Evidence may support a Completed, "
        "Failed, or Cancelled Reasoning Result.",
        "Invalid Evidence shall not support a normative "
        "terminal result.",
        "Lifecycle Status shall not regress.",
    ):
        assert rule in content


def test_evidence_types_are_declared() -> None:
    content = normalized_text()

    for evidence_type in EVIDENCE_TYPES:
        assert evidence_type in content

    assert "Unknown or private Evidence Types shall be invalid." in content


def test_evidence_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Evidence Identifier.",
        "Evidence Version.",
        "Evidence Type.",
        "Lifecycle Status.",
        "Reasoning Request Identifier.",
        "Reasoning Form.",
        "Reasoning Status.",
        "Reasoning Outcome.",
        "Graph Identifier.",
        "Graph Version.",
        "Execution Context Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Query Language Baseline Reference.",
        "Resolved Fact References.",
        "Resolved Premise References.",
        "Applied Rule References.",
        "Rejected Rule References.",
        "Rule Application References.",
        "Variable Binding References.",
        "Intermediate Conclusion References.",
        "Final Conclusion References.",
        "Proof References.",
        "Proof Step References.",
        "Contradiction References.",
        "Failure Classification.",
        "Failure Reason.",
        "Maximum Reasoning Depth.",
        "Actual Reasoning Depth.",
        "Validation Result.",
        "Evidence Integrity Reference.",
        "Source Evidence References.",
    ):
        assert property_name in content


def test_evidence_scope_is_exactly_one_request() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Evidence artifact shall belong "
        "to exactly one Reasoning Request.",
        "Every Evidence artifact shall remain within one "
        "immutable Reasoning Execution Context.",
        "Evidence shall not combine unrelated Reasoning Requests.",
        "Evidence shall not combine incompatible Graph Versions.",
        "Evidence shall not combine incompatible baseline versions.",
        "Evidence scope shall remain immutable after "
        "construction begins.",
    ):
        assert requirement in content


def test_request_evidence_is_complete() -> None:
    content = normalized_text()

    assert (
        "Every valid or invalid Reasoning Request shall "
        "produce deterministic Request Evidence."
    ) in content

    for property_name in (
        "Reasoning Request Version.",
        "Goal Assertion Reference.",
        "Fact Source References.",
        "Inference Rule References.",
        "Constraint References.",
        "Reasoning Limits.",
        "Closed-World Policy.",
        "Contradiction Policy.",
        "Expected Reasoning Outcome.",
        "Request Validation Result.",
        "Request Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "No Reasoning Request validation shall omit "
        "Request Evidence."
    ) in content


def test_fact_evidence_is_complete() -> None:
    content = normalized_text()

    assert (
        "Every Fact consumed during reasoning shall "
        "possess deterministic Fact Evidence."
    ) in content

    for property_name in (
        "Fact Identifier.",
        "Fact Version.",
        "Fact Type.",
        "Subject.",
        "Predicate.",
        "Object or Literal Value.",
        "Assertion Type.",
        "Assertion Polarity.",
        "Fact Source Reference.",
        "Fact Provenance.",
        "Fact Confidence.",
        "Fact Validation Result.",
        "Fact Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "A Fact without complete Evidence shall not "
        "participate in normative reasoning."
    ) in content


def test_premise_evidence_covers_satisfied_and_unsatisfied() -> None:
    content = normalized_text()

    assert (
        "Every Premise evaluated during reasoning shall "
        "possess deterministic Premise Evidence."
    ) in content

    for property_name in (
        "Premise Identifier.",
        "Premise Version.",
        "Premise Type.",
        "Required Polarity.",
        "Required Source Type.",
        "Referenced Fact References.",
        "Referenced Derived Assertion References.",
        "Premise Priority.",
        "Premise Optionality.",
        "Premise Validation Result.",
        "Premise Satisfaction Result.",
        "Premise Integrity Reference.",
        "Underlying Fact Evidence References.",
    ):
        assert property_name in content

    assert (
        "A satisfied or unsatisfied Premise shall "
        "produce Evidence."
    ) in content


def test_rule_evidence_includes_registered_and_rejected_rules() -> None:
    content = normalized_text()

    assert (
        "Every registered or rejected Inference Rule "
        "shall possess deterministic Rule Evidence."
    ) in content

    for property_name in (
        "Preferred Rule Name.",
        "Rule Registry Reference.",
        "Premise Definitions.",
        "Premise Conjunction.",
        "Variable Definitions.",
        "Variable Binding Rules.",
        "Applicability Constraints.",
        "Conclusion Template.",
        "Maximum Application Count.",
        "Rule Registration Result.",
        "Rule Validation Result.",
        "Rule Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "A rejected Rule shall remain represented in "
        "Evidence when it was considered during reasoning."
    ) in content


def test_every_rule_application_outcome_produces_evidence() -> None:
    content = normalized_text()

    assert (
        "Every attempted Rule Application shall produce "
        "deterministic Rule Application Evidence."
    ) in content

    for property_name in (
        "Rule Application Identifier.",
        "Application Status.",
        "Applicability Result.",
        "Resolved Derived Assertion References.",
        "Variable Bindings.",
        "Applicability Constraint Results.",
        "Current Reasoning Depth.",
        "Rule Application Count.",
        "Produced Conclusion Reference.",
        "Rule Application Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "APPLIED, NOT APPLICABLE, FAILED, and CANCELLED "
        "Rule Applications shall all produce Evidence."
    ) in content


def test_proof_and_proof_step_evidence_are_required() -> None:
    content = normalized_text()

    assert (
        "Every valid or invalid Proof shall possess "
        "deterministic Proof Evidence."
    ) in content

    assert (
        "Every valid or invalid Proof Step shall possess "
        "deterministic Proof Step Evidence."
    ) in content

    assert "No Proof validation shall omit Evidence." in content
    assert (
        "Proof Step Evidence shall preserve dependency ordering."
    ) in content


def test_contradiction_evidence_preserves_both_branches() -> None:
    content = normalized_text()

    assert (
        "Every CONTRADICTED Reasoning Outcome shall "
        "produce deterministic Contradiction Evidence."
    ) in content

    for property_name in (
        "Positive Assertion Reference.",
        "Negative or incompatible Assertion Reference.",
        "Positive Proof Reference.",
        "Negative or incompatible Proof Reference.",
        "Positive Evidence Reference.",
        "Negative or incompatible Evidence Reference.",
        "Contradiction Rule Reference.",
        "Contradiction Policy.",
        "Contradiction Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Both incompatible branches shall remain "
        "independently verifiable."
    ) in content

    assert (
        "Contradiction Evidence shall not delete, "
        "suppress, rewrite, prioritize, or repair either branch."
    ) in content


def test_failure_evidence_is_required() -> None:
    content = normalized_text()

    assert (
        "Every failed or unevaluable reasoning path shall "
        "produce deterministic Failure Evidence."
    ) in content

    for property_name in (
        "Failure Evidence Identifier.",
        "Failed Reasoning Stage.",
        "Failed Artifact Type.",
        "Failed Artifact Identifier.",
        "Failed Validation Rule.",
        "Resolved Inputs.",
        "Unresolved Inputs.",
        "Partial Conclusions.",
        "Partial Proof References.",
        "Failure Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "No failed Reasoning Request shall omit Evidence."
    ) in content


def test_terminal_reasoning_evidence_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every terminal Reasoning Result shall possess "
        "exactly one Terminal Reasoning Evidence artifact."
    ) in content

    for property_name in (
        "Expected Reasoning Outcome.",
        "Expectation Match Result.",
        "Determinism Result.",
        "Result Integrity Reference.",
        "Evidence Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Completed, Failed, and Cancelled terminal "
        "results shall produce Terminal Reasoning Evidence."
    ) in content


def test_reasoning_status_compatibility_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Not Executed shall not possess Terminal "
        "Reasoning Evidence.",
        "Running may possess partial non-terminal Evidence.",
        "Completed shall possess complete terminal Evidence.",
        "Failed shall possess complete Failure Evidence "
        "and Terminal Reasoning Evidence.",
        "Cancelled shall possess deterministic cancellation "
        "Evidence and Terminal Reasoning Evidence.",
        "Terminal Evidence shall not claim Running status.",
        "A terminal status shall not regress.",
    ):
        assert rule in content


def test_reasoning_outcome_compatibility_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "PROVEN shall reference one valid Proof.",
        "DISPROVEN shall reference one valid Proof for "
        "the explicit negation of the Goal.",
        "UNDETERMINED shall preserve the evaluated search "
        "boundary and absence of a valid Proof for either polarity.",
        "CONTRADICTED shall preserve both incompatible Proof branches.",
        "ERROR shall preserve deterministic Failure Evidence.",
        "Evidence shall not alter the actual Reasoning Outcome.",
        "Expected Reasoning Outcome shall remain independent "
        "from actual Reasoning Outcome.",
    ):
        assert rule in content


def test_evidence_construction_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Evidence Construction shall begin only after "
        "the corresponding normative artifact exists.",
        "Evidence Construction shall preserve the exact "
        "artifact state evaluated during reasoning.",
        "Evidence Construction shall not reconstruct "
        "missing inputs through undocumented assumptions.",
        "Evidence Construction shall not repair an invalid artifact.",
        "Evidence Construction shall not change a Reasoning Outcome.",
        "Evidence Construction shall fail closed when "
        "required evidence completeness cannot be established.",
    ):
        assert rule in content


def test_evidence_completeness_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Evidence Identity is valid.",
        "Evidence Version is supported.",
        "Evidence Type is permitted.",
        "Reasoning Request resolves.",
        "Execution Context resolves.",
        "Every consumed Fact has Evidence.",
        "Every evaluated Premise has Evidence.",
        "Every considered Rule has Evidence.",
        "Every attempted Rule Application has Evidence.",
        "Every Variable Binding is represented.",
        "Every intermediate Conclusion is represented.",
        "Every final Conclusion is represented.",
        "Every Proof has Evidence.",
        "Every Proof Step has Evidence.",
        "Every contradiction has Evidence.",
        "Every failure has Evidence.",
        "Evidence Integrity is valid.",
    ):
        assert requirement in content

    assert (
        "Incomplete Evidence shall not support a "
        "normative terminal Reasoning Result."
    ) in content


def test_evidence_closure_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every referenced artifact shall resolve within "
        "the declared Evidence scope or through one "
        "explicit immutable source Evidence reference.",
        "No dangling Evidence reference shall exist.",
        "No implicit Evidence dependency shall exist.",
        "No Evidence artifact shall depend on a future artifact state.",
        "Every derived artifact shall remain traceable "
        "to source Facts and immutable baseline references.",
    ):
        assert rule in content


def test_evidence_chain_is_complete_and_acyclic() -> None:
    content = normalized_text()

    for evidence_kind in (
        "Reasoning Request Evidence.",
        "Fact Evidence.",
        "Premise Evidence.",
        "Rule Evidence.",
        "Rule Application Evidence.",
        "Proof Step Evidence.",
        "Proof Evidence.",
        "Contradiction or Failure Evidence.",
        "Terminal Reasoning Evidence.",
    ):
        assert evidence_kind in content

    for link_property in (
        "Source Evidence Identifier.",
        "Target Evidence Identifier.",
        "Relationship Type.",
        "Chain Position.",
        "Integrity Reference.",
    ):
        assert link_property in content

    assert "Evidence Chain cycles shall be invalid." in content
    assert "Evidence Chain gaps shall cause validation failure." in content


def test_evidence_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Request Evidence shall appear first.",
        "Fact Evidence shall be ordered by: Fact Identifier.",
        "Premise Priority. Then Premise Identifier.",
        "Rule Priority. Then Rule Identifier.",
        "Reasoning Depth. Then Rule Priority. Then Rule Identifier. "
        "Then Rule Application Identifier.",
        "Variable Identifier.",
        "Reasoning Depth. Then Conclusion Identifier.",
        "Proof Step Position. Then Proof Step Identifier.",
        "Proof Evidence shall be ordered by: Proof Identifier.",
        "Failed Reasoning Stage. Then Failed Artifact Identifier.",
        "Terminal Reasoning Evidence shall appear last.",
        "Runtime discovery order shall not affect "
        "normative Evidence ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_evidence_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Evidence Identifier validity.",
        "Evidence Version support.",
        "Lifecycle Status validity.",
        "Evidence Type validity.",
        "Evidence scope validity.",
        "Reasoning Request resolution.",
        "Reasoning Status compatibility.",
        "Reasoning Outcome compatibility.",
        "Fact Evidence completeness.",
        "Premise Evidence completeness.",
        "Rule Evidence completeness.",
        "Rule Application Evidence completeness.",
        "Proof Evidence completeness.",
        "Proof Step Evidence completeness.",
        "Contradiction Evidence completeness.",
        "Failure Evidence completeness.",
        "Terminal Evidence completeness.",
        "Evidence reference closure.",
        "Evidence Chain completeness.",
        "Evidence Chain acyclicity.",
        "Canonical serialization.",
        "Evidence Integrity.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content
    assert (
        "Invalid or incomplete Evidence shall not support "
        "a terminal normative Reasoning Result."
    ) in content


def test_evidence_validation_result_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Evidence Validation shall produce exactly "
        "one deterministic Evidence Validation Result."
    ) in content

    assert (
        "Permitted Evidence Validation Result values are: PASS. FAIL."
    ) in content

    for property_name in (
        "Validation Identifier.",
        "Evidence Identifier.",
        "Evidence Version.",
        "Evidence Type.",
        "Validation Outcome.",
        "Validated Evidence Artifact Count.",
        "Detected Violations.",
        "Failure Classifications.",
        "Failure Reasons.",
        "Validation Evidence Reference.",
        "Validation Integrity Reference.",
    ):
        assert property_name in content


def test_evidence_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Reasoning Evidence artifact shall possess "
        "one deterministic Evidence Integrity Reference."
    ) in content

    assert (
        "Any normative Evidence mutation shall invalidate "
        "Evidence Integrity."
    ) in content


def test_evidence_chain_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Evidence Chain shall possess one "
        "deterministic Chain Integrity Reference."
    ) in content

    for property_name in (
        "Evidence Chain Identifier.",
        "Ordered Evidence References.",
        "Ordered Chain Links.",
        "Source Evidence Identifiers.",
        "Target Evidence Identifiers.",
        "Relationship Types.",
        "Chain Positions.",
        "Terminal Evidence Identifier.",
    ):
        assert property_name in content

    assert (
        "Any missing, reordered, replaced, or mutated "
        "Evidence Chain element shall invalidate Chain Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Preserve every normative Evidence property.",
        "Preserve every normative Evidence Chain property.",
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve Evidence Type.",
        "Preserve Reasoning Status.",
        "Preserve Reasoning Outcome.",
        "Preserve Assertion Polarity.",
        "Preserve Facts.",
        "Preserve Premises.",
        "Preserve Rules.",
        "Preserve Rule Applications.",
        "Preserve Variable Bindings.",
        "Preserve Conclusions.",
        "Preserve Proofs.",
        "Preserve Proof Steps.",
        "Preserve contradictions.",
        "Preserve failures.",
        "Preserve Evidence Chain ordering.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert requirement in content


def test_determinism_is_declared() -> None:
    content = normalized_text()

    assert (
        "Identical valid Reasoning Executions evaluated "
        "against the same immutable baselines, registered "
        "Rule Set, Graph Version, and Execution Context "
        "shall produce normatively identical Reasoning Evidence."
    ) in content

    for property_name in (
        "Evidence Type.",
        "Referenced Facts.",
        "Referenced Premises.",
        "Applied Rules.",
        "Rejected Rules.",
        "Rule Applications.",
        "Variable Bindings.",
        "Intermediate Conclusions.",
        "Final Conclusions.",
        "Proof References.",
        "Proof Step References.",
        "Contradiction References.",
        "Failure Classifications.",
        "Failure Reasons.",
        "Reasoning Status.",
        "Reasoning Outcome.",
        "Evidence ordering.",
        "Evidence Chain.",
        "Evidence Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Execution Timestamp shall not alter normative "
        "Evidence equality."
    ) in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Evidence Identifier is missing, malformed, "
        "duplicated, or improperly reused.",
        "Evidence scope is ambiguous or spans incompatible "
        "Requests, Graph Versions, or baselines.",
        "A consumed Fact lacks valid Evidence.",
        "An evaluated Premise lacks Evidence.",
        "A considered Rule lacks Evidence.",
        "An attempted Rule Application lacks Evidence.",
        "A required Variable Binding is omitted.",
        "An intermediate Conclusion is omitted.",
        "A final Conclusion is omitted.",
        "A Proof lacks Evidence.",
        "A Proof Step lacks Evidence.",
        "A contradiction omits either branch.",
        "A failed reasoning path lacks Failure Evidence.",
        "Terminal Reasoning Evidence is missing.",
        "A dangling Evidence reference exists.",
        "The Evidence Chain is incomplete.",
        "An Evidence Chain cycle exists.",
        "Canonical serialization cannot be produced.",
        "Evidence Integrity cannot be established.",
        "Evidence Chain Integrity cannot be established.",
        "The Evidence attempts to mutate source knowledge "
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
        "Register a Derived Conclusion as a Graph Fact.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Modify a Query Result.",
        "Modify a Reasoning Request.",
        "Modify a Goal Assertion.",
        "Modify a registered Fact.",
        "Modify a registered Premise.",
        "Modify a registered Rule.",
        "Modify a Rule Application.",
        "Modify a Variable Binding.",
        "Modify a Derived Conclusion.",
        "Modify a Proof.",
        "Modify a Proof Step.",
        "Modify an Execution Context.",
        "Repair missing Evidence.",
        "Repair an incomplete Proof.",
        "Resolve a contradiction by deleting Evidence.",
        "Modify HAS Foundation 1.0 LTS.",
        "Modify Specification Runtime 1.0.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Modify CKP-005.1.",
        "Modify CKP-005.2.",
        "Modify CKP-005.3.",
        "Modify CKP-005.4.",
        "Modify CKP-005.5.",
        "Modify CKP-005.6.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_evidence_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in EVIDENCE_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Evidence Identity is valid and unique.",
        "Evidence Version is supported.",
        "Exactly one canonical Evidence Type is declared.",
        "Evidence belongs to exactly one Reasoning Request.",
        "Request Evidence is complete.",
        "Every consumed Fact has complete Evidence.",
        "Every evaluated Premise has complete Evidence.",
        "Every considered Rule has complete Evidence.",
        "Every attempted Rule Application has complete Evidence.",
        "Every Variable Binding is represented.",
        "Every intermediate Conclusion is represented.",
        "Every final Conclusion is represented.",
        "Every Proof has complete Evidence.",
        "Every Proof Step has complete Evidence.",
        "Every contradiction preserves both branches.",
        "Every failure has deterministic Failure Evidence.",
        "Exactly one Terminal Reasoning Evidence artifact "
        "exists for a terminal result.",
        "Evidence reference closure is established.",
        "The Evidence Chain is complete and acyclic.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "Evidence Integrity is valid.",
        "Evidence Chain Integrity is valid.",
        "No Failure Condition remains open.",
        "Evidence does not mutate source knowledge or a "
        "frozen baseline.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Reasoning Evidence Model."
    ) in content

    assert (
        "Future implementations shall preserve this "
        "normative Reasoning Evidence contract."
    ) in content

    for excluded_capability in (
        "Production logging infrastructure.",
        "Telemetry implementation.",
        "Observability platform.",
        "Evidence database.",
        "Evidence transport protocol.",
        "Distributed evidence replication.",
        "Cryptographic algorithm selection.",
        "Evidence user interface.",
        "Evidence visualization.",
        "Automated evidence admission.",
        "Graph mutation.",
        "Ontology mutation.",
        "Machine learning.",
        "Probabilistic evidence.",
    ):
        assert excluded_capability in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.8" in content
    assert "Explanation Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
