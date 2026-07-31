from pathlib import Path


CHARTER = Path(
    "research/commerce/reasoning/"
    "CKP005_COMMERCE_REASONING_CHARTER.md"
)


REASONING_CAPABILITIES = (
    "Fact Resolution.",
    "Premise Validation.",
    "Rule Resolution.",
    "Rule Applicability Validation.",
    "Direct Deduction.",
    "Multi-Step Deduction.",
    "Conjunctive Premises.",
    "Negative Premise Validation.",
    "Relationship Composition.",
    "Hierarchy Reasoning.",
    "Inverse Relationship Reasoning.",
    "Reachability-Based Reasoning.",
    "Constraint Evaluation.",
    "Contradiction Detection.",
    "Proof Construction.",
    "Evidence Construction.",
    "Explanation Construction.",
    "Deterministic Conclusion Ordering.",
    "Reasoning Integrity Validation.",
)


REASONING_FORMS = (
    "DERIVE ASSERTION.",
    "VALIDATE ASSERTION.",
    "EXPLAIN ASSERTION.",
    "PROVE ASSERTION.",
    "DETECT CONTRADICTION.",
)


ASSERTION_TYPES = (
    "Graph Fact Assertion.",
    "Ontology Assertion.",
    "Query Result Assertion.",
    "Derived Assertion.",
    "Constraint Assertion.",
    "Contradiction Assertion.",
)


RULE_TYPES = (
    "DIRECT.",
    "HIERARCHICAL.",
    "INVERSE.",
    "TRANSITIVE.",
    "COMPOSITIONAL.",
    "CONSTRAINT.",
    "CONTRADICTION.",
)


REASONING_OUTCOMES = (
    "PROVEN.",
    "DISPROVEN.",
    "UNDETERMINED.",
    "CONTRADICTED.",
    "ERROR.",
)


FAILURE_CLASSIFICATIONS = (
    "REASONING_REQUEST_IDENTITY_VIOLATION.",
    "REASONING_FORM_VIOLATION.",
    "GOAL_ASSERTION_VIOLATION.",
    "FACT_RESOLUTION_VIOLATION.",
    "PREMISE_RESOLUTION_VIOLATION.",
    "PREMISE_POLARITY_VIOLATION.",
    "RULE_IDENTITY_VIOLATION.",
    "RULE_VERSION_VIOLATION.",
    "RULE_TYPE_VIOLATION.",
    "RULE_APPLICABILITY_VIOLATION.",
    "RULE_PRIORITY_VIOLATION.",
    "VARIABLE_BINDING_VIOLATION.",
    "VARIABLE_TYPE_VIOLATION.",
    "CONCLUSION_VIOLATION.",
    "HIERARCHY_VIOLATION.",
    "INVERSE_RELATIONSHIP_VIOLATION.",
    "TRANSITIVITY_VIOLATION.",
    "COMPOSITION_VIOLATION.",
    "CONSTRAINT_VIOLATION.",
    "CONTRADICTION_VIOLATION.",
    "REASONING_DEPTH_VIOLATION.",
    "RULE_APPLICATION_LIMIT_VIOLATION.",
    "DERIVED_ASSERTION_LIMIT_VIOLATION.",
    "CIRCULAR_DERIVATION_VIOLATION.",
    "PROOF_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "EXPLANATION_VIOLATION.",
    "BASELINE_VIOLATION.",
    "DETERMINISM_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)


REASONING_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Reasoning Request Identity.",
    "Reasoning Request Version Preservation.",
    "Canonical Reasoning Form.",
    "Immutable Goal Assertion.",
    "Explicit Assertion Polarity.",
    "Fact Source Closure.",
    "Premise Reference Closure.",
    "Premise Polarity Compatibility.",
    "Canonical Rule Identity.",
    "Rule Registration Closure.",
    "Rule Type Validity.",
    "Rule Applicability.",
    "Variable Binding Completeness.",
    "Variable Type Compatibility.",
    "Deterministic Rule Ordering.",
    "Deterministic Conclusion Ordering.",
    "Hierarchy Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Explicit Transitivity.",
    "Registered Relationship Composition.",
    "Constraint Integrity.",
    "Contradiction Preservation.",
    "Reasoning Depth Enforcement.",
    "Rule Application Limit Enforcement.",
    "Derived Assertion Limit Enforcement.",
    "Circular Derivation Prohibition.",
    "Proof Completeness.",
    "Proof Step Acyclicity.",
    "Evidence Completeness.",
    "Explanation Consistency.",
    "Expected Outcome Independence.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Query Language Compatibility.",
    "Canonical Serialization.",
    "Reasoning Request Integrity.",
    "Rule Integrity.",
    "Conclusion Integrity.",
    "Proof Integrity.",
    "Evidence Integrity.",
    "Result Integrity.",
    "Deterministic Reasoning.",
    "Fail-Closed Validation.",
    "Semantic Closure.",
    "Traceability Closure.",
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


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Model" in content
    assert "Abbreviation CRM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_vision_is_declared() -> None:
    content = normalized_text()

    assert (
        "Establish a canonical, deterministic, "
        "explainable, reproducible, evidence-producing, "
        "and auditable reasoning model over immutable "
        "Commerce Knowledge Graphs."
    ) in content

    assert (
        "The Commerce Reasoning Model shall allow "
        "registered Commerce assertions to be evaluated "
        "and derived through explicit registered rules "
        "without modifying the source Graph or its "
        "frozen semantic baselines."
    ) in content


def test_mission_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define a technology-independent reasoning "
        "contract over the frozen Commerce Knowledge "
        "Platform baselines.",
        "Deterministic Reasoning Results.",
        "Derived Assertions.",
        "Proof Artifacts.",
        "Reasoning Evidence.",
        "Human-readable Explanations.",
        "Integrity References.",
        "Every conclusion shall remain traceable to its "
        "premises, rules, graph components, baselines, "
        "proof steps, and evidence.",
    ):
        assert requirement in content


