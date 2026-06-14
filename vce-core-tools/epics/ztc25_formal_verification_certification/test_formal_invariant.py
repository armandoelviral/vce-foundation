from epics.ztc25_formal_verification_certification.formal_invariant import (
    FormalInvariant,
)


def test_invariant_contains_identifier():

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    assert invariant.invariant_id == "INV-001"


def test_invariant_contains_description():

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    assert (
        invariant.description
        == "sequence never decreases"
    )


def test_invariant_serializes():

    invariant = FormalInvariant(
        invariant_id="INV-001",
        description="sequence never decreases",
    )

    assert invariant.to_dict() == {
        "invariant_id": "INV-001",
        "description": "sequence never decreases",
    }
