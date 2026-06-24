from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)
from epics.phase8_003_historical_trust_replay.replay_registry import (
    ReplayRegistry,
)


def test_registry_adds_record():
    registry = ReplayRegistry()

    record = ReplayRecord(
        "replay.001",
        "trust.001",
        100,
    )

    registry.add(record)

    assert registry.records() == [record]
