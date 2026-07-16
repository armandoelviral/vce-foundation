from pathlib import Path

MANIFEST = Path(
    "research/specifications/manifest/runtime_manifest.yaml"
)


def manifest_text() -> str:
    return MANIFEST.read_text(
        encoding="utf-8",
    )


def test_manifest_exists() -> None:
    assert MANIFEST.is_file()


def test_manifest_declares_version() -> None:
    assert "version:" in manifest_text()


def test_manifest_declares_runtime_block() -> None:
    text = manifest_text()

    assert "runtime:" in text
    assert "specification:" in text


def test_manifest_references_normative_assets() -> None:
    text = manifest_text()

    required = (
        "runtime_specification.md",
        "SPECIFICATION_STYLE_GUIDE.md",
        "SPECIFICATION_GRAMMAR.md",
    )

    for asset in required:
        assert asset in text


def test_manifest_declares_contracts() -> None:
    text = manifest_text()

    assert "contracts:" in text
    assert "invariants:" in text


def test_manifest_declares_core_invariants() -> None:
    text = manifest_text()

    invariants = (
        "Replay Determinism",
        "History Integrity",
        "Verification Closure",
        "Pipeline Closure",
        "State Monotonicity",
    )

    for invariant in invariants:
        assert invariant in text
