from epics.ztc10_multi_party_verification.consensus_attestation import (
    ConsensusAttestation,
)

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)


def test_consensus_attestation_contains_quorum_result():

    witnesses = [
        WitnessResponse(
            witness_id="witness-001",
            state_root_hash="root-a",
            classical_signature="sig-001",
            pqc_signature="pqc-001",
            accepted=True,
        ),
        WitnessResponse(
            witness_id="witness-002",
            state_root_hash="root-a",
            classical_signature="sig-002",
            pqc_signature="pqc-002",
            accepted=True,
        ),
    ]

    attestation = ConsensusAttestation.build(
        winning_state_root="root-a",
        quorum_policy="2-of-3",
        witnesses=witnesses,
    )

    assert attestation["winning_state_root"] == "root-a"
    assert attestation["quorum_policy"] == "2-of-3"
    assert attestation["consensus_verified"] is True
    assert len(attestation["witnesses"]) == 2


def test_consensus_attestation_contains_signatures():

    witnesses = [
        WitnessResponse(
            witness_id="witness-001",
            state_root_hash="root-a",
            classical_signature="sig-001",
            pqc_signature="pqc-001",
            accepted=True,
        )
    ]

    attestation = ConsensusAttestation.build(
        winning_state_root="root-a",
        quorum_policy="1-of-1",
        witnesses=witnesses,
    )

    witness = attestation["witnesses"][0]

    assert witness["classical_signature"] == "sig-001"
    assert witness["pqc_signature"] == "pqc-001"
