from pathlib import Path


MODEL = Path(
    "research/commerce/ontology/"
    "ONTOLOGY_HIERARCHY_MODEL.md"
)

HIERARCHY_PROPERTIES = (
    "Canonical Identifier.",
    "Parent Node.",
    "Child Node.",
    "Canonical Relationship Type.",
    "Directionality.",
    "Lifecycle Status.",
    "Evidence Reference.",
)

HIERARCHY_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Explicit Parentage.",
    "Direction Preservation.",
    "Acyclicity.",
    "No Self-Ancestry.",
    "No Duplicate Assertions.",
    "Hierarchy Consistency.",
    "Vocabulary Compatibility.",
    "Traceability Closure.",
)

AUDIT_EVIDENCE_FIELDS = (
    "Hierarchy Assertion Identifier.",
    "Parent Node Identifier.",
    "Child Node Identifier.",
    "Relationship Type.",
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


def test_hierarchy_model_exists() -> None:
    assert MODEL.is_file()


def test_hierarchy_assertion_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Hierarchy Assertion declares one explicit "
        "semantic relationship between one Parent Node "
        "and one Child Node."
    ) in content

    for property_name in HIERARCHY_PROPERTIES:
        assert property_name in model_text()


def test_canonical_hierarchy_relationship_is_defined() -> None:
    content = normalized_text()

    assert (
        "The canonical hierarchy relationship type is: Is A."
        in content
    )

    assert (
        "An Is A assertion means that the Child Node "
        "is a semantic specialization of the Parent Node."
    ) in content


def test_parent_and_child_nodes_are_defined() -> None:
    content = normalized_text()

    assert (
        "A Parent Node represents the broader canonical "
        "semantic category."
    ) in content

    assert (
        "A Child Node represents a narrower canonical "
        "semantic specialization."
    ) in content

    assert (
        "Every Child Node shall reference at least one "
        "explicit Parent Node."
    ) in content


def test_commerce_is_root_node() -> None:
    content = normalized_text()

    assert (
        "Commerce is the root Ontology Node of the "
        "Commerce Ontology."
    ) in content

    assert (
        "The Commerce root node shall not declare a "
        "parent within the Commerce Ontology."
    ) in content


def test_initial_hierarchy_is_declared() -> None:
    content = model_text()

    for node in (
        "Commerce",
        "Retail",
        "Wholesale",
        "Ecommerce",
        "Informal Commerce",
        "Product",
        "SKU",
        "Inventory",
        "Channel",
        "Retail Channel",
        "Wholesale Channel",
        "Ecommerce Channel",
        "Informal Commerce Channel",
    ):
        assert node in content


def test_hierarchy_directionality_is_declared() -> None:
    content = normalized_text()

    assert (
        "Hierarchy Assertions are directed from the "
        "broader Parent Node to the narrower Child Node."
    ) in content

    assert "Directionality shall be explicit." in content


def test_transitivity_is_constrained() -> None:
    content = normalized_text()

    assert (
        "Hierarchy transitivity may be derived only "
        "from explicit valid hierarchy assertions."
    ) in content

    assert (
        "Derived transitivity shall not replace explicit "
        "direct parent-child assertions."
    ) in content


def test_multiple_inheritance_is_constrained() -> None:
    content = normalized_text()

    assert (
        "A Child Node may declare more than one Parent "
        "Node only when each parent relationship is "
        "semantically valid and explicitly audited."
    ) in content

    assert (
        "Multiple inheritance shall not create "
        "contradictory canonical meaning."
    ) in content


def test_hierarchy_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Parent Node shall be a registered Ontology Node.",
        "Every Child Node shall be a registered Ontology Node.",
        "Every Hierarchy Assertion shall use the canonical "
        "Is A relationship type.",
        "A Node shall not be its own ancestor.",
        "Circular hierarchy paths shall be prohibited.",
        "Duplicate parent-child assertions shall be prohibited.",
        "Implicit hierarchy shall not be treated as normative.",
        "Domain-specific hierarchy shall not redefine canonical "
        "Commerce semantics.",
    ):
        assert constraint in content


def test_hierarchy_invariants_are_declared() -> None:
    content = model_text()

    for invariant in HIERARCHY_INVARIANTS:
        assert invariant in content


def test_audit_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Hierarchy Assertion shall produce "
        "deterministic audit evidence."
    ) in content

    for field_name in AUDIT_EVIDENCE_FIELDS:
        assert field_name in model_text()


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Hierarchy Assertion is explicitly defined.",
        "Canonical hierarchy relationship is defined.",
        "Root Node is declared.",
        "Initial hierarchy is declared.",
        "Directionality is declared.",
        "Transitivity is constrained.",
        "Multiple inheritance is constrained.",
        "Circularity is prohibited.",
        "Hierarchy invariants are declared.",
        "Audit Evidence is defined.",
    ):
        assert criterion in content
