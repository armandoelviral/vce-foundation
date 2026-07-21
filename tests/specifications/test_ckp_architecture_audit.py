from pathlib import Path

AUDIT = Path(
    "research/commerce/audits/"
    "CKP_ARCHITECTURE_AUDIT.md"
)


def audit_text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(audit_text().split())


def test_audit_exists() -> None:
    assert AUDIT.is_file()


def test_audit_declares_all_areas() -> None:
    content = audit_text()

    for area in (
        "Vocabulary",
        "Identifier Model",
        "Knowledge Registry",
        "Semantic Relationships",
        "Governance",
        "Traceability",
        "Domain Separation",
        "Scalability",
    ):
        assert area in content


def test_traceability_chain_exists() -> None:
    content = audit_text()

    for node in (
        "Term",
        "Claim",
        "Specification",
        "Implementation",
        "Decision",
        "Evidence",
    ):
        assert node in content


def test_domain_hierarchy_exists() -> None:
    content = normalized_text()

    for item in (
        "Commerce remains the root domain.",
        "Retail depends on Commerce.",
        "Visual Merchandising depends on Retail.",
        "Planogram depends on Visual Merchandising.",
        "No inverse architectural dependency exists.",
    ):
        assert item in content


def test_release_criteria_exist() -> None:
    content = normalized_text()

    for item in (
        "All audit areas verified.",
        "No architectural violations detected.",
        "Architecture declared coherent.",
        "Architecture eligible for Freeze.",
    ):
        assert item in content
