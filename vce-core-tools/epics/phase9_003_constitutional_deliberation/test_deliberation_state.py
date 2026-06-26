from epics.phase9_003_constitutional_deliberation.deliberation_record import (
    DeliberationRecord,
)
from epics.phase9_003_constitutional_deliberation.deliberation_state import (
    DeliberationState,
)


def test_builds_deliberation_state():
    records = [
        DeliberationRecord(
            "delib.001",
            "proposal.001",
            7,
        ),
        DeliberationRecord(
            "delib.002",
            "proposal.002",
            5,
        ),
    ]

    state = DeliberationState.from_records(records)

    assert state.total_deliberations == 2
    assert state.total_participants == 12


def test_empty_deliberation_state():
    state = DeliberationState.from_records([])

    assert state.total_deliberations == 0
    assert state.total_participants == 0
