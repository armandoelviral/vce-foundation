from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)
from epics.phase6_004_constitutional_trust_engine.trust_state import (
    TrustState,
)


def test_builds_trust_state():
    records = [
        TrustRecord(
            "trust.001",
            "identity.001",
            10,
        ),
        TrustRecord(
            "trust.002",
            "identity.001",
            20,
        ),
    ]

    state = TrustState.from_records(records)

    assert state.total_records == 2
    assert state.total_score == 30


def test_empty_trust_state():
    state = TrustState.from_records([])

    assert state.total_records == 0
    assert state.total_score == 0
