from pathlib import Path


PRINCIPLES = Path(
    "docs/principles/veracity_principles.md"
)


def test_principle_2_exists():

    content = PRINCIPLES.read_text()

    assert "VERACITY PRINCIPLE #2" in content


def test_principle_2_defines_evidence_longevity():

    content = PRINCIPLES.read_text()

    assert (
        "Evidence must outlive the cryptography used to create it."
        in content
    )


def test_principle_2_requires_future_verifiability():

    content = PRINCIPLES.read_text()

    assert "Historical evidence must remain replayable" in content
    assert "future cryptographic primitives" in content


def test_principle_2_protects_against_algorithm_drift():

    content = PRINCIPLES.read_text()

    assert "signature algorithm" in content
    assert "hash function" in content
    assert "certificate authority" in content
    assert "transparency ledger" in content