def test_immutable_inputs_are_declared() -> None:
    content = normalized_text()

    for baseline in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-004 Commerce Query Language 1.0.",
    ):
        assert baseline in content

    assert "These baselines shall remain immutable." in content


def test_reasoning_boundary_is_read_only() -> None:
    content = normalized_text()

    for rule in (
        "The Commerce Reasoning Model is a read-only "
        "derivation layer.",
        "Reasoning may derive a Reasoning Assertion.",
        "A derived Reasoning Assertion shall not automatically become:",
        "A Canonical Commerce Term.",
        "An Ontology Assertion.",
        "A Graph Node.",
        "A Graph Edge.",
        "A Graph Path.",
        "A frozen Query Result.",
        "A registered baseline fact.",
    ):
        assert rule in content


def test_reasoning_capabilities_are_declared() -> None:
    content = normalized_text()

    for capability in REASONING_CAPABILITIES:
        assert capability in content


def test_reasoning_forms_are_declared() -> None:
    content = normalized_text()

    for reasoning_form in REASONING_FORMS:
        assert reasoning_form in content

    assert (
        "Every Reasoning Request shall declare exactly "
        "one canonical Reasoning Form."
    ) in content

    assert (
        "Unknown or private Reasoning Forms shall be invalid."
    ) in content


def test_reasoning_request_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Reasoning Request Identifier.",
        "Reasoning Request Version.",
        "Lifecycle Status.",
        "Reasoning Form.",
        "Graph Identifier.",
        "Graph Version.",
        "Query Language Version.",
        "Goal Assertion.",
        "Premise References.",
        "Inference Rule References.",
        "Execution Context Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Query Language Baseline Reference.",
        "Maximum Reasoning Depth.",
        "Expected Reasoning Outcome.",
        "Reasoning Request Integrity Reference.",
        "Source Evidence Reference.",
    ):
        assert property_name in content


def test_reasoning_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Request shall possess one "
        "immutable Reasoning Request Identifier.",
        "CKP-REASONING-REQUEST-000001",
        "Reasoning Request Identifiers shall be unique "
        "within one Reasoning Execution Context.",
        "Reasoning Request identity shall remain distinct "
        "from Reasoning Request Version.",
        "A Reasoning Request Identifier shall never be "
        "reused for a different normative Reasoning Request.",
    ):
        assert requirement in content


