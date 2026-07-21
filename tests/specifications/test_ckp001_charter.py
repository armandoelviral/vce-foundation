from pathlib import Path


CHARTER = Path(
    "research/commerce/"
    "CKP001_CANONICAL_COMMERCE_VOCABULARY_CHARTER.md"
)

REQUIRED_DOMAINS = (
    "Organization",
    "Commercial Structure",
    "Product",
    "Assortment",
    "Inventory",
    "Pricing",
    "Promotion",
    "Procurement",
    "Wholesale",
    "Retail",
    "Ecommerce",
    "Marketplace",
    "Omnichannel",
    "Social Commerce",
    "Informal Commerce",
    "Distribution",
    "Logistics",
    "Fulfillment",
    "Visual Merchandising",
    "Space Management",
    "Customer",
    "Analytics",
    "Finance",
    "Governance",
)

REQUIRED_PRINCIPLES = (
    "Knowledge precedes implementation.",
    "Vocabulary precedes ontology.",
    "Ontology precedes models.",
    "Models precede services.",
    "Services precede applications.",
    "Canonical terms precede private terminology.",
    "Semantic identity precedes presentation labels.",
)

REQUIRED_DELIVERABLES = (
    "Canonical Vocabulary.",
    "Canonical Definitions.",
    "Canonical Relationships.",
    "Allowed Synonyms.",
    "Forbidden Synonyms.",
    "Applicability Domains.",
    "Normative Claims.",
    "Vocabulary Governance Rules.",
    "Semantic Audit.",
    "Vocabulary Freeze.",
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


def test_charter_declares_identity() -> None:
    content = normalized_text()

    assert "CKP-001" in content
    assert "Canonical Commerce Vocabulary" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_vision_declares_commerce_knowledge_platform() -> None:
    content = normalized_text()

    assert "canonical business language" in content
    assert "Commerce Knowledge Platform" in content
    assert "normative semantic foundation" in content


def test_scope_declares_required_domains() -> None:
    content = charter_text()

    for domain in REQUIRED_DOMAINS:
        assert domain in content


def test_charter_declares_out_of_scope() -> None:
    content = charter_text()

    for item in (
        "Implementation.",
        "Python Models.",
        "Databases.",
        "APIs.",
        "User Interfaces.",
        "Execution Logic.",
        "Artificial Intelligence.",
        "Domain Services.",
        "Applications.",
    ):
        assert item in content


def test_charter_declares_principles() -> None:
    content = normalized_text()

    for principle in REQUIRED_PRINCIPLES:
        assert principle in content


def test_charter_declares_deliverables() -> None:
    content = normalized_text()

    for deliverable in REQUIRED_DELIVERABLES:
        assert deliverable in content


def test_charter_requires_stable_term_identity() -> None:
    content = normalized_text()

    assert (
        "Every canonical term shall have a stable identifier."
        in content
    )

    assert (
        "Every canonical term shall have one preferred name."
        in content
    )

    assert (
        "Every canonical term shall have one canonical definition."
        in content
    )


def test_charter_unifies_commerce_channels() -> None:
    content = normalized_text()

    for channel in (
        "Retail",
        "Wholesale",
        "Ecommerce",
        "Marketplace",
        "Omnichannel",
        "Social Commerce",
        "Franchise",
        "Distribution",
        "Informal Commerce",
    ):
        assert channel in content


def test_charter_preserves_frozen_baselines() -> None:
    content = normalized_text()

    assert "HAS Foundation 1.0 LTS remains frozen." in content

    assert (
        "Specification Runtime 1.0 remains frozen."
        in content
    )

    assert (
        "without modifying their normative behavior"
        in content
    )


def test_charter_declares_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-001.2" in content
    assert "Vocabulary Structure" in content
