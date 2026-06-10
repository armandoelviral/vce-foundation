from pathlib import Path


PRINCIPLES = Path(
    "docs/principles/veracity_principles.md"
)


def test_principle_3_exists():

    content = PRINCIPLES.read_text()

    assert "VERACITY PRINCIPLE #3" in content


def test_principle_3_defines_execution_vs_decision():

    content = PRINCIPLES.read_text()

    assert (
        "A verifiable execution does not imply a correct decision."
        in content
    )


def test_principle_3_defines_veracity_scope():

    content = PRINCIPLES.read_text()

    assert "Veracity proves execution integrity." in content

    assert (
        "Veracity does not certify decision correctness."
        in content
    )


def test_principle_3_warns_about_verified_bad_outputs():

    content = PRINCIPLES.read_text()

    assert "perfectly verified execution" in content

    assert (
        "wrong, harmful, illegal, or biased result"
        in content
    )
