from epics.phase5_002_witness_attestation.witness_attestation import (
    attest_witness,
)
from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)


def test_attests_witness():
    witness = WitnessRecord(
        "witness.001",
        "obs.001",
        "human",
    )

    result = attest_witness(witness)

    assert result["attested"] is True


def test_attestation_contains_witness_id():
    witness = WitnessRecord(
        "witness.001",
        "obs.001",
        "human",
    )

    result = attest_witness(witness)

    assert result["witness_id"] == "witness.001"