def test_reasoning_goal_is_explicit() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Request shall declare one "
        "explicit Goal Assertion.",
        "Goal Assertion Identifier.",
        "Subject Identifier.",
        "Predicate Identifier.",
        "Object Identifier or Literal Value.",
        "Assertion Polarity.",
        "Assertion Type.",
        "Graph Scope.",
        "Expected Truth Value.",
        "Goal Integrity Reference.",
        "A Goal Assertion shall not be inferred from "
        "presentation text.",
        "The Goal Assertion shall remain immutable "
        "during reasoning.",
    ):
        assert requirement in content


def test_assertion_model_is_declared() -> None:
    content = normalized_text()

    for assertion_type in ASSERTION_TYPES:
        assert assertion_type in content

    for property_name in (
        "Assertion Identifier.",
        "Assertion Type.",
        "Subject.",
        "Predicate.",
        "Object or Value.",
        "Assertion Polarity.",
        "Source Type.",
        "Source Reference.",
        "Graph Identifier.",
        "Graph Version.",
        "Lifecycle Status.",
        "Assertion Integrity Reference.",
    ):
        assert property_name in content


def test_assertion_polarity_is_explicit() -> None:
    content = normalized_text()

    for value in (
        "POSITIVE.",
        "NEGATIVE.",
    ):
        assert value in content

    for rule in (
        "Assertion Polarity shall be explicit.",
        "Absence of a positive assertion shall not "
        "automatically establish a negative assertion.",
        "Absence of a negative assertion shall not "
        "automatically establish a positive assertion.",
        "Closed-world evaluation shall not be assumed "
        "unless explicitly declared",
    ):
        assert rule in content


def test_fact_sources_are_declared() -> None:
    content = normalized_text()

    for source in (
        "Canonical Vocabulary.",
        "Commerce Ontology.",
        "Commerce Knowledge Graph.",
        "Commerce Query Language Result.",
        "Registered Reasoning Evidence.",
    ):
        assert source in content

    for rule in (
        "Every Fact shall remain traceable to one "
        "resolvable source.",
        "A Fact shall not be created from undocumented assumption.",
        "A Fact shall not be silently corrected during reasoning.",
    ):
        assert rule in content


def test_premises_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Premise Identifier.",
        "Assertion Pattern.",
        "Required Polarity.",
        "Required Source Type.",
        "Variable Bindings.",
        "Premise Priority.",
        "Premise Validation Reference.",
        "Premise Evidence Reference.",
    ):
        assert property_name in content

    assert (
        "Every mandatory Premise shall resolve before "
        "the rule may fire."
    ) in content


def test_inference_rule_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Rule Identifier.",
        "Rule Version.",
        "Preferred Rule Name.",
        "Rule Type.",
        "Lifecycle Status.",
        "Premise Definitions.",
        "Premise Conjunction.",
        "Conclusion Template.",
        "Variable Binding Rules.",
        "Applicability Constraints.",
        "Maximum Application Count.",
        "Rule Priority.",
        "Rule Integrity Reference.",
        "Rule Evidence Reference.",
    ):
        assert property_name in content


def test_initial_rule_types_are_declared() -> None:
    content = normalized_text()

    for rule_type in RULE_TYPES:
        assert rule_type in content

    for rule in (
        "TRANSITIVE derives through a relationship "
        "explicitly declared transitive.",
        "COMPOSITIONAL derives through an explicit "
        "registered relationship composition rule.",
        "CONTRADICTION detects incompatible assertions "
        "without repairing them.",
        "Unknown or private Rule Types shall be invalid.",
    ):
        assert rule in content


def test_rule_registration_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Every Inference Rule shall be registered before use.",
        "One immutable Rule Identifier.",
        "One Rule Version.",
        "One canonical Rule Type.",
        "One deterministic canonical serialization.",
        "One Rule Integrity Reference.",
        "One Rule Validation Evidence Reference.",
        "An unregistered Rule shall not participate in reasoning.",
        "A private runtime rule shall not create a "
        "normative conclusion.",
    ):
        assert requirement in content


