from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_registry import (
    CivilizationReplayRegistry,
)


def test_registry_adds_record():
    registry = CivilizationReplayRegistry()

    record = CivilizationReplayRecord(
        "civ_replay.001",
        "snapshot.001",
        100,
    )

    registry.add(record)

    assert registry.records() == [record]
