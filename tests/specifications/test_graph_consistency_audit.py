from pathlib import Path


AUDIT = Path(
    "research/commerce/knowledge_graph/"
    "GRAPH_CONSISTENCY_AUDIT.md"
)

REQUIRED_AUDIT_AREAS = (
    "Vocabulary Audit.",
    "Ontology Audit.",
    "Graph Manifest Audit.",
    "Node Audit.",
    "Edge Audit.",
    "Hierarchy Audit.",
    "Inverse Relationship Audit.",
    "Path Audit.",
    "Traversal Compatibility Audit.",
    "Deterministic Ordering Audit.",
    "Integrity Audit.",
    "Evidence Audit.",
    "Semantic Closure Audit.",
    "Traceability Audit.",
    "Failure Classification.",
    "Release Eligibility.",
)

AUDIT_PRINCIPLES = (
    "Deterministic.",
    "Repeatable.",
    "Non-mutating.",
    "Traceable.",
    "Auditable.",
    "Evidence-producing.",
    "Baseline-aware.",
    "Fail-closed.",
)

CONSISTENCY_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Registered Node Closure.",
    "Canonical Edge Closure.",
    "Single Root Preservation.",
    "Node Count Integrity.",
    "Edge Count Integrity.",
    "Preferred Name Preservation.",
    "Knowledge Object Type Preservation.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Hierarchy Acyclicity.",
    "No Self-Ancestry.",
    "No Duplicate Nodes.",
    "No Duplicate Edges.",
    "No Orphan Nodes.",
    "No Orphan Edges.",
    "No Implicit Graph Components.",
    "No Initial Reflexivity.",
    "Path Continuity.",
    "Path Length Integrity.",
    "Deterministic Node Ordering.",
    "Deterministic Edge Ordering.",
    "Graph Integrity.",
    "Node Integrity.",
    "Edge Integrity.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Evidence Completeness.",
    "Deterministic Audit Result.",
    "Fail-Closed Evaluation.",
    "Non-Mutation.",
)

FAILURE_CLASSIFICATIONS = (
    "MANIFEST_VIOLATION.",
    "VOCABULARY_VIOLATION.",
    "ONTOLOGY_VIOLATION.",
    "REGISTRY_CLOSURE_VIOLATION.",
    "NODE_VIOLATION.",
    "EDGE_VIOLATION.",
    "ROOT_VIOLATION.",
    "HIERARCHY_VIOLATION.",
    "INVERSE_VIOLATION.",
    "PATH_VIOLATION.",
    "ORDERING_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "SEMANTIC_CLOSURE_VIOLATION.",
    "TRACEABILITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

EVIDENCE_FIELDS = (
    "Evidence Identifier.",
    "Audit Identifier.",
    "Graph Identifier.",
    "Graph Version.",
    "Audit Rule.",
    "Validated Component Type.",
    "Validated Component Identifier.",
    "Vocabulary Validation Result.",
    "Ontology Validation Result.",
    "Registry Closure Result.",
    "Node Validation Result.",
    "Edge Validation Result.",
    "Hierarchy Validation Result.",
    "Inverse Validation Result.",
    "Path Validation Result.",
    "Ordering Validation Result.",
    "Integrity Validation Result.",
    "Semantic Closure Result.",
    "Traceability Result.",
    "Validation Result.",
    "Failure Classification.",
    "Failure Reason.",
    "Evidence Integrity Reference.",
)


def audit_text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        audit_text().split()
    )


def test_graph_consistency_audit_exists() -> None:
    assert AUDIT.is_file()


def test_audit_declares_identity() -> None:
    content = normalized_text()

    assert (
        "Commerce Knowledge Graph Consistency Audit"
        in content
    )
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_purpose_is_defined() -> None:
    content = normalized_text()

    assert (
        "Define the normative consistency audit for "
        "the Commerce Knowledge Graph."
    ) in content

    assert (
        "The audit shall detect violations without "
        "modifying the audited Graph."
    ) in content


def test_audit_target_is_defined() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-GRAPH-000001",
        "Initial Commerce Knowledge Graph 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "Exactly ten Graph Nodes.",
        "Exactly twelve Graph Edges.",
        "Exactly one root Graph Node.",
    ):
        assert requirement in content


