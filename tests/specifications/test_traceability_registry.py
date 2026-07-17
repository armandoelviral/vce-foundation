from pathlib import Path

REGISTRY = Path(
    "research/specifications/TRACEABILITY.yaml"
)


def registry() -> str:
    return REGISTRY.read_text(encoding="utf-8")


def test_registry_exists() -> None:
    assert REGISTRY.is_file()


def test_registry_declares_claims() -> None:
    text = registry()

    assert "KS-001" in text
    assert "GP-001" in text


def test_registry_declares_required_fields() -> None:
    text = registry()

    for field in (
        "asset:",
        "capability:",
        "contracts:",
    ):
        assert field in text


def test_registry_contains_no_runtime_mapping() -> None:
    assert "runtime:" not in registry()
