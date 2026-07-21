from pathlib import Path

MODEL = Path(
    "research/commerce/"
    "CANONICAL_TERM_STRUCTURE.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_structure_exists() -> None:
    assert MODEL.is_file()


def test_identifier_exists() -> None:
    content = normalized()

    assert "Canonical Identifier" in content
    assert "CKP-TERM-000001" in content


def test_mandatory_sections_exist() -> None:
    content = text()

    for item in (
        "Preferred Name",
        "Canonical Definition",
        "Business Meaning",
        "Allowed Synonyms",
        "Forbidden Synonyms",
        "Relationships",
        "Applies To",
        "Normative Claims",
        "Business Examples",
        "References",
        "Status",
    ):
        assert item in content


def test_domains_exist() -> None:
    content = text()

    for domain in (
        "Retail",
        "Wholesale",
        "Marketplace",
        "Ecommerce",
        "Distribution",
    ):
        assert domain in content


def test_constraints_exist() -> None:
    content = normalized()

    assert (
        "Every Canonical Term shall define every section."
        in content
    )

    assert (
        "No section may be omitted."
        in content
    )


def test_release_criteria_exist() -> None:
    content = normalized()

    for item in (
        "Canonical structure defined.",
        "Mandatory sections declared.",
        "Lifecycle declared.",
    ):
        assert item in content
