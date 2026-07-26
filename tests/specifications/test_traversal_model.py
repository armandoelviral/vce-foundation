from pathlib import Path


MODEL = Path(
    "research/commerce/knowledge_graph/"
    "TRAVERSAL_MODEL.md"
)

REQUEST_PROPERTIES = (
    "Request Identifier.",
    "Graph Identifier.",
    "Graph Version.",
    "Start Node Identifier.",
    "Target Node Identifier.",
    "Traversal Strategy.",
    "Traversal Direction.",
    "Relationship Type Filter.",
    "Node Type Filter.",
    "Domain Filter.",
    "Lifecycle Filter.",
    "Maximum Depth.",
    "Execution Context.",
    "Vocabulary Baseline Reference.",
    "Ontology Baseline Reference.",
)

TRAVERSAL_STRATEGIES = (
    "Hierarchy Traversal.",
    "Semantic Traversal.",
    "Mixed Traversal.",
)

TRAVERSAL_DIRECTIONS = (
    "Forward.",
    "Reverse.",
    "Bidirectional.",
)

TRAVERSAL_STATUSES = (
    "Not Executed.",
    "Running.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

TRAVERSAL_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Registered Node Closure.",
    "Registered Edge Closure.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Hierarchy Acyclicity.",
    "Maximum Depth Enforcement.",
    "Constraint Enforcement.",
    "Filter Enforcement.",
    "Path Continuity.",
    "Deterministic Ordering.",
    "Deterministic Traversal.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Traversal Evidence Completeness.",
    "Result Integrity.",
    "Terminal Status Consistency.",
)

EVIDENCE_FIELDS = (
    "Evidence Identifier.",
    "Request Identifier.",
    "Graph Identifier.",
    "Graph Version.",
    "Start Node Identifier.",
    "Target Node Identifier.",
    "Traversal Strategy.",
    "Traversal Direction.",
    "Maximum Depth.",
    "Applied Constraints.",
    "Applied Filters.",
    "Visited Node Sequence.",
    "Traversed Edge Sequence.",
    "Matched Path Identifiers.",
    "Direction Validation Result.",
    "Registry Closure Result.",
    "Edge Closure Result.",
    "Path Continuity Result.",
    "Determinism Result.",
    "Result Hash.",
    "Validation Result.",
    "Failure Reason.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_traversal_model_exists() -> None:
    assert MODEL.is_file()


def test_traversal_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal is one deterministic navigation "
        "operation over a registered Commerce Knowledge Graph."
    ) in content

    for rule in (
        "Begin from one registered Start Node.",
        "Use only registered Graph Edges.",
        "Preserve canonical edge direction.",
        "Respect declared Traversal Constraints.",
        "Produce one deterministic Traversal Result.",
        "Produce Traversal Evidence.",
    ):
        assert rule in content


def test_traversal_request_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal Request defines one explicit "
        "navigation operation."
    ) in content

    for property_name in REQUEST_PROPERTIES:
        assert property_name in model_text()


def test_request_identity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Traversal Request shall possess one "
        "immutable Request Identifier."
    ) in content

    assert "CKP-TRAVERSAL-REQUEST-000001" in content

    assert (
        "Request Identifiers shall be unique within "
        "one execution context."
    ) in content


def test_start_and_target_node_behavior_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Traversal Request shall declare one "
        "registered Start Node Identifier.",
        "An unregistered Start Node shall cause the "
        "Traversal to fail before navigation begins.",
        "A Traversal Request may declare one Target "
        "Node Identifier.",
        "A traversal without a Target Node may return "
        "all nodes satisfying its declared constraints.",
        "An unregistered Target Node shall cause the "
        "Traversal to fail before navigation begins.",
    ):
        assert rule in content


def test_traversal_context_is_defined() -> None:
    content = normalized_text()

    assert (
        "Traversal Context defines the immutable "
        "execution boundary of one Traversal Request."
    ) in content

    for property_name in (
        "Graph Identifier.",
        "Graph Version.",
        "Vocabulary Baseline.",
        "Ontology Baseline.",
        "Node Registry Reference.",
        "Edge Registry Reference.",
        "Execution Identifier.",
        "Execution Timestamp.",
        "Maximum Allowed Depth.",
    ):
        assert property_name in model_text()


def test_context_immutability_is_defined() -> None:
    content = normalized_text()

    assert (
        "Traversal Context shall remain immutable "
        "during execution."
    ) in content

    assert (
        "A Traversal shall not switch Graph Version, "
        "Vocabulary Baseline, Ontology Baseline, Node "
        "Registry, or Edge Registry after execution begins."
    ) in content


