from pathlib import Path


MODEL = Path(
    "research/governance/HAS_GOVERNANCE_MODEL.md"
)


def test_governance_model_exists() -> None:
    assert MODEL.is_file()


def test_governance_hierarchy() -> None:
    text = MODEL.read_text(
        encoding="utf-8",
    )

    expected = (
        "Program",
        "Milestone",
        "Deliverable",
        "Asset",
        "Executable Contract",
    )

    for item in expected:
        assert item in text


def test_every_asset_has_contract() -> None:
    text = MODEL.read_text(
        encoding="utf-8",
    )

    assert (
        "Every Asset shall have at least one"
        in text
    )

    assert "Executable Contract" in text