def test_rule_applicability_is_fail_closed() -> None:
    content = normalized_text()

    for condition in (
        "The Rule is registered.",
        "Every mandatory Premise resolves.",
        "Premise polarity is compatible.",
        "Variable bindings are complete.",
        "Variable bindings are type-compatible.",
        "Maximum Reasoning Depth is not exceeded.",
        "Maximum Application Count is not exceeded.",
        "Rule Integrity is valid.",
    ):
        assert condition in content

    assert (
        "A Rule shall fail closed when applicability "
        "cannot be established."
    ) in content


def test_premise_conjunction_is_explicit() -> None:
    content = normalized_text()

    for conjunction in (
        "ALL.",
        "ANY.",
    ):
        assert conjunction in content

    for rule in (
        "Premise conjunction shall be explicit.",
        "Conjunction shall not be inferred from "
        "presentation order.",
        "Ambiguous premise grouping shall be invalid.",
    ):
        assert rule in content


def test_variable_binding_is_typed() -> None:
    content = normalized_text()

    for variable_type in (
        "GRAPH NODE IDENTIFIER.",
        "GRAPH EDGE IDENTIFIER.",
        "GRAPH PATH IDENTIFIER.",
        "CANONICAL TERM IDENTIFIER.",
        "RELATIONSHIP TYPE.",
        "TEXT.",
        "INTEGER.",
        "BOOLEAN.",
        "ENUMERATION.",
    ):
        assert variable_type in content

    for rule in (
        "Every variable shall be bound before "
        "conclusion construction.",
        "Implicit type conversion shall be invalid.",
        "A variable binding shall not escape its "
        "Reasoning Request scope.",
    ):
        assert rule in content


def test_conclusion_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Conclusion Identifier.",
        "Rule Identifier.",
        "Rule Version.",
        "Bound Premise References.",
        "Variable Bindings.",
        "Subject.",
        "Predicate.",
        "Object or Value.",
        "Assertion Polarity.",
        "Conclusion Type.",
        "Reasoning Depth.",
        "Proof Reference.",
        "Evidence Reference.",
        "Conclusion Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "A Conclusion shall not automatically enter a "
        "frozen baseline."
    ) in content


def test_reasoning_depth_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Source Facts have Reasoning Depth zero.",
        "A direct Conclusion from source Facts has "
        "Reasoning Depth one.",
        "Maximum Reasoning Depth shall be a non-negative integer.",
        "Reasoning shall not continue beyond Maximum "
        "Reasoning Depth.",
    ):
        assert rule in content


def test_multi_step_reasoning_is_traceable_and_acyclic() -> None:
    content = normalized_text()

    for requirement in (
        "One Conclusion Identifier.",
        "One Rule Application Reference.",
        "One Proof Step.",
        "One Evidence Record.",
        "One Integrity Reference.",
        "Intermediate conclusions shall remain "
        "traceable to source Facts.",
        "Circular derivation shall be invalid.",
        "A Rule shall not use its own unsupported "
        "Conclusion as a Premise.",
    ):
        assert requirement in content


def test_hierarchy_inverse_transitive_and_composition_rules_are_bounded() -> None:
    content = normalized_text()

    for rule in (
        "Hierarchy Reasoning shall use only registered "
        "hierarchy relationships.",
        "Hierarchy reasoning shall preserve canonical direction.",
        "Inverse Relationship Reasoning shall require "
        "one registered canonical inverse relationship.",
        "A unidirectional relationship shall not be "
        "silently treated as inverse-paired.",
        "Transitive Reasoning shall apply only to a "
        "Relationship Type explicitly registered as transitive.",
        "An undocumented relationship composition shall be invalid.",
    ):
        assert rule in content


