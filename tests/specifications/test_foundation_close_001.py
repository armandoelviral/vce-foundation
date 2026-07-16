from pathlib import Path


REQUIRED_SPEC_TESTS = (
    "test_runtime_specification_consistency.py",
    "test_specification_style_guide.py",
    "test_specification_grammar.py",
    "test_runtime_manifest.py",
    "test_specification_consistency.py",
    "test_traceability_schema.py",
    "test_traceability_registry.py",
)


def test_required_foundation_contracts_exist() -> None:
    root = Path("tests/specifications")

    for contract in REQUIRED_SPEC_TESTS:
        assert (root / contract).is_file()


def test_runtime_specification_exists() -> None:
    assert Path(
        "research/specifications/runtime_specification.md"
    ).is_file()


def test_style_guide_exists() -> None:
    assert Path(
        "research/specifications/SPECIFICATION_STYLE_GUIDE.md"
    ).is_file()


def test_grammar_exists() -> None:
    assert Path(
        "research/specifications/SPECIFICATION_GRAMMAR.md"
    ).is_file()


def test_manifest_exists() -> None:
    assert Path(
        "research/specifications/manifest/runtime_manifest.yaml"
    ).is_file()


def test_traceability_exists() -> None:
    assert Path(
        "research/specifications/TRACEABILITY.yaml"
    ).is_file()


def test_traceability_schema_exists() -> None:
    assert Path(
        "research/specifications/TRACEABILITY_SCHEMA.md"
    ).is_file()
