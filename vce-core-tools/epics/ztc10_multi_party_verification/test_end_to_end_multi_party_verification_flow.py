from epics.ztc10_multi_party_verification.witness_contract import (
    WitnessContract,
)

from epics.ztc10_multi_party_verification.witness_registry import (
    WitnessRegistry,
)

from epics.ztc10_multi_party_verification.witness_response import (
    WitnessResponse,
)

from epics.ztc10_multi_party_verification.consensus_verifier import (
    ConsensusVerifier,
)

from epics.ztc10_multi_party_verification.state_root_ballot_box import (
    StateRootBallotBox,
)

from epics.ztc10_multi_party_verification.quorum_policy import (
    QuorumPolicy,
)

from epics.ztc10_multi_party_verification.consensus_attestation import (
    ConsensusAttestation,
)


def test_end_to_end_multi_party_verification_flow():

    registry = WitnessRegistry()

    registry.register(
        WitnessContract(
            witness_id="witness-001",
            public_key="pk-001",
        )
    )

    registry.register(
        WitnessContract(
            witness_id="witness-002",
            public_key="pk-002",
        )
    )

    responses = [
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

    eligible = [
        response
        for response in responses
        if ConsensusVerifier.verify(
            response,
            registry,
        )
    ]

    ballot = StateRootBallotBox.group(
        eligible
    )

    winner = QuorumPolicy.select(
        ballot,
        minimum_witnesses=2,
    )

    attestation = ConsensusAttestation.build(
        winning_state_root=winner,
        quorum_policy="2-of-2",
        witnesses=eligible,
    )

    assert winner == "root-a"
    assert attestation["consensus_verified"] is True
    assert len(attestation["witnesses"]) == 2
