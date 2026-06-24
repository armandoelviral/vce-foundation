from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)
from epics.phase6_002_constitutional_reputation.reputation_registry import (
    ReputationRegistry,
)
from epics.phase6_002_constitutional_reputation.reputation_state import (
    ReputationState,
)
from epics.phase6_002_constitutional_reputation.reputation_verifier import (
    verify_reputation,
)


def test_end_to_end_reputation_flow():
    registry = ReputationRegistry()

    registry.add(
        ReputationRecord(
            "rep.001",
            "identity.001",
            10,
        )
    )

    registry.add(
        ReputationRecord(
            "rep.002",
            "identity.001",
            20,
        )
    )

    state = ReputationState.from_records(
        registry.records()
    )

    verification = verify_reputation(state)

    assert verification["verified"] is True
    assert verification["total_score"] == 30
