from pathlib import Path


GRAMMAR = Path(
    "research/specifications/SPECIFICATION_GRAMMAR.md"
)

README = Path(
    "research/specifications/README.md"
)

MANIFEST = Path(
    "research/specifications/manifest/runtime_manifest.yaml"
)

NORMATIVE_CLAUSES = (
    "Purpose",
    "Domain Definition",
    "Runtime Semantics",
    "Constraints",
    "Guaranteed Properties",
    "Verification",
)

NORMATIVE_LANGUAGE = (
    "Shall",
    "Shall Not",
    "May",
    "Undefined",
)


def grammar_text() -> str:
    return GRAMMAR.read_text(
        encoding="utf-8",
    )


def test_grammar_exists() -> None:
    assert GRAMMAR.is_file()


def test_grammar_defines_six_normative_clauses() -> None:
    text = grammar_text()

    assert "six normative clauses" in text

    for clause in NORMATIVE_CLAUSES:
        assert clause in text


def test_grammar_defines_normative_language() -> None:
    text = grammar_text()

    assert "Normative Language" in text

    for term in NORMATIVE_LANGUAGE:
        assert term in text


def test_grammar_is_referenced_by_manifest() -> None:
    text = MANIFEST.read_text(
        encoding="utf-8",
    )

    assert "SPECIFICATION_GRAMMAR.md" in text


def test_grammar_is_referenced_by_readme() -> None:
    text = README.read_text(
        encoding="utf-8",
    )

    assert "Specification Grammar" in text
