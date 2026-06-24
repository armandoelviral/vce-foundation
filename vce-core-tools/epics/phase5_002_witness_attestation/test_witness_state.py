from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)
from epics.phase5_002_witness_attestation.witness_state import (
    WitnessState,
)


def test_builds_witness_state():
    state = WitnessState.from_records(
        [
            WitnessRecord(
                "w1",
                "obs.001",
                "human",
            )
        ]
    )

    assert state.total_witnesses == 1


def test_empty_state():
    state = WitnessState.from_records([])

    assert state.total_witnesses == 0