def test_constraint_and_contradiction_reasoning_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Constraint Identifier.",
        "Constraint Type.",
        "Subject Scope.",
        "Required Assertions.",
        "Forbidden Assertions.",
        "Cardinality Rules.",
        "Value Rules.",
        "Graph Scope.",
        "Failure Classification.",
        "Constraint Integrity Reference.",
    ):
        assert property_name in content

    for rule in (
        "Constraint evaluation shall not repair violations.",
        "A contradiction exists only when an explicit "
        "registered Contradiction Rule is satisfied.",
        "Contradiction Detection shall not delete, "
        "rewrite, prioritize, or repair assertions.",
    ):
        assert rule in content


def test_reasoning_outcomes_are_declared() -> None:
    content = normalized_text()

    for outcome in REASONING_OUTCOMES:
        assert outcome in content

    for rule in (
        "PROVEN means the Goal Assertion is supported "
        "by a valid deterministic Proof.",
        "DISPROVEN means the explicit negation of the "
        "Goal is supported by a valid deterministic Proof.",
        "CONTRADICTED means both the Goal and its "
        "explicit negation are supported.",
        "UNDETERMINED shall not be converted into DISPROVEN.",
        "ERROR shall not be converted into UNDETERMINED.",
    ):
        assert rule in content


def test_reasoning_status_transitions_are_declared() -> None:
    content = normalized_text()

    for transition in (
        "Not Executed to Running.",
        "Running to Completed.",
        "Running to Failed.",
        "Running to Cancelled.",
    ):
        assert transition in content

    assert (
        "Completed, Failed, and Cancelled are terminal statuses."
    ) in content


def test_proof_requirement_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every PROVEN or DISPROVEN Reasoning Outcome "
        "shall possess one deterministic Proof Artifact.",
        "Every CONTRADICTED outcome shall possess "
        "proofs for both incompatible conclusions.",
        "No conclusion shall be PROVEN without a valid "
        "Proof Artifact.",
    ):
        assert rule in content

    for property_name in (
        "Proof Identifier.",
        "Reasoning Request Identifier.",
        "Goal Assertion Identifier.",
        "Conclusion Identifier.",
        "Ordered Proof Steps.",
        "Source Fact References.",
        "Rule Application References.",
        "Variable Bindings.",
        "Reasoning Depth.",
        "Proof Validation Result.",
        "Proof Integrity Reference.",
    ):
        assert property_name in content


def test_proof_steps_are_ordered_and_acyclic() -> None:
    content = normalized_text()

    for rule in (
        "Proof Step Position shall be deterministic "
        "and unique within one Proof Artifact.",
        "A Proof Step shall not depend on a later Proof Step.",
        "Circular Proof dependencies shall be invalid.",
    ):
        assert rule in content


def test_reasoning_evidence_is_declared() -> None:
    content = normalized_text()

    for field_name in (
        "Evidence Identifier.",
        "Reasoning Request Identifier.",
        "Reasoning Form.",
        "Resolved Facts.",
        "Resolved Premises.",
        "Applied Rules.",
        "Rejected Rules.",
        "Variable Bindings.",
        "Intermediate Conclusions.",
        "Final Conclusions.",
        "Proof References.",
        "Contradiction References.",
        "Reasoning Outcome.",
        "Reasoning Status.",
        "Maximum Reasoning Depth.",
        "Actual Reasoning Depth.",
        "Determinism Result.",
        "Validation Result.",
        "Failure Classification.",
        "Failure Reason.",
        "Result Hash.",
        "Evidence Integrity Reference.",
    ):
        assert field_name in content


def test_failed_reasoning_still_produces_evidence() -> None:
    content = normalized_text()

    for rule in (
        "A failed Reasoning Request shall still produce "
        "Reasoning Evidence.",
        "The failed validation rule.",
        "The failed reasoning stage.",
        "The deterministic Failure Classification.",
        "The deterministic Failure Reason.",
        "No failed Reasoning Request shall omit evidence.",
    ):
        assert rule in content


def test_explanation_is_derived_from_proof_and_evidence() -> None:
    content = normalized_text()

    for rule in (
        "Every terminal Reasoning Result shall produce "
        "one Explanation Artifact.",
        "An Explanation shall remain derived from the "
        "Proof and Reasoning Evidence.",
        "An Explanation shall not introduce a Fact, "
        "Rule, Premise, Conclusion, or semantic meaning "
        "absent from the Proof and Evidence.",
    ):
        assert rule in content


