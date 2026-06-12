from pathlib import Path


PRINCIPLES = Path(
    "docs/principles/veracity_principles.md"
)


def test_principles_4_to_8_exist():

    content = PRINCIPLES.read_text()

    assert "VERACITY PRINCIPLE #4" in content
    assert "VERACITY PRINCIPLE #5" in content
    assert "VERACITY PRINCIPLE #6" in content
    assert "VERACITY PRINCIPLE #7" in content
    assert "VERACITY PRINCIPLE #8" in content


def test_all_veracity_principles_present():

    content = PRINCIPLES.read_text()

    for number in range(1, 9):

        assert (
            f"VERACITY PRINCIPLE #{number}"
            in content
        )