def test_audit_scope_is_complete() -> None:
    content = audit_text()

    for area in REQUIRED_AUDIT_AREAS:
        assert area in content


def test_audit_principles_are_declared() -> None:
    content = audit_text()

    for principle in AUDIT_PRINCIPLES:
        assert principle in content

    assert (
        "The audit shall not repair, reinterpret, or "
        "silently normalize an invalid Graph."
    ) in normalized_text()


def test_vocabulary_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Vocabulary Audit shall verify that every "
        "Graph Node references one registered Canonical "
        "Commerce Term.",
        "No Graph Node may use an unregistered "
        "Canonical Identifier.",
        "No Graph Node may replace its Preferred Name "
        "with a private normative name.",
        "No Graph Node may redefine a frozen Canonical "
        "Definition.",
        "No private Knowledge Object Type may enter "
        "the Graph.",
        "No Forbidden Synonym may replace a Preferred Name.",
        "Vocabulary compatibility shall be evaluated "
        "against the frozen CKP-001 baseline.",
    ):
        assert rule in content


def test_ontology_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Ontology Audit shall verify that every "
        "Graph Node preserves its frozen CKP-002 "
        "Ontology Membership.",
        "The Ontology Audit shall verify that every "
        "Graph Edge derives from exactly one frozen "
        "CKP-002 Ontology Assertion.",
        "No Graph Edge may exist without a resolvable "
        "Ontology Assertion Reference.",
        "No Graph Component may privately redefine "
        "frozen Commerce semantics.",
    ):
        assert rule in content


def test_graph_manifest_audit_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Graph Identifier.",
        "Graph Version.",
        "Lifecycle Status.",
        "Root Node Identifier.",
        "Node Count.",
        "Edge Count.",
        "Vocabulary Baseline.",
        "Ontology Baseline.",
        "Node Registry Reference.",
        "Edge Registry Reference.",
        "Graph Integrity Reference.",
    ):
        assert field_name in audit_text()

    for requirement in (
        "The Graph Identifier shall be: "
        "CKP-GRAPH-000001",
        "The Graph Version shall be: 1.0",
        "The Root Node Identifier shall be: "
        "CKP-TERM-000001",
        "The declared Node Count shall equal the "
        "actual Graph Node count.",
        "The declared Edge Count shall equal the "
        "actual Graph Edge count.",
    ):
        assert requirement in content


def test_node_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Node Audit shall verify that exactly ten "
        "Graph Nodes exist.",
        "Every Graph Node shall reference exactly one "
        "registered Knowledge Object.",
        "Every Graph Node shall possess one unique "
        "Canonical Identifier.",
        "Every Graph Node shall preserve its registered "
        "Preferred Name.",
        "Every Graph Node shall preserve the TERM "
        "Knowledge Object Type.",
        "Every Graph Node shall declare one Node "
        "Integrity Reference.",
        "No duplicate Graph Node shall exist.",
        "No orphan Graph Node shall exist.",
        "No implicit Graph Node shall exist.",
        "No Graph Node shall represent more than one "
        "Knowledge Object.",
    ):
        assert rule in content


def test_root_node_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "CKP-TERM-000001 is the root Graph Node.",
        "The Preferred Name of the root Graph Node is "
        "Commerce.",
        "Exactly one root Graph Node exists.",
        "Commerce has no outgoing canonical Is A edge "
        "inside the Initial Commerce Knowledge Graph.",
        "Every non-root hierarchy Graph Node reaches "
        "Commerce through an explicit canonical "
        "hierarchy path.",
        "No second root Graph Node may exist.",
    ):
        assert rule in content


def test_edge_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Edge Audit shall verify that exactly "
        "twelve Graph Edges exist.",
        "Every Graph Edge shall reference exactly one "
        "frozen Ontology Assertion.",
        "Every Graph Edge shall possess one unique "
        "Relationship Identifier.",
        "Every Graph Edge shall reference one "
        "registered Source Graph Node.",
        "Every Graph Edge shall reference one "
        "registered Target Graph Node.",
        "Every Graph Edge shall use one canonical "
        "Relationship Type.",
        "Every Graph Edge shall preserve explicit "
        "directionality.",
        "Every Graph Edge shall declare one Edge "
        "Integrity Reference.",
        "No duplicate Graph Edge shall exist.",
        "No orphan Graph Edge shall exist.",
        "No implicit Graph Edge shall exist.",
        "No initial Graph Edge shall be reflexive.",
    ):
        assert rule in content


