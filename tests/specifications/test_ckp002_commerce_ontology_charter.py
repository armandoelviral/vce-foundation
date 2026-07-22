from pathlib import Path


CHARTER = Path(
    "research/commerce/ontology/"
    "CKP002_COMMERCE_ONTOLOGY_CHARTER.md"
)

REQUIRED_INPUTS = (
    "CKP-001 Canonical Commerce Vocabulary 1.0.",
    "Canonical Commerce Terms.",
    "Canonical Identifiers.",
    "Knowledge Object Architecture.",
    "Semantic Relationship Model.",
    "Knowledge Registry.",
)

REQUIRED_OUTPUTS = (
    "Commerce Ontology.",
    "Ontology Classes.",
    "Ontology Hierarchies.",
    "Canonical Relationship Assertions.",
    "Domain Membership Assertions.",
    "Ontology Constraints.",
    "Ontology Audit Evidence.",
)

REQUIRED_DOMAINS = (
    "Commerce",
    "Retail",
    "Wholesale",
    "Ecommerce",
    "Marketplace",
    "Omnichannel",
    "Social Commerce",
    "Informal Commerce",
    "Organization",
    "Commercial Structure",
    "Product",
    "SKU",
    "Assortment",
    "Inventory",
    "Pricing",
    "Promotion",
    "Procurement",
    "Distribution",
    "Logistics",
    "Fulfillment",
    "Visual Merchandising",
    "Space Management",
    "Customer",
    "Channel",
    "Analytics",
    "Finance",
    "Governance",
)

REQUIRED_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Hierarchy Consistency.",
    "Relationship Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Domain Separation.",
    "Semantic Closure.",
    "Traceability Closure.",
)

INITIAL_TERMS = (
    "CKP-TERM-000001 Commerce.",
    "CKP-TERM-000002 Retail.",
    "CKP-TERM-000003 Wholesale.",
    "CKP-TERM-000004 Ecommerce.",
    "CKP-TERM-000005 Informal Commerce.",
    "CKP-TERM-000006 Product.",
    "CKP-TERM-000007 SKU.",
    "CKP-TERM-000008 Inventory.",
    "CKP-TERM-000009 Customer.",
    "CKP-TERM-000010 Channel.",
)


def charter_text() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        charter_text().split()
    )


def test_ckp002_charter_exists() -> None:
    assert CHARTER.is_file()


def test_ckp002_declares_identity() -> None:
    content = normalized_text()

    assert "CKP-002" in content
    assert "Commerce Ontology" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_ckp002_declares_vision_and_mission() -> None:
    content = normalized_text()

    assert (
        "canonical and verifiable representation "
        "of Commerce knowledge"
    ) in content

    assert (
        "Transform the frozen Canonical Commerce "
        "Vocabulary into an explicit semantic model."
    ) in content


def test_ckp002_declares_required_inputs() -> None:
    content = charter_text()

    for item in REQUIRED_INPUTS:
        assert item in content


def test_ckp002_declares_required_outputs() -> None:
    content = charter_text()

    for item in REQUIRED_OUTPUTS:
        assert item in content


def test_ckp002_declares_commerce_scope() -> None:
    content = charter_text()

    for domain in REQUIRED_DOMAINS:
        assert domain in content


def test_ckp002_declares_ontology_responsibilities() -> None:
    content = normalized_text()

    for responsibility in (
        "Classify registered Knowledge Objects.",
        "Define canonical parent-child relationships.",
        "Define domain membership.",
        "Define relationship directionality.",
        "Preserve inverse relationship consistency.",
        "Prevent semantic duplication.",
        "Prevent private redefinition of canonical "
        "Commerce concepts.",
        "Maintain traceability to canonical terms.",
    ):
        assert responsibility in content


def test_ckp002_declares_non_goals() -> None:
    content = normalized_text()

    for non_goal in (
        "create application code",
        "create Python domain models",
        "create database schemas",
        "implement a graph database",
        "implement runtime execution logic",
        "infer undocumented business meaning",
        "replace the Canonical Commerce Vocabulary",
        "redefine frozen CKP-001 semantics",
        "create user interfaces",
        "create commercial decision services",
    ):
        assert non_goal in content


def test_ckp002_declares_ontology_invariants() -> None:
    content = charter_text()

    for invariant in REQUIRED_INVARIANTS:
        assert invariant in content


def test_ckp002_preserves_frozen_baselines() -> None:
    content = normalized_text()

    assert "HAS Foundation 1.0 LTS remains frozen." in content

    assert (
        "Specification Runtime 1.0 remains frozen."
        in content
    )

    assert (
        "CKP-001 Canonical Commerce Vocabulary 1.0 "
        "remains frozen."
    ) in content

    assert (
        "without modifying their normative behavior "
        "or canonical semantics"
    ) in content


def test_ckp002_declares_initial_term_boundary() -> None:
    content = charter_text()

    for term in INITIAL_TERMS:
        assert term in content

    assert (
        "No additional term shall enter the initial "
        "ontology without registration in the "
        "Knowledge Registry."
    ) in normalized_text()


def test_ckp002_declares_success_criteria() -> None:
    content = normalized_text()

    for criterion in (
        "Every ontology class references a registered "
        "Knowledge Object.",
        "Every hierarchy is explicit.",
        "Every relationship assertion uses a canonical "
        "relationship type.",
        "No ontology node exists without a canonical "
        "identifier.",
        "No frozen canonical definition is privately "
        "redefined.",
        "Ontology consistency is executable and auditable.",
        "The initial Commerce ontology is semantically "
        "closed over the first ten canonical terms.",
    ):
        assert criterion in content


def test_ckp002_declares_deliverables() -> None:
    content = charter_text()

    for deliverable in (
        "Commerce Ontology Charter.",
        "Ontology Structure Model.",
        "Ontology Class Model.",
        "Hierarchy Model.",
        "Relationship Assertion Model.",
        "Initial Commerce Ontology.",
        "Ontology Consistency Audit.",
        "Ontology Freeze.",
    ):
        assert deliverable in content


def test_ckp002_declares_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-002.2" in content
    assert "Ontology Structure Model" in content
