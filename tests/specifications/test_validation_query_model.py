from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "VALIDATION_QUERY_MODEL.md"
)

VALIDATION_TYPES = (
    "EXISTS.",
    "REACHABLE.",
    "RELATIONSHIP.",
    "PATH.",
)

FAILURE_CLASSIFICATIONS = (
    "VALIDATION_QUERY_IDENTITY_VIOLATION.",
    "VALIDATION_TYPE_VIOLATION.",
    "QUERY_FORM_COMPATIBILITY_VIOLATION.",
    "SUBJECT_VIOLATION.",
    "OBJECT_VIOLATION.",
    "EXPECTED_RESULT_VIOLATION.",
    "GRAPH_TARGET_VIOLATION.",
    "REGISTRY_CLOSURE_VIOLATION.",
    "GRAPH_CLOSURE_VIOLATION.",
    "DIRECTION_VIOLATION.",
    "RELATIONSHIP_TYPE_VIOLATION.",
    "INVERSE_RELATIONSHIP_VIOLATION.",
    "MAXIMUM_DEPTH_VIOLATION.",
    "TRAVERSAL_STRATEGY_VIOLATION.",
    "REACHABILITY_VIOLATION.",
    "PATH_MODE_VIOLATION.",
    "PATH_REGISTRATION_VIOLATION.",
    "PATH_SEQUENCE_VIOLATION.",
    "PATH_CONTINUITY_VIOLATION.",
    "PATH_LENGTH_VIOLATION.",
    "IMPLICIT_EDGE_VIOLATION.",
    "BASELINE_VIOLATION.",
    "DETERMINISM_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "VALIDATION_INTEGRITY_VIOLATION.",
    "RESULT_INTEGRITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Validation Query Identity.",
    "Canonical Validation Type.",
    "Query Form Compatibility.",
    "Immutable Graph Target.",
    "Subject Registration Closure.",
    "Object Registration Closure.",
    "Expected Result Independence.",
    "Validation Outcome Integrity.",
    "Expectation Match Integrity.",
    "EXISTS Registry Closure.",
    "Reachability Direction Preservation.",
    "Reachability Maximum Depth Enforcement.",
    "Reachability Witness Continuity.",
    "Canonical Relationship Type Preservation.",
    "Direct Relationship Semantics.",
    "Inverse Relationship Consistency.",
    "Path Mode Validity.",
    "Registered Path Closure.",
    "Composed Path Non-Registration.",
    "Path Sequence Cardinality.",
    "Path Continuity.",
    "Path Length Integrity.",
    "No Implicit Edges.",
    "Deterministic Witness Selection.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Validation Query Integrity.",
    "Validation Result Integrity.",
    "Canonical Serialization.",
    "Validation Evidence Completeness.",
    "Deterministic Validation.",
    "Fail-Closed Evaluation.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_validation_query_model_exists() -> None:
    assert MODEL.is_file()


def test_validation_query_is_read_only() -> None:
    content = normalized_text()

    for rule in (
        "A Validation Query is one explicit, "
        "deterministic, read-only request",
        "Validation Queries shall remain read-only.",
        "Validation Queries shall not create, modify, "
        "infer, repair, or redefine canonical Commerce knowledge.",
    ):
        assert rule in content


def test_validation_query_identity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Validation Query shall possess one "
        "immutable Validation Query Identifier.",
        "CKP-VALIDATION-QUERY-000001",
        "Validation Query Identifiers shall be unique "
        "within one Execution Context.",
        "A Validation Query Identifier shall never be "
        "reused for a different normative Validation Query.",
    ):
        assert rule in content


def test_validation_types_are_declared() -> None:
    content = normalized_text()

    for validation_type in VALIDATION_TYPES:
        assert validation_type in content

    assert (
        "Every Validation Query shall declare exactly "
        "one Validation Type."
    ) in content


def test_query_form_compatibility_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "VALIDATE EXISTS shall use Validation Type EXISTS.",
        "VALIDATE REACHABLE shall use Validation Type REACHABLE.",
        "VALIDATE RELATIONSHIP shall use Validation Type RELATIONSHIP.",
        "VALIDATE PATH shall use Validation Type PATH.",
        "SELECT Query Forms shall not be interpreted "
        "as Validation Query Forms.",
    ):
        assert rule in content


def test_subject_and_object_are_defined() -> None:
    content = normalized_text()

    for component_type in (
        "Graph Node.",
        "Graph Edge.",
        "Graph Path.",
    ):
        assert component_type in content

    for rule in (
        "Every Validation Query shall declare one "
        "Validation Subject.",
        "REACHABLE requires one Object Graph Node.",
        "RELATIONSHIP requires one Object Graph Node.",
        "EXISTS may omit Validation Object.",
        "A missing required Validation Object shall "
        "cause validation failure.",
    ):
        assert rule in content