def test_canonical_relationship_types_are_audited() -> None:
    content = audit_text()

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

    normalized = normalized_text()

    assert (
        "Related To shall not replace a more specific "
        "canonical Relationship Type."
    ) in normalized

    assert (
        "An unknown or private Relationship Type shall "
        "cause audit failure."
    ) in normalized


def test_directionality_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Edge shall preserve the explicit "
        "directionality of its source Ontology Assertion.",
        "Source and Target presentation order shall "
        "not redefine edge direction.",
        "A Graph Edge shall not become bidirectional "
        "through presentation or traversal behavior.",
        "A reverse traversal shall not mutate the "
        "stored Graph Edge.",
        "Any mismatch between Graph directionality and "
        "Ontology directionality shall cause audit failure.",
    ):
        assert rule in content


def test_inverse_relationship_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Inverse-Paired Graph Edge shall "
        "reference its canonical inverse Graph Edge.",
        "Part Of shall remain inverse-consistent with "
        "Contains.",
        "Uses shall remain inverse-consistent with "
        "Used By.",
        "A missing, asymmetric, or incompatible inverse "
        "reference shall cause audit failure.",
    ):
        assert rule in content

    assert (
        "CKP-REL-000005 is inverse-paired with: "
        "CKP-REL-000006."
    ) in content

    assert (
        "CKP-REL-000008 is inverse-paired with: "
        "CKP-REL-000009."
    ) in content


def test_hierarchy_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Hierarchy Audit shall verify that exactly "
        "four hierarchy Graph Edges exist.",
        "Every hierarchy Graph Edge shall use the "
        "canonical Is A Relationship Type.",
        "Hierarchy Graph Edges shall remain acyclic.",
        "No Graph Node may become its own ancestor.",
        "No duplicate parent relationship may exist.",
        "No implicit hierarchy relationship may be "
        "treated as normative.",
    ):
        assert rule in content

    for assertion in (
        "Retail Is A Commerce.",
        "Wholesale Is A Commerce.",
        "Ecommerce Is A Commerce.",
        "Informal Commerce Is A Commerce.",
    ):
        assert assertion in content


def test_semantic_edge_audit_is_defined() -> None:
    content = normalized_text()

    assert (
        "The Semantic Edge Audit shall verify that "
        "exactly eight semantic Graph Edges exist."
    ) in content

    for assertion in (
        "SKU Part Of Product.",
        "Product Contains SKU.",
        "Product Tracked As SKU.",
        "Retail Uses Channel.",
        "Channel Used By Retail.",
        "Product Sold Through Channel.",
        "Inventory Applies To SKU.",
        "Customer Uses Channel.",
    ):
        assert assertion in content

    assert (
        "No semantic Graph Edge may create "
        "undocumented meaning."
    ) in content


def test_duplicate_and_orphan_audits_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "The audit shall detect duplicate Graph Nodes "
        "by Canonical Identifier.",
        "The audit shall detect duplicate Graph Edges "
        "by Relationship Identifier.",
        "Any prohibited duplicate shall cause audit failure.",
        "No orphan Graph Node shall exist.",
        "No orphan Graph Edge shall exist.",
        "Any orphan Graph Component shall cause audit failure.",
    ):
        assert rule in content


def test_path_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Path Audit shall verify every registered "
        "Graph Path.",
        "Every Graph Node in a path shall be registered.",
        "Every Graph Edge in a path shall be registered.",
        "Every adjacent Graph Node pair shall be "
        "connected by the corresponding Graph Edge.",
        "The declared Path Length shall equal the "
        "number of Graph Edges in the Ordered Edge Sequence.",
        "A disconnected Node or Edge sequence shall "
        "not be accepted as a valid Graph Path.",
    ):
        assert rule in content


