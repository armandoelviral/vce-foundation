from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)
from epics.phase6_001_constitutional_identity.identity_state import (
    IdentityState,
)


def test_builds_identity_state():
    records = [
        IdentityRecord(
            "identity.001",
            "subject.001",
            "human",
        )
    ]

    state = IdentityState.from_records(records)

    assert state.total_identities == 1


def test_empty_identity_state():
    state = IdentityState.from_records([])

    assert state.total_identities == 0
