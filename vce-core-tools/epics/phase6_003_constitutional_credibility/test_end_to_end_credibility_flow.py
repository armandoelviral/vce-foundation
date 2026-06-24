from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)
from epics.phase6_003_constitutional_credibility.credibility_registry import (
    CredibilityRegistry,
)
from epics.phase6_003_constitutional_credibility.credibility_state import (
    CredibilityState,
)
from epics.phase6_003_constitutional_credibility.credibility_verifier import (
    verify_credibility,
)


def test_end_to_end_credibility_flow():
    registry = CredibilityRegistry()

    registry.add(
        CredibilityRecord(
            "cred.001",
            "identity.001",
            10,
        )
    )

    registry.add(
        CredibilityRecord(
            "cred.002",
            "identity.001",
            20,
        )
    )

    state = CredibilityState.from_records(
        registry.records()
    )

    verification = verify_credibility(state)

    assert verification["verified"] is True
    assert verification["total_score"] == 30