def test_traversal_strategies_are_defined() -> None:
    content = model_text()

    for strategy in TRAVERSAL_STRATEGIES:
        assert strategy in content

    normalized = normalized_text()

    assert (
        "Hierarchy Traversal shall navigate only "
        "canonical hierarchy Graph Edges."
    ) in normalized

    assert (
        "Semantic Traversal shall navigate canonical "
        "non-hierarchy Graph Edges."
    ) in normalized

    assert (
        "Mixed Traversal may navigate hierarchy and "
        "semantic Graph Edges."
    ) in normalized


def test_traversal_directions_are_defined() -> None:
    content = model_text()

    for direction in TRAVERSAL_DIRECTIONS:
        assert direction in content


def test_direction_semantics_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Forward Traversal shall navigate from the "
        "Source Node of a Graph Edge to its Target Node.",
        "Reverse Traversal shall navigate against the "
        "stored Source-to-Target direction only when:",
        "Reverse Traversal shall not mutate the "
        "original Graph Edge.",
        "Reverse Traversal shall not create a new "
        "semantic assertion.",
        "Bidirectional Traversal shall not treat a "
        "Unidirectional Graph Edge as implicitly bidirectional.",
    ):
        assert rule in content


def test_traversal_constraints_are_defined() -> None:
    content = model_text()

    for constraint in (
        "Maximum Depth.",
        "Allowed Relationship Types.",
        "Forbidden Relationship Types.",
        "Allowed Node Types.",
        "Forbidden Node Types.",
        "Domain Filter.",
        "Lifecycle Filter.",
        "Vocabulary Baseline.",
        "Ontology Baseline.",
        "Registered Node Closure.",
        "Registered Edge Closure.",
        "Direction Preservation.",
    ):
        assert constraint in content


def test_constraint_precedence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Forbidden constraints shall take precedence "
        "over allowed constraints."
    ) in content

    assert (
        "Baseline compatibility constraints shall not "
        "be overridden."
    ) in content


def test_traversal_depth_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Traversal Depth represents the number of "
        "Graph Edges traversed from the Start Node.",
        "The Start Node has depth zero.",
        "Every traversed Graph Edge increases depth by one.",
        "Traversal shall not exceed the declared Maximum Depth.",
        "A negative Maximum Depth shall be invalid.",
        "Maximum Depth zero shall permit validation of "
        "the Start Node without traversing an edge.",
    ):
        assert rule in content


def test_maximum_depth_boundary_is_defined() -> None:
    content = normalized_text()

    assert (
        "The Traversal Request Maximum Depth shall not "
        "exceed the Traversal Context Maximum Allowed Depth."
    ) in content

    assert (
        "If Request Maximum Depth exceeds Context "
        "Maximum Allowed Depth, the Traversal shall "
        "fail before navigation begins."
    ) in content


def test_traversal_filters_are_defined() -> None:
    content = model_text()

    for filter_name in (
        "Relationship Type Filter.",
        "Node Type Filter.",
        "Domain Filter.",
        "Lifecycle Filter.",
        "Target Node Filter.",
    ):
        assert filter_name in content

    normalized = normalized_text()

    assert (
        "An unknown or private Relationship Type shall "
        "cause validation failure."
    ) in normalized

    assert (
        "Domain filtering shall not redefine or infer "
        "Domain Membership."
    ) in normalized


def test_traversal_ordering_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Traversal ordering shall be deterministic.",
        "Graph Nodes shall be ordered by Canonical "
        "Identifier.",
        "Graph Edges shall be ordered by Relationship "
        "Identifier.",
        "Identical Traversal Requests against the same "
        "Graph Version shall produce the same visited "
        "and traversed ordering.",
    ):
        assert rule in content


def test_cycle_handling_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Traversal shall detect previously visited "
        "Graph Nodes and Graph Edges.",
        "Hierarchy Traversal shall never permit a cycle.",
        "Cycle detection shall produce deterministic "
        "Traversal Evidence.",
    ):
        assert rule in content


def test_traversal_result_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal Result represents the "
        "deterministic outcome of one Traversal Request."
    ) in content

    for property_name in (
        "Request Identifier.",
        "Graph Identifier.",
        "Graph Version.",
        "Traversal Status.",
        "Start Node Identifier.",
        "Target Node Identifier.",
        "Visited Node Sequence.",
        "Traversed Edge Sequence.",
        "Matched Paths.",
        "Maximum Depth Reached.",
        "Constraint Evaluation Result.",
        "Failure Reason.",
        "Traversal Evidence Reference.",
        "Result Integrity Reference.",
    ):
        assert property_name in model_text()


def test_traversal_statuses_and_transitions_are_defined() -> None:
    content = model_text()

    for status in TRAVERSAL_STATUSES:
        assert status in content

    normalized = normalized_text()

    for transition in (
        "Not Executed to Running.",
        "Running to Completed.",
        "Running to Failed.",
        "Running to Cancelled.",
    ):
        assert transition in normalized

    assert (
        "Completed, Failed, and Cancelled are terminal statuses."
    ) in normalized