def test_expected_result_is_independent() -> None:
    content = normalized_text()

    for rule in (
        "Permitted Expected Result values are: TRUE. FALSE.",
        "Expected Result shall not influence graph evaluation.",
        "The actual Validation Outcome shall be "
        "calculated independently.",
    ):
        assert rule in content


def test_validation_outcomes_are_defined() -> None:
    content = normalized_text()

    for value in (
        "TRUE.",
        "FALSE.",
        "ERROR.",
    ):
        assert value in content

    assert "ERROR shall cause fail-closed evaluation." in content


def test_validation_status_is_defined() -> None:
    content = normalized_text()

    for transition in (
        "Not Executed to Running.",
        "Running to Completed.",
        "Running to Failed.",
        "Running to Cancelled.",
    ):
        assert transition in content


def test_exists_validation_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "EXISTS validates whether one declared Graph "
        "Component is registered",
        "EXISTS shall not require Validation Object.",
        "EXISTS shall not perform semantic inference.",
        "EXISTS shall return TRUE when:",
        "EXISTS shall return FALSE when:",
        "EXISTS shall return ERROR when:",
    ):
        assert rule in content


def test_exists_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Registry Resolution Result.",
        "Registration Lookup Result.",
        "Graph Membership Result.",
        "Expectation Match Result.",
    ):
        assert field_name in content


def test_reachable_validation_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "REACHABLE validates whether one registered "
        "Subject Graph Node can reach one registered "
        "Object Graph Node",
        "REACHABLE shall not infer undocumented Graph Edges.",
        "REACHABLE shall return TRUE when at least one "
        "continuous permitted path exists",
        "REACHABLE shall return FALSE when Subject and "
        "Object are registered but no permitted path exists",
    ):
        assert rule in content


def test_reachability_direction_and_strategy_are_defined() -> None:
    content = normalized_text()

    for value in (
        "FORWARD.",
        "REVERSE.",
        "BIDIRECTIONAL.",
        "HIERARCHY.",
        "SEMANTIC.",
        "MIXED.",
    ):
        assert value in content

    assert (
        "BIDIRECTIONAL shall not reinterpret a "
        "Unidirectional Graph Edge as bidirectional."
    ) in content


def test_reachability_depth_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Maximum Depth shall be a non-negative integer.",
        "Maximum Depth shall not exceed the Maximum "
        "Validation Depth declared by Execution Context.",
        "Maximum Depth shall count traversed Graph Edges.",
        "Traversal shall not continue beyond Maximum Depth.",
    ):
        assert rule in content


def test_reachability_witness_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Witness Path Identifier.",
        "Ordered Node Sequence.",
        "Ordered Edge Sequence.",
        "Traversal Direction.",
        "Traversal Strategy.",
        "Path Length.",
        "Path Continuity Result.",
        "Path Integrity Reference.",
    ):
        assert field_name in content


def test_relationship_validation_is_direct() -> None:
    content = normalized_text()

    for rule in (
        "RELATIONSHIP validates whether one explicit "
        "canonical direct relationship exists",
        "RELATIONSHIP validates a direct Graph Edge.",
        "RELATIONSHIP shall not validate transitive reachability.",
        "RELATIONSHIP shall not infer undocumented relationships.",
    ):
        assert rule in content


def test_canonical_relationship_types_are_declared() -> None:
    content = normalized_text()

    for relationship_type in (
        "Is A.",
        "Part Of.",
        "Contains.",
        "Tracked As.",
        "Uses.",
        "Used By.",
        "Sold Through.",
        "Applies To.",
    ):
        assert relationship_type in content


def test_relationship_direction_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "FORWARD validates an edge from Subject to Object.",
        "Source and Target roles shall remain explicit.",
        "A Subject Node shall not be silently treated "
        "as an Object Node.",
        "A required inverse relationship is inconsistent.",
    ):
        assert rule in content


def test_path_validation_modes_are_defined() -> None:
    content = normalized_text()

    for mode in (
        "REGISTERED PATH mode.",
        "COMPOSED PATH mode.",
    ):
        assert mode in content

    assert (
        "Every PATH Validation Query shall declare "
        "exactly one Path Validation Mode."
    ) in content


def test_composed_path_does_not_register() -> None:
    content = normalized_text()

    assert (
        "A composed path shall not become a registered "
        "canonical Graph Path merely by being validated."
    ) in content


