from pathlib import Path


REGISTRY = Path(
    "research/commerce/registry/TERM_REGISTRY.md"
)

TERM_DIRECTORY = Path(
    "research/commerce/registry/terms"
)

REQUIRED_TERMS = {
    "CKP-TERM-000001": "Commerce",
    "CKP-TERM-000002": "Retail",
    "CKP-TERM-000003": "Wholesale",
    "CKP-TERM-000004": "Ecommerce",
    "CKP-TERM-000005": "Informal Commerce",
    "CKP-TERM-000006": "Product",
    "CKP-TERM-000007": "SKU",
    "CKP-TERM-000008": "Inventory",
    "CKP-TERM-000009": "Customer",
    "CKP-TERM-000010": "Channel",
}

MANDATORY_SECTIONS = (
    "## Preferred Name",
    "## Canonical Definition",
    "## Business Meaning",
    "## Allowed Synonyms",
    "## Forbidden Synonyms",
    "## Relationships",
    "## Applies To",
    "## Normative Claims",
    "## Business Examples",
    "## References",
    "## Status",
)


def term_files() -> tuple[Path, ...]:
    return tuple(
        sorted(
            TERM_DIRECTORY.glob(
                "CKP-TERM-*.md"
            )
        )
    )


def test_term_registry_exists() -> None:
    assert REGISTRY.is_file()


def test_term_directory_exists() -> None:
    assert TERM_DIRECTORY.is_dir()


def test_first_ten_terms_exist() -> None:
    assert len(term_files()) == 10


def test_registry_declares_first_ten_terms() -> None:
    content = REGISTRY.read_text(
        encoding="utf-8",
    )

    for identifier, name in REQUIRED_TERMS.items():
        assert identifier in content
        assert name in content


def test_every_term_has_unique_identifier() -> None:
    identifiers = tuple(
        path.name.split("_", maxsplit=1)[0]
        for path in term_files()
    )

    assert len(identifiers) == len(
        set(identifiers)
    )


def test_every_term_declares_mandatory_sections() -> None:
    for path in term_files():
        content = path.read_text(
            encoding="utf-8",
        )

        for section in MANDATORY_SECTIONS:
            assert section in content, (
                f"{path} missing {section}"
            )


def test_every_term_identifier_matches_filename() -> None:
    for path in term_files():
        content = path.read_text(
            encoding="utf-8",
        )

        identifier = path.name.split(
            "_",
            maxsplit=1,
        )[0]

        assert content.startswith(
            f"# {identifier}"
        )


def test_every_term_is_draft() -> None:
    for path in term_files():
        content = path.read_text(
            encoding="utf-8",
        )

        assert "## Status\n\nDraft" in content


def test_registry_declares_next_identifier() -> None:
    content = REGISTRY.read_text(
        encoding="utf-8",
    )

    assert "CKP-TERM-000011" in content