def test_registered_paths_are_audited() -> None:
    content = audit_text()

    for path_identifier in (
        "CKP-PATH-000001.",
        "CKP-PATH-000002.",
        "CKP-PATH-000003.",
        "CKP-PATH-000004.",
    ):
        assert path_identifier in content

    normalized = normalized_text()

    assert (
        "CKP-TERM-000008. CKP-TERM-000007. "
        "CKP-TERM-000006."
    ) in normalized

    assert (
        "CKP-REL-000011. CKP-REL-000005."
    ) in normalized

    assert "Path Length 2" in normalized
    assert "Path Continuity Valid" in normalized


def test_traversal_compatibility_is_audited() -> None:
    content = normalized_text()

    for traversal_type in (
        "Hierarchy Traversal.",
        "Semantic Traversal.",
        "Mixed Traversal.",
        "Forward Traversal.",
        "Canonical inverse-aware Reverse Traversal.",
    ):
        assert traversal_type in audit_text()

    assert (
        "The audit shall not execute traversal algorithms."
    ) in content

    assert (
        "The audit shall verify structural readiness "
        "for deterministic traversal."
    ) in content


def test_deterministic_ordering_is_audited() -> None:
    content = normalized_text()

    for rule in (
        "The audit shall verify the Deterministic "
        "Node Order.",
        "The audit shall verify the Deterministic "
        "Edge Order.",
        "Identical Graph Component sets shall produce "
        "identical deterministic ordering.",
        "Presentation order shall not alter normative "
        "Graph identity or directionality.",
    ):
        assert rule in content

    for node_number in range(1, 11):
        assert (
            f"CKP-TERM-{node_number:06d}."
            in audit_text()
        )

    assert "CKP-REL-000001" in audit_text()
    assert "CKP-REL-000012." in audit_text()


def test_integrity_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "The Integrity Audit shall verify: Graph "
        "Integrity Reference. Node Integrity References. "
        "Edge Integrity References.",
        "CKP-GRAPH-INTEGRITY-000001",
        "Every Graph Node shall declare one "
        "deterministic Node Integrity Reference.",
        "Every Graph Edge shall declare one "
        "deterministic Edge Integrity Reference.",
        "Missing or inconsistent integrity references "
        "shall cause audit failure.",
    ):
        assert rule in content


def test_baseline_integrity_is_audited() -> None:
    content = normalized_text()

    assert (
        "CKP-001 Canonical Commerce Vocabulary 1.0."
        in audit_text()
    )
    assert (
        "CKP-002 Commerce Ontology 1.0."
        in audit_text()
    )

    assert (
        "A Graph Component referencing an unknown, "
        "different, or incompatible baseline shall "
        "cause audit failure."
    ) in content

    assert (
        "The audit shall not modify a frozen baseline."
    ) in content


def test_semantic_closure_is_audited() -> None:
    content = normalized_text()

    for rule in (
        "The Graph shall contain exactly the first ten "
        "registered Canonical Commerce Terms.",
        "The Graph shall contain exactly the twelve "
        "frozen CKP-002 Ontology Assertions.",
        "No unregistered Knowledge Object may enter "
        "the Graph.",
        "No private Graph Node may enter the Graph.",
        "No private Graph Edge may enter the Graph.",
        "No implicit semantic relationship may enter "
        "the Graph.",
        "No Graph Component may privately redefine "
        "frozen Commerce semantics.",
    ):
        assert rule in content


def test_traceability_audit_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node shall remain traceable to:"
        in content
    )
    assert (
        "Every Graph Edge shall remain traceable to:"
        in content
    )
    assert (
        "Every registered Graph Path shall remain "
        "traceable to its ordered Graph Nodes and "
        "Graph Edges."
    ) in content


def test_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every audit operation shall produce "
        "deterministic Graph Consistency Evidence."
    ) in content

    for field_name in EVIDENCE_FIELDS:
        assert field_name in audit_text()


def test_evidence_requirements_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Evidence shall be produced for successful audits.",
        "Evidence shall be produced for failed audits.",
        "Evidence shall identify the exact failed audit rule.",
        "Evidence shall identify the affected Graph Component.",
        "Evidence shall preserve deterministic failure "
        "classification.",
        "No audit result shall exist without Graph "
        "Consistency Evidence.",
    ):
        assert rule in content


