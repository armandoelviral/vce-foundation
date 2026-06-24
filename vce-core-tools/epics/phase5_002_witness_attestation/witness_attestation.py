from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)


def attest_witness(
    witness: WitnessRecord,
):
    return {
        "attested": True,
        "witness_id": witness.witness_id,
        "observation_id": witness.observation_id,
    }