def test_sequences_are_defined() -> None:
    content = normalized_text()

    assert (
        "The Start Node shall be the first visited node."
    ) in content

    assert (
        "No unregistered node shall appear in the "
        "Visited Node Sequence."
    ) in content

    assert (
        "No implicit Graph Edge shall appear in the "
        "Traversed Edge Sequence."
    ) in content


def test_matched_paths_and_continuity_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Matched Paths shall contain zero or more "
        "validated Graph Paths satisfying the "
        "Traversal Request.",
        "Every adjacent pair of Graph Nodes in a "
        "Matched Path shall be connected by the "
        "corresponding Graph Edge.",
        "A disconnected Node or Edge sequence shall "
        "not be accepted as a Matched Path.",
    ):
        assert rule in content


def test_traversal_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Traversal shall produce deterministic "
        "Traversal Evidence."
    ) in content

    for field_name in EVIDENCE_FIELDS:
        assert field_name in model_text()


def test_failed_traversal_evidence_is_required() -> None:
    content = normalized_text()

    for rule in (
        "A failed Traversal shall still produce "
        "Traversal Evidence.",
        "No failed Traversal shall omit evidence.",
    ):
        assert rule in content


def test_result_integrity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every terminal Traversal Result shall possess "
        "one deterministic Result Integrity Reference."
    ) in content


def test_traversal_determinism_is_defined() -> None:
    content = normalized_text()

    assert (
        "Identical Traversal Requests executed against "
        "the same immutable Graph Version and "
        "Traversal Context shall produce identical "
        "terminal Traversal Results."
    ) in content

    assert (
        "Execution Timestamp shall not alter normative "
        "Traversal Result equality."
    ) in content


def test_traversal_validation_stages_are_defined() -> None:
    content = normalized_text()

    assert (
        "Traversal validation shall occur before, "
        "during, and after navigation."
    ) in content

    for stage in (
        "Pre-Traversal Validation",
        "During-Traversal Validation",
        "Post-Traversal Validation",
    ):
        assert stage in model_text()


def test_failure_conditions_are_defined() -> None:
    content = normalized_text()

    for failure_condition in (
        "The Graph Manifest cannot be resolved.",
        "The Start Node is unregistered.",
        "The declared Target Node is unregistered.",
        "The Traversal Strategy is unknown.",
        "The Traversal Direction is unknown.",
        "A Relationship Type is private or unknown.",
        "Maximum Depth is negative.",
        "Edge direction is violated.",
        "A hierarchy cycle is detected.",
        "A path is disconnected.",
        "A baseline is incompatible.",
        "Traversal Evidence cannot be produced.",
        "Result Integrity cannot be established.",
    ):
        assert failure_condition in content


def test_cancellation_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal may enter Cancelled status only "
        "after entering Running status."
    ) in content

    assert (
        "Cancellation shall produce deterministic "
        "Traversal Evidence."
    ) in content


def test_traversal_constraints_summary_is_defined() -> None:
    content = normalized_text()

    for constraint in (
        "No Traversal may create a Graph Node.",
        "No Traversal may create a Graph Edge.",
        "No Traversal may create a semantic relationship.",
        "No Traversal may redefine canonical Commerce semantics.",
        "No Traversal may exceed Maximum Depth.",
        "No Traversal may bypass declared filters.",
        "No Traversal may ignore edge direction.",
        "No Traversal may include unregistered Graph Components.",
        "No terminal Traversal Result may omit Traversal Evidence.",
    ):
        assert constraint in content


def test_traversal_invariants_are_declared() -> None:
    content = model_text()

    for invariant in TRAVERSAL_INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Traversal is explicitly defined.",
        "Traversal Request is explicitly defined.",
        "Request Identity is defined.",
        "Start and Target Node behavior is defined.",
        "Traversal Context is explicitly defined.",
        "Context Immutability is defined.",
        "Traversal Strategies are defined.",
        "Traversal Directions are defined.",
        "Traversal Constraints are defined.",
        "Constraint Precedence is defined.",
        "Traversal Depth is defined.",
        "Maximum Depth Boundary is defined.",
        "Traversal Filters are defined.",
        "Traversal Ordering is defined.",
        "Cycle Handling is defined.",
        "Traversal Result is explicitly defined.",
        "Traversal Status and transitions are defined.",
        "Visited Node Sequence is defined.",
        "Traversed Edge Sequence is defined.",
        "Matched Paths and Path Continuity are defined.",
        "Traversal Evidence is defined.",
        "Failed Traversal Evidence is defined.",
        "Result Integrity is defined.",
        "Traversal Determinism is defined.",
        "Traversal Equality is defined.",
        "Traversal Validation is defined.",
        "Failure Conditions are defined.",
        "Cancellation behavior is defined.",
        "Traversal Constraints Summary is declared.",
        "Traversal Invariants are declared.",
    ):
        assert criterion in content
