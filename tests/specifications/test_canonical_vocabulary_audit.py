from pathlib import Path

MODEL = Path(
    "research/commerce/audits/"
    "CANONICAL_VOCABULARY_AUDIT.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_audit_exists() -> None:
    assert MODEL.is_file()


def test_scope_exists() -> None:
    content = text()

    for item in (
        "Canonical Identifiers",
        "Preferred Names",
        "Canonical Definitions",
        "Allowed Synonyms",
        "Forbidden Synonyms",
        "Relationships",
        "Applicability Domains",
        "Normative Claims",
        "Registry Consistency",
    ):
        assert item in content


def test_audit_rules_exist() -> None:
    content = normalized()

    rules = (
        "Every Canonical Identifier shall be unique.",
        "Every Preferred Name shall be unique.",
        "Every Definition shall exist.",
        "Every Canonical Term shall declare all mandatory sections.",
        "Every Relationship shall reference existing Canonical Terms.",
        "Forbidden Synonyms shall never appear as Preferred Names.",
        "Every registered term shall belong to the Knowledge Registry.",
    )

    for rule in rules:
        assert rule in content


def test_runtime_properties_exist() -> None:
    content = text()

    for item in (
        "Deterministic",
        "Repeatable",
        "Traceable",
        "Auditable",
    ):
        assert item in content


def test_release_criteria_exist() -> None:
    content = normalized()

    criteria = (
        "Identifier uniqueness verified.",
        "Preferred Name uniqueness verified.",
        "Relationship consistency verified.",
        "Registry consistency verified.",
        "Vocabulary integrity verified.",
    )

    for criterion in criteria:
        assert criterion in content
