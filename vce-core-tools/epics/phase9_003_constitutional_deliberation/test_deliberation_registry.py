from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)
from epics.phase9_003_constitutional_deliberation.deliberation_registry import (
    DeliberationRegistry,
)


def test_registry_adds_deliberation():
    registry = DeliberationRegistry()

    registry.add(
        DeliberationRecord(
            "delib.001",
            "proposal.001",
            7,
        )
    )

    assert len(registry.records()) == 1
