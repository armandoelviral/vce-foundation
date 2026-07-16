from pathlib import Path


STYLE_GUIDE = Path(
    "research/specifications/SPECIFICATION_STYLE_GUIDE.md"
)

README = Path(
    "research/specifications/README.md"
)

MANIFEST = Path(
    "research/specifications/manifest/runtime_manifest.yaml"
)

REQUIRED_SECTIONS = (
    "Purpose",
    "Domain Definition",
    "Runtime Semantics",
    "Constraints",
    "Guaranteed Properties",
    "Verification",
)


def style_guide_text() -> str:
    return STYLE_GUIDE.read_text(
        encoding="utf-8",
    )


def test_style_guide_exists() -> None:
    assert STYLE_GUIDE.is_file()


def test_style_guide_defines_required_sections() -> None:
    text = style_guide_text()

    for section in REQUIRED_SECTIONS:
        assert section in text


def test_style_guide_references_specification_grammar() -> None:
    text = style_guide_text()

    assert "Runtime Specification Grammar" in text


def test_style_guide_is_referenced_by_readme() -> None:
    text = README.read_text(
        encoding="utf-8",
    )

    assert "Specification Style Guide" in text


def test_style_guide_is_referenced_by_manifest() -> None:
    text = MANIFEST.read_text(
        encoding="utf-8",
    )

    assert "SPECIFICATION_STYLE_GUIDE.md" in text