def test_audit_result_is_fail_closed() -> None:
    content = normalized_text()

    assert "Permitted Audit Result values are: PASS. FAIL." in content

    assert (
        "PASS means that every mandatory audit rule "
        "is satisfied."
    ) in content

    assert (
        "FAIL means that one or more mandatory audit "
        "rules are violated."
    ) in content

    assert "The audit shall fail closed." in content

    assert (
        "Warnings shall not convert a mandatory "
        "failure into PASS."
    ) in content


def test_failure_conditions_are_defined() -> None:
    content = normalized_text()

    for condition in (
        "The Graph Manifest cannot be resolved.",
        "The Graph Identifier is missing or invalid.",
        "The Vocabulary Baseline is missing or incompatible.",
        "The Ontology Baseline is missing or incompatible.",
        "The declared Node Count differs from the "
        "actual Node Count.",
        "The declared Edge Count differs from the "
        "actual Edge Count.",
        "A Graph Node is unregistered.",
        "A Graph Edge references an unregistered "
        "Source Node.",
        "A Graph Edge references an unregistered "
        "Target Node.",
        "A Graph Edge uses an unknown or private "
        "Relationship Type.",
        "A hierarchy cycle exists.",
        "A registered Graph Path is disconnected.",
        "Graph Integrity cannot be established.",
        "Graph Consistency Evidence cannot be produced.",
        "Traceability Closure cannot be established.",
        "Semantic Closure cannot be established.",
    ):
        assert condition in content


def test_failure_classifications_are_declared() -> None:
    content = audit_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content

    assert (
        "An unknown failure shall not be silently "
        "classified as PASS."
    ) in normalized_text()


def test_non_mutation_is_defined() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Rewrite a Graph Component.",
        "Repair a broken inverse pair.",
        "Repair a disconnected Graph Path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify the audited Initial Commerce Knowledge Graph.",
    ):
        assert prohibition in content

    assert (
        "The audit reports violations; it does not "
        "repair them."
    ) in content


def test_consistency_invariants_are_declared() -> None:
    content = audit_text()

    for invariant in CONSISTENCY_INVARIANTS:
        assert invariant in content


def test_acceptance_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "The Graph Manifest is valid.",
        "The Graph Identifier is CKP-GRAPH-000001.",
        "The Graph Version is 1.0.",
        "Exactly ten registered Graph Nodes exist.",
        "Exactly twelve canonical Graph Edges exist.",
        "Exactly one root Graph Node exists.",
        "CKP-TERM-000001 is the root Graph Node.",
        "All Graph Edges use canonical Relationship Types.",
        "All inverse-paired Graph Edges are "
        "reciprocally consistent.",
        "The hierarchy is acyclic.",
        "No duplicate Graph Component exists.",
        "No orphan Graph Component exists.",
        "No implicit Graph Component exists.",
        "All registered Graph Paths are continuous.",
        "Semantic Closure is satisfied.",
        "Traceability Closure is satisfied.",
        "Graph Consistency Evidence is complete.",
        "No mandatory violation remains open.",
    ):
        assert criterion in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Purpose is explicitly defined.",
        "Audit Target is explicitly defined.",
        "Audit Scope is explicitly defined.",
        "Audit Principles are declared.",
        "Vocabulary Audit is explicitly defined.",
        "Ontology Audit is explicitly defined.",
        "Graph Manifest Audit is explicitly defined.",
        "Node Audit is explicitly defined.",
        "Root Node Audit is explicitly defined.",
        "Edge Audit is explicitly defined.",
        "Hierarchy Audit is explicitly defined.",
        "Path Audit is explicitly defined.",
        "Integrity Audit is explicitly defined.",
        "Semantic Closure Audit is explicitly defined.",
        "Traceability Audit is explicitly defined.",
        "Evidence is explicitly defined.",
        "Audit Result is explicitly defined.",
        "Failure Conditions are explicitly defined.",
        "Failure Classification is explicitly defined.",
        "Non-Mutation is explicitly defined.",
        "Consistency Invariants are declared.",
        "Acceptance Criteria are declared.",
    ):
        assert criterion in content

    assert (
        "The Initial Commerce Knowledge Graph is "
        "eligible for Freeze only when the Audit "
        "Result is PASS."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-003.8" in content
    assert "Commerce Knowledge Graph Freeze" in content
