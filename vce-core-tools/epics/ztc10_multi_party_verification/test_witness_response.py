from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


def test_witness_response_contains_state_root_and_signatures():

    response = WitnessResponse(
        witness_id="witness-001",
        state_root_hash="state-root-001",
        classical_signature="ed25519-signature",
        pqc_signature="ml-dsa-signature",
        accepted=True,
    )

    assert response.witness_id == "witness-001"
    assert response.state_root_hash == "state-root-001"
    assert response.classical_signature == "ed25519-signature"
    assert response.pqc_signature == "ml-dsa-signature"
    assert response.accepted is True


def test_witness_response_serializes():

    response = WitnessResponse(
        witness_id="witness-001",
        state_root_hash="state-root-001",
        classical_signature="ed25519-signature",
        pqc_signature="ml-dsa-signature",
        accepted=True,
    )

    assert response.to_dict() == {
        "witness_id": "witness-001",
        "state_root_hash": "state-root-001",
        "classical_signature": "ed25519-signature",
        "pqc_signature": "ml-dsa-signature",
        "accepted": True,
    }