def test_reasoning_determinism_is_declared() -> None:
    content = normalized_text()

    assert (
        "Identical valid Reasoning Requests evaluated "
        "against the same immutable baselines, registered "
        "Rule Set, Graph Version, and Reasoning Execution "
        "Context shall produce identical normative "
        "terminal results."
    ) in content

    assert (
        "Execution Timestamp shall not alter normative "
        "Reasoning Result equality."
    ) in content


def test_rule_and_conclusion_ordering_are_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Rule Priority.",
        "Then Rule Identifier.",
        "Lower numeric Rule Priority shall be evaluated "
        "before higher numeric Rule Priority.",
        "Runtime discovery order shall not alter "
        "normative reasoning results.",
        "Derived Assertions shall be ordered by:",
        "Reasoning Depth.",
        "Conclusion ordering shall be deterministic.",
    ):
        assert rule in content


def test_execution_context_is_immutable() -> None:
    content = normalized_text()

    for property_name in (
        "Execution Identifier.",
        "Graph Identifier.",
        "Graph Version.",
        "Vocabulary Baseline.",
        "Ontology Baseline.",
        "Graph Baseline.",
        "Query Language Baseline.",
        "Fact Registry Reference.",
        "Rule Registry Reference.",
        "Constraint Registry Reference.",
        "Maximum Reasoning Depth.",
        "Maximum Rule Applications.",
        "Maximum Derived Assertions.",
        "Closed-World Policy.",
        "Contradiction Policy.",
        "Execution Timestamp.",
    ):
        assert property_name in content

    assert (
        "The Reasoning Execution Context shall remain "
        "immutable during evaluation."
    ) in content


def test_closed_world_policy_is_explicit() -> None:
    content = normalized_text()

    for policy in (
        "OPEN WORLD.",
        "EXPLICIT CLOSED WORLD.",
    ):
        assert policy in content

    for rule in (
        "OPEN WORLD shall treat absence of evidence as "
        "insufficient to establish negation.",
        "Closed-world behavior shall never be inferred implicitly.",
    ):
        assert rule in content


def test_contradiction_policy_is_explicit() -> None:
    content = normalized_text()

    for policy in (
        "REPORT.",
        "FAIL.",
    ):
        assert policy in content

    assert (
        "Contradiction Policy shall not delete or "
        "rewrite conflicting assertions."
    ) in content


def test_reasoning_validation_stages_are_declared() -> None:
    content = normalized_text()

    for stage in (
        "Pre-Reasoning Validation shall verify:",
        "During-Reasoning Validation shall verify:",
        "Post-Reasoning Validation shall verify:",
    ):
        assert stage in content

    for validation in (
        "Reasoning Request completeness.",
        "Rule Registry resolution.",
        "Rule applicability.",
        "Variable binding completeness.",
        "Reasoning Depth boundary.",
        "Proof completeness.",
        "Evidence completeness.",
        "Explanation consistency.",
        "Determinism.",
        "Result Integrity.",
    ):
        assert validation in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic identifier ordering.",
        "Preserve Premise grouping.",
        "Preserve Rule Priority.",
        "Preserve variable bindings.",
        "Preserve Proof Step ordering.",
        "Preserve Reasoning Depth.",
        "Preserve Assertion Polarity.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert rule in content


