from pathlib import Path


BASELINE = Path(
    "research/baselines/HAS_BASELINE_001.md"
)


def baseline_text() -> str:
    return BASELINE.read_text(
        encoding="utf-8",
    )


def test_baseline_exists() -> None:
    assert BASELINE.exists()


def test_contains_repository_rule() -> None:
    text = baseline_text()

    assert "Repository Rule" in text


def test_contains_milestones() -> None:
    text = baseline_text()

    assert "EKI" in text
    assert "SP" in text
    assert "Runtime" in text
    assert "Research" in text
