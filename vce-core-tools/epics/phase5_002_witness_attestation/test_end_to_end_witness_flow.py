from epics.phase5_002_witness_attestation.witness_attestation import (
    attest_witness,
)
from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)
from epics.phase5_002_witness_attestation.witness_registry import (
    WitnessRegistry,
)


def test_end_to_end_witness_flow():
    registry = WitnessRegistry()

    witness = WitnessRecord(
        witness_id="witness.001",
        observation_id="obs.001",
        witness_type="human",
    )

    registry.add(witness)

    result = attest_witness(
        registry.records()[0]
    )

    assert result["attested"] is True
    assert result["witness_id"] == "witness.001"
