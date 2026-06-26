from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)
from epics.phase9_003_constitutional_deliberation.deliberation_registry import (
    DeliberationRegistry,
)
from epics.phase9_003_constitutional_deliberation.deliberation_state import (
    DeliberationState,
)
from epics.phase9_003_constitutional_deliberation.deliberation_verifier import (
    verify_deliberation,
)


def test_end_to_end_deliberation_flow():
    registry = DeliberationRegistry()

    registry.add(
        DeliberationRecord(
            "delib.001",
            "proposal.001",
            7,
        )
    )

    registry.add(
        DeliberationRecord(
            "delib.002",
            "proposal.002",
            5,
        )
    )

    state = DeliberationState.from_records(
        registry.records()
    )

    verification = verify_deliberation(state)

    assert verification["verified"] is True
    assert verification["total_deliberations"] == 2
    assert verification["total_participants"] == 12
