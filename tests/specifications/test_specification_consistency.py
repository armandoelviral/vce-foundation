from pathlib import Path


SPEC_ROOT = Path("research/specifications")

README = SPEC_ROOT / "README.md"

MANIFEST = SPEC_ROOT / "manifest" / "runtime_manifest.yaml"

ASSETS = {
    "runtime_specification.md":
        SPEC_ROOT / "runtime_specification.md",

    "SPECIFICATION_STYLE_GUIDE.md":
        SPEC_ROOT / "SPECIFICATION_STYLE_GUIDE.md",

    "SPECIFICATION_GRAMMAR.md":
        SPEC_ROOT / "SPECIFICATION_GRAMMAR.md",

    "runtime_manifest.yaml":
        MANIFEST,
}

CONTRACTS = (
    Path("tests/specifications/test_runtime_specification_consistency.py"),
    Path("tests/specifications/test_specification_style_guide.py"),
    Path("tests/specifications/test_specification_grammar.py"),
    Path("tests/specifications/test_runtime_manifest.py"),
)


def test_all_normative_assets_exist() -> None:
    for asset in ASSETS.values():
        assert asset.is_file()


def test_readme_references_published_assets() -> None:
    text = README.read_text(
        encoding="utf-8",
    )

    assert "Runtime Specification" in text
    assert "Specification Style Guide" in text
    assert "Specification Grammar" in text
    assert "runtime_manifest.yaml" in text


def test_manifest_references_normative_assets() -> None:
    text = MANIFEST.read_text(
        encoding="utf-8",
    )

    assert "runtime_specification.md" in text
    assert "SPECIFICATION_STYLE_GUIDE.md" in text
    assert "SPECIFICATION_GRAMMAR.md" in text


def test_every_asset_has_contract() -> None:
    for contract in CONTRACTS:
        assert contract.is_file()


def test_no_missing_normative_assets() -> None:
    for _, asset in ASSETS.items():
        assert asset.exists()
