from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)


def test_witness_record_creation():
    record = WitnessRecord(
        witness_id="witness.001",
        observation_id="obs.001",
        witness_type="human",
    )

    assert record.witness_id == "witness.001"
    assert record.observation_id == "obs.001"


def test_rejects_empty_witness_id():
    try:
        WitnessRecord(
            witness_id="",
            observation_id="obs.001",
            witness_type="human",
        )
        assert False
    except ValueError as exc:
        assert "witness_id" in str(exc)


def test_rejects_empty_observation_id():
    try:
        WitnessRecord(
            witness_id="witness.001",
            observation_id="",
            witness_type="human",
        )
        assert False
    except ValueError as exc:
        assert "observation_id" in str(exc)
