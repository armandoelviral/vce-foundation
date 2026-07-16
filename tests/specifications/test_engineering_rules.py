from pathlib import Path


RULES = (
    Path(
        "research/engineering_rules/ER-010_MILESTONE_DISCIPLINE.md"
    ),
    Path(
        "research/engineering_rules/ER-011_MILESTONE_CHARTER.md"
    ),
    Path(
        "research/engineering_rules/ER-013_ASSET_VERIFICATION.md"
    ),
    Path(
        "research/engineering_rules/ER-014_EXECUTABLE_EVIDENCE.md"
    ),
)


def test_engineering_rules_exist() -> None:
    for rule in RULES:
        assert rule.is_file()


def test_engineering_rules_are_active() -> None:
    for rule in RULES:
        text = rule.read_text(
            encoding="utf-8",
        )

        assert "Status" in text
        assert "Active" in text
        assert "Rule" in text
        assert "Rationale" in text
