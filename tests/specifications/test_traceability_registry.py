from pathlib import Path


REGISTRY = Path(
    "research/specifications/TRACEABILITY.yaml"
)


def registry_text() -> str:
    return REGISTRY.read_text(
        encoding="utf-8",
    )


def test_registry_exists() -> None:
    assert REGISTRY.is_file()


def test_registry_declares_claims() -> None:
    text = registry_text()

    assert "claims:" in text

    assert "KS-001" in text
    assert "GP-001" in text


def test_registry_declares_required_sections() -> None:
    text = registry_text()

    required = (
        "asset:",
        "capability:",
        "contracts:",
        "runtime:",
    )

    for section in required:
        assert section in text


def test_registry_references_assets() -> None:
    text = registry_text()

    assert "runtime_specification.md" in text


def test_registry_references_contracts() -> None:
    text = registry_text()

    assert "test_runtime_specification_consistency.py" in text
    assert "test_runtime_manifest.py" in text
