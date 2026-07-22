from pathlib import Path


MODEL = Path(
    "research/commerce/ontology/"
    "ONTOLOGY_STRUCTURE_MODEL.md"
)

ONTOLOGY_COMPONENTS = (
    "Ontology Class.",
    "Ontology Node.",
    "Hierarchy Assertion.",
    "Relationship Assertion.",
    "Domain Membership Assertion.",
    "Ontology Constraint.",
    "Ontology Evidence.",
)

NODE_PROPERTIES = (
    "Canonical Identifier.",
    "Knowledge Object Type.",
    "Preferred Name.",
    "Ontology Class.",
    "Lifecycle Status.",
)

ONTOLOGY_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Registered Object Closure.",
    "Hierarchy Consistency.",
    "Relationship Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Domain Separation.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Deterministic Audit Evidence.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_ontology_structure_model_exists() -> None:
    assert MODEL.is_file()


def test_ontology_components_are_declared() -> None:
    content = model_text()

    for component in ONTOLOGY_COMPONENTS:
        assert component in content


def test_ontology_class_is_defined() -> None:
    content = normalized_text()

    assert (
        "An Ontology Class represents one canonical "
        "semantic category."
    ) in content

    assert (
        "Every Ontology Class shall reference one "
        "registered Knowledge Object."
    ) in content

    assert (
        "Every Ontology Class shall preserve the "
        "Canonical Identifier of its referenced "
        "Knowledge Object."
    ) in content


def test_ontology_node_structure_is_defined() -> None:
    content = model_text()

    assert (
        "An Ontology Node represents one registered"
        in content
    )

    for property_name in NODE_PROPERTIES:
        assert property_name in content


def test_hierarchy_assertion_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Hierarchy Assertion declares an explicit "
        "parent-child semantic relationship."
    ) in content

    for property_name in (
        "Parent Node.",
        "Child Node.",
        "Canonical Relationship Type.",
        "Directionality.",
        "Status.",
    ):
        assert property_name in model_text()


def test_relationship_assertion_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Relationship Assertion connects two "
        "registered Ontology Nodes."
    ) in content

    for property_name in (
        "Source Node.",
        "Canonical Relationship Type.",
        "Target Node.",
        "Directionality.",
        "Inverse Relationship Reference.",
        "Status.",
    ):
        assert property_name in model_text()


def test_domain_membership_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Domain Membership Assertion declares the "
        "Commerce domain or domains to which an "
        "Ontology Node applies."
    ) in content

    for domain in (
        "Commerce",
        "Retail",
        "Wholesale",
        "Ecommerce",
        "Marketplace",
        "Informal Commerce",
    ):
        assert domain in model_text()


def test_ontology_constraints_are_defined() -> None:
    content = model_text()

    for constraint_type in (
        "Class Membership.",
        "Hierarchy Compatibility.",
        "Relationship Direction.",
        "Inverse Consistency.",
        "Domain Separation.",
        "Canonical Identity Preservation.",
    ):
        assert constraint_type in content


def test_ontology_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Ontology Evidence demonstrates that one "
        "semantic assertion satisfies the Ontology "
        "Structure Model."
    ) in content

    assert (
        "Every audited assertion shall produce "
        "deterministic Ontology Evidence."
    ) in content


def test_ontology_graph_is_defined() -> None:
    content = normalized_text()

    assert "Ontology Nodes are graph nodes." in content

    assert (
        "Hierarchy Assertions and Relationship "
        "Assertions are directed graph edges."
    ) in content

    for property_name in (
        "Canonical.",
        "Directed.",
        "Traceable.",
        "Auditable.",
        "Semantically Closed.",
    ):
        assert property_name in model_text()


def test_mandatory_structure_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Ontology Node shall reference one "
        "registered Knowledge Object.",
        "Every semantic assertion shall reference "
        "registered Ontology Nodes.",
        "Every relationship shall use one canonical "
        "Relationship Type.",
        "Every assertion shall declare directionality.",
        "Every inverse-paired relationship shall "
        "preserve inverse consistency.",
        "No Ontology Node may redefine the canonical "
        "definition of its referenced Knowledge Object.",
    ):
        assert rule in content


def test_initial_ontology_structure_is_declared() -> None:
    content = normalized_text()

    assert (
        "The initial Commerce Ontology shall contain "
        "the first ten registered Canonical Terms."
    ) in content

    assert (
        "Commerce shall be the root Ontology Node."
    ) in content

    assert (
        "Retail, Wholesale, Ecommerce, and Informal "
        "Commerce shall be classified beneath Commerce."
    ) in content

    assert (
        "Product, SKU, Inventory, Customer, and Channel "
        "shall participate as canonical Commerce concepts."
    ) in content


def test_ontology_invariants_are_declared() -> None:
    content = model_text()

    for invariant in ONTOLOGY_INVARIANTS:
        assert invariant in content


def test_prohibited_behavior_is_declared() -> None:
    content = normalized_text()

    for constraint in (
        "No unregistered object may enter the Ontology.",
        "No private identifier may replace a Canonical Identifier.",
        "No implicit hierarchy shall be treated as normative.",
        "No ambiguous relationship shall be used.",
        "No domain specialization may redefine canonical "
        "Commerce semantics.",
    ):
        assert constraint in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Ontology components are explicitly defined.",
        "Ontology Node structure is explicitly defined.",
        "Hierarchy and Relationship Assertions are "
        "explicitly defined.",
        "Domain Membership is explicitly defined.",
        "Ontology Constraints are explicitly defined.",
        "Ontology Graph structure is explicitly defined.",
        "Initial Ontology Structure is declared.",
        "Ontology invariants are declared.",
    ):
        assert criterion in content