def test_path_continuity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Ordered Node Sequence contains exactly one "
        "more element than Ordered Edge Sequence.",
        "Every edge connects the corresponding adjacent node pair.",
        "The first node equals Start Node Identifier.",
        "The final node equals End Node Identifier.",
        "Declared Path Length equals the number of ordered edges.",
        "No implicit Graph Edge participates in the path.",
    ):
        assert rule in content


def test_expectation_match_is_defined() -> None:
    content = normalized_text()

    for value in (
        "MATCH.",
        "MISMATCH.",
        "NOT EVALUATED.",
    ):
        assert value in content

    assert (
        "Expectation mismatch shall not change the "
        "actual Validation Outcome."
    ) in content


def test_validation_query_result_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Validation Query Identifier.",
        "Validation Type.",
        "Validation Status.",
        "Validation Outcome.",
        "Expected Result.",
        "Expectation Match Result.",
        "Matched Component Identifiers.",
        "Witness Path Identifiers.",
        "Validation Query Evidence Reference.",
        "Validation Result Integrity Reference.",
    ):
        assert field_name in content


def test_validation_evidence_is_required_for_all_outcomes() -> None:
    content = normalized_text()

    assert (
        "Every successful, false, failed, or cancelled "
        "Validation Query shall produce deterministic "
        "Validation Query Evidence."
    ) in content


def test_integrity_models_are_defined() -> None:
    content = normalized_text()

    assert (
        "Every Validation Query shall possess one "
        "deterministic Validation Query Integrity Reference."
    ) in content

    assert (
        "Every terminal Validation Query Result shall "
        "possess one deterministic Validation Result "
        "Integrity Reference."
    ) in content


def test_deterministic_validation_is_defined() -> None:
    content = normalized_text()

    assert (
        "Identical valid Validation Queries executed "
        "against the same immutable Graph Version and "
        "Execution Context shall produce identical "
        "terminal normative results."
    ) in content


def test_canonical_serialization_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic identifier ordering.",
        "Preserve path ordering.",
        "Preserve direction and Maximum Depth.",
        "Exclude non-normative presentation metadata.",
    ):
        assert rule in content


def test_validation_execution_order_is_defined() -> None:
    content = normalized_text()

    for stage in (
        "Validation Query Manifest Validation.",
        "Baseline Validation.",
        "Graph Manifest Resolution.",
        "Query Form Validation.",
        "Validation Type Validation.",
        "Subject Resolution.",
        "Object Resolution when required.",
        "Direction Validation.",
        "Validation Evaluation.",
        "Expected Result Comparison.",
        "Validation Result Construction.",
        "Evidence Construction.",
        "Integrity Construction.",
        "Terminal Status Validation.",
    ):
        assert stage in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Query Form and Validation Type are incompatible.",
        "Expected Result is missing or invalid.",
        "A required Validation Object is missing, "
        "malformed, or unresolved.",
        "A required inverse relationship is missing or inconsistent.",
        "Maximum Depth exceeds the Execution Context boundary.",
        "A registered Path Identifier cannot be resolved.",
        "A path contains a disconnected node pair.",
        "An implicit Graph Edge is required.",
        "Validation Query Evidence cannot be produced.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Register a composed Graph Path.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Repair a missing Graph Component.",
        "Repair a broken inverse relationship.",
        "Repair a disconnected path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Validation Query shall be read-only.",
        "Every Validation Query shall declare exactly "
        "one canonical Validation Type.",
        "Every Validation Query shall declare one "
        "Validation Subject.",
        "Every Expected Result shall be explicit.",
        "Every witness path shall be continuous.",
        "Every Validation Outcome shall be calculated "
        "independently from Expected Result.",
        "No invalid Validation Query shall execute.",
    ):
        assert constraint in content


def test_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Validation Query is explicitly defined.",
        "Validation Query Identity is explicitly defined.",
        "Validation Types and Query Form compatibility "
        "are explicitly defined.",
        "EXISTS validation, evaluation, and evidence "
        "are explicitly defined.",
        "REACHABLE validation, direction, strategy, "
        "depth, evaluation, witness paths, and evidence "
        "are explicitly defined.",
        "RELATIONSHIP validation, canonical types, "
        "direction, evaluation, and evidence are "
        "explicitly defined.",
        "PATH validation, registered and composed modes, "
        "continuity, evaluation, and evidence are "
        "explicitly defined.",
        "Deterministic Validation is explicitly defined.",
        "Read-Only Boundary is declared.",
        "Validation Query Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.8" in content
    assert "Initial Executable Queries." in content
