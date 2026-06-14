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


def test_accepts_registered_witness():

    registry = WitnessRegistry()

    registry.register(
        WitnessContract(
            witness_id="witness-001",
            public_key="pk-001",
        )
    )

    response = WitnessResponse(
        witness_id="witness-001",
        state_root_hash="root-a",
        classical_signature="sig",
        pqc_signature="pqc",
        accepted=True,
    )

    assert ConsensusVerifier.verify(
        response,
        registry,
    )


def test_rejects_unknown_witness():

    registry = WitnessRegistry()

    response = WitnessResponse(
        witness_id="unknown",
        state_root_hash="root-a",
        classical_signature="sig",
        pqc_signature="pqc",
        accepted=True,
    )

    assert not ConsensusVerifier.verify(
        response,
        registry,
    )


def test_rejects_failed_execution():

    registry = WitnessRegistry()

    registry.register(
        WitnessContract(
            witness_id="witness-001",
            public_key="pk-001",
        )
    )

    response = WitnessResponse(
        witness_id="witness-001",
        state_root_hash="root-a",
        classical_signature="sig",
        pqc_signature="pqc",
        accepted=False,
    )

    assert not ConsensusVerifier.verify(
        response,
        registry,
    )