def test_reasoning_integrity_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Reasoning Request shall possess one "
        "deterministic Reasoning Request Integrity Reference.",
        "Every registered Inference Rule shall possess "
        "one deterministic Rule Integrity Reference.",
        "Every Derived Assertion shall possess one "
        "deterministic Conclusion Integrity Reference.",
        "Every Proof shall possess one deterministic "
        "Proof Integrity Reference.",
        "Every Reasoning Evidence record shall possess "
        "one deterministic Evidence Integrity Reference.",
        "Every terminal Reasoning Result shall possess "
        "one deterministic Result Integrity Reference.",
    ):
        assert rule in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Reasoning Request is incomplete.",
        "The Reasoning Form is unknown or private.",
        "The Goal Assertion is missing or invalid.",
        "A required Fact cannot be resolved.",
        "A mandatory Premise cannot be resolved.",
        "An Inference Rule is unregistered.",
        "A required variable is unbound.",
        "Transitivity is applied to a non-transitive "
        "Relationship Type.",
        "An undocumented relationship composition is attempted.",
        "Maximum Reasoning Depth is exceeded.",
        "A circular derivation is detected.",
        "A Proof cannot be constructed.",
        "Reasoning Evidence cannot be produced.",
        "Deterministic reasoning cannot be established.",
        "The Reasoning Request attempts to mutate a "
        "frozen baseline.",
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
        "Register a Derived Assertion as a Graph Fact.",
        "Delete a Canonical Commerce Term.",
        "Delete an Ontology Assertion.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Modify a Query Result.",
        "Repair a missing Fact.",
        "Repair a broken relationship.",
        "Repair a disconnected path.",
        "Resolve a contradiction by deleting evidence.",
        "Modify HAS Foundation 1.0 LTS.",
        "Modify Specification Runtime 1.0.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_non_goals_are_declared() -> None:
    content = normalized_text()

    for non_goal in (
        "Implement a production reasoning engine.",
        "Implement a parser.",
        "Implement a compiler.",
        "Implement an unrestricted rule language.",
        "Implement machine learning.",
        "Implement probabilistic inference.",
        "Implement fuzzy logic.",
        "Implement autonomous ontology modification.",
        "Implement autonomous graph modification.",
        "Implement automated baseline admission.",
        "Replace CQL.",
        "Redefine frozen Commerce semantics.",
    ):
        assert non_goal in content


def test_reasoning_principles_are_declared() -> None:
    content = normalized_text()

    for principle in (
        "Explicit facts before assumptions.",
        "Registered rules before derivation.",
        "Explicit negation before negative conclusions.",
        "Rule applicability before rule execution.",
        "Deterministic ordering before conclusion construction.",
        "Proof before PROVEN.",
        "Evidence for every terminal result.",
        "Explanation derived from Proof and Evidence.",
        "Contradictions reported, not repaired.",
        "Read-only reasoning over immutable baselines.",
        "Fail-closed validation.",
    ):
        assert principle in content


def test_reasoning_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in REASONING_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Every Reasoning Request references immutable baselines.",
        "Every Reasoning Request declares one canonical "
        "Reasoning Form.",
        "Every Goal Assertion is explicit.",
        "Every Fact is source-resolvable.",
        "Every mandatory Premise is validated.",
        "Every applied Rule is registered.",
        "Every variable binding is complete and typed.",
        "Every Conclusion identifies its applied Rule "
        "and supporting Premises.",
        "Every PROVEN or DISPROVEN outcome possesses a valid Proof.",
        "Every CONTRADICTED outcome preserves both proofs.",
        "Every terminal result produces Reasoning Evidence.",
        "Every terminal result produces an Explanation.",
        "Every Derived Assertion remains outside the "
        "frozen Graph unless separately admitted.",
        "Reasoning is deterministic and auditable.",
        "No Reasoning Request mutates a frozen baseline.",
    ):
        assert criterion in content


def test_deliverables_are_declared() -> None:
    content = normalized_text()

    for deliverable in (
        "Commerce Reasoning Charter.",
        "Reasoning Structure Model.",
        "Reasoning Request Model.",
        "Inference Rule Model.",
        "Fact and Premise Model.",
        "Derived Assertion Model.",
        "Proof Model.",
        "Reasoning Evidence Model.",
        "Explanation Model.",
        "Initial Executable Reasoning Cases.",
        "Reasoning Consistency Audit.",
        "Commerce Reasoning Freeze.",
    ):
        assert deliverable in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005 shall remain specification-first." in content

    assert (
        "No production reasoning engine, rule runtime, "
        "graph mutation capability, autonomous admission "
        "mechanism, parser, compiler, or network interface "
        "shall be implemented before the normative reasoning "
        "models and executable specification contracts are complete."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.2" in content
    assert "Reasoning Structure Model." in content
