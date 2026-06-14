from epics.ztc25_formal_verification_certification.proof_obligation import (
    ProofObligation,
)


def test_obligation_contains_identifier():

    obligation = ProofObligation(
        obligation_id="PO-001",
        invariant_id="INV-001",
        description="prove sequence monotonicity",
    )

    assert obligation.obligation_id == "PO-001"


def test_obligation_contains_invariant_reference():

    obligation = ProofObligation(
        obligation_id="PO-001",
        invariant_id="INV-001",
        description="prove sequence monotonicity",
    )

    assert obligation.invariant_id == "INV-001"


def test_obligation_contains_description():

    obligation = ProofObligation(
        obligation_id="PO-001",
        invariant_id="INV-001",
        description="prove sequence monotonicity",
    )

    assert (
        obligation.description
        == "prove sequence monotonicity"
    )


def test_obligation_serializes():

    obligation = ProofObligation(
        obligation_id="PO-001",
        invariant_id="INV-001",
        description="prove sequence monotonicity",
    )

    assert obligation.to_dict() == {
        "obligation_id": "PO-001",
        "invariant_id": "INV-001",
        "description": "prove sequence monotonicity",
    }
